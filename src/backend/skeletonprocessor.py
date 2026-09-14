import heapq

import numpy as np
from scipy.ndimage import binary_dilation, convolve, label

# One definition of "connected" for the whole module, so that counting neighbors,
# labelling components and measuring distances cannot disagree with each other.
# The skeleton is 8-connected, so the diagonals count as neighbors as well.
NEIGHBOR_KERNEL = np.array([[1, 1, 1],
							[1, 0, 1],
							[1, 1, 1]], dtype=np.uint8)
# In clockwise order on purpose: count_neighbor_groups() reads them as a ring
# around the pixel, so neighbors that follow each other here have to touch.
NEIGHBOR_OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1),
					(1, 0), (1, -1), (0, -1), (-1, -1))
CONNECTIVITY_8 = np.ones((3, 3), dtype=np.uint8)
# Geometric length of a diagonal step. Used to measure distances in the pixel graph,
# where an actual distance is needed to find the way along a segment; the length of a
# chain is estimated with the weights below instead.
DIAGONAL_STEP = float(np.sqrt(2))
# Weights of the length estimator (Vossepoel/Smeulders), see measure_chain_length():
# one straight step, one diagonal step, one direction change.
STRAIGHT_WEIGHT = 0.980
DIAGONAL_WEIGHT = 1.406
CORNER_WEIGHT = 0.091


class SkeletonProcessor:
	r"""
	Process and analyze skeletonized images. Provides functions to detect endpoints, branch points, main endpoints,
	and remove small branches from a skeletonized image.
	"""
	def __init__(self):
		r"""
		Initialize the SkeletonProcessor with an empty dictionary to store skeleton data.
		"""
		self.skeletons = {}

	def count_neighbors(self, skeleton):
		r"""
		Count the set neighbors of every pixel in the skeleton.

		One neighbor means a loose end, two mean a piece of line, three or more mean
		the pixel may be a fork (see find_branch_points, which takes a closer look).
		Everything outside the image counts as background, otherwise a crack running
		into the image border would look as if the line continued there.

		\param skeleton: A binary skeletonized image.
		\return: An integer array with the number of set neighbors per pixel.
		"""
		binary = (np.asarray(skeleton) > 0).astype(np.uint8)
		return convolve(binary, NEIGHBOR_KERNEL, mode="constant", cval=0)

	def find_end_points(self, skeleton):
		r"""
		Detect endpoints in a skeletonized image.
		Endpoints are the loose ends of the skeleton, i.e. pixels with a single neighbor.

		\param skeleton: A binary skeletonized image.
		\return: A boolean array marking endpoint locations.
		"""
		binary = np.asarray(skeleton) > 0
		return binary & (self.count_neighbors(binary) == 1)

	def find_branch_points(self, skeleton):
		r"""
		Identify branch points in a skeletonized image.

		A branch point is a real fork: three or more branches leave it in different
		directions. Counting neighbors alone is not enough, because a skeleton draws
		a slanted line as a small staircase and the corner pixel of such a step has
		three neighbors without anything branching off there. Those neighbors all
		touch each other, so counting the groups they form tells the two apart.

		\param skeleton: A binary skeletonized image.
		\return: A boolean array marking branch point locations.
		"""
		binary = np.asarray(skeleton) > 0
		branch_points = np.zeros(binary.shape, dtype=bool)
		# Three neighbors are the minimum for a fork, so only those pixels are worth
		# the closer look; on a full image that is a handful instead of millions.
		for pixel in zip(*np.where(binary & (self.count_neighbors(binary) >= 3))):
			if self.count_neighbor_groups(binary, pixel) >= 3:
				branch_points[pixel] = True
		return branch_points

	def count_neighbor_groups(self, skeleton, pixel):
		r"""
		Count how many separate groups of set pixels lie around a pixel.

		The eight neighbors are read as a ring around the pixel, and every place
		where background turns into skeleton starts a new group. One group is a loose
		end, two mean the pixel sits somewhere on a line, three or more mean that
		three branches leave it and it is a fork.

		Reading the ring is what tells a fork from a bend. The three neighbors of the
		corner pixel of a staircase follow each other on the ring and are one group,
		while the three neighbors of a T-shaped fork are separated by background and
		count as three.

		\param skeleton: A binary skeletonized image.
		\param pixel: The (row, col) pixel to look at.
		\return: The number of groups around the pixel.
		"""
		row, col = pixel
		ring = []
		for row_offset, col_offset in NEIGHBOR_OFFSETS:
			neighbor = (row + row_offset, col + col_offset)
			inside_image = 0 <= neighbor[0] < skeleton.shape[0] and 0 <= neighbor[1] < skeleton.shape[1]
			ring.append(bool(inside_image and skeleton[neighbor]))
		# ring[index - 1] wraps around for the first entry, which closes the ring.
		return sum(1 for index, is_set in enumerate(ring) if is_set and not ring[index - 1])

	def find_junction_zones(self, skeleton):
		r"""
		Mark the area a fork takes up, not just the pixel in its middle.

		Removing only the middle pixel is not enough to separate the branches: in an
		8-connected skeleton the three branches of a fork still touch each other
		diagonally around it and would come out as one piece. Taking the fork pixel
		together with the pixels immediately around it pulls the branches apart, and
		it also puts forks that sit one or two pixels apart into a single area, which
		is what they are.

		\param skeleton: A binary skeletonized image.
		\return: A boolean array marking the fork areas.
		"""
		binary = np.asarray(skeleton) > 0
		return binary_dilation(self.find_branch_points(binary), structure=CONNECTIVITY_8) & binary

	def find_main_endpoints(self, skeleton):
		r"""
		Determine the endpoints that mark the ends of the main line.

		The main line of a crack is the longest way through it, so its ends are the
		two loose ends that are furthest apart when measured along the skeleton, not
		as the crow flies: a bent crack can have its two ends lying next to each
		other. Found per connected part, because an image usually holds several
		separate cracks and each of them has to keep its own two ends.

		The two ends are found with the usual double sweep - go as far as possible
		from any starting point, then as far as possible from there. That is exact
		for a skeleton without closed loops, which is the normal case here.

		\param skeleton: A binary skeletonized image.
		\return: A NumPy array of (row, col) endpoints, two per connected part.
		"""
		graph = self.build_segment_graph(self.find_branch_segments(skeleton))

		main_endpoints = []
		visited = set()
		for node in graph:
			if node in visited:
				continue
			distances = self.distances_from(graph, node)
			visited.update(distances)
			first = self.furthest_end_point(distances)
			if first is None:
				continue
			second = self.furthest_end_point(self.distances_from(graph, first), exclude=first)
			if second is None:
				continue
			main_endpoints.append(first[1])
			main_endpoints.append(second[1])

		if not main_endpoints:
			return np.empty((0, 2), dtype=int)
		return np.array(main_endpoints)

	def build_segment_graph(self, segments):
		r"""
		Build a graph out of the segments to work on the shape of the skeleton
		instead of on single pixels.

		The nodes are the junctions and the loose ends, the edges are the segments
		between them, weighted with their length. A skeleton of a few hundred
		thousand pixels usually boils down to a handful of nodes this way.

		\param segments: The segments as returned by find_branch_segments().
		\return: A dictionary mapping a node to a list of (neighbor, length) pairs.
		"""
		graph = {}
		for segment in segments:
			nodes = self.segment_nodes(segment)
			# Fewer than two nodes means a closed loop that leads back to where it
			# started; more than two only happens where forks sit right next to each
			# other and the piece between them belongs to all of them.
			for first in range(len(nodes)):
				for second in range(first + 1, len(nodes)):
					graph.setdefault(nodes[first], []).append((nodes[second], segment["length"]))
					graph.setdefault(nodes[second], []).append((nodes[first], segment["length"]))
		return graph

	def segment_nodes(self, segment):
		r"""
		Name the points a segment runs between: the junctions it touches and its
		loose ends.

		\param segment: One segment as returned by find_branch_segments().
		\return: A list of node keys for the segment graph.
		"""
		return ([("junction", junction) for junction in sorted(segment["junctions"])]
				+ [("end", point) for point in segment["end_points"]])

	def distances_from(self, graph, start):
		r"""
		Measure the distance along the skeleton from one node to every node it is
		connected to (Dijkstra).

		\param graph: The segment graph as returned by build_segment_graph().
		\param start: The node to start from.
		\return: A dictionary mapping every reachable node to its distance.
		"""
		return self.shortest_paths_from(graph, start)[0]

	def shortest_paths_from(self, graph, start):
		r"""
		Walk a graph from one node with Dijkstra and keep both what came out of it:
		how far every node is away, and which node it was reached over.

		\param graph: A graph of (neighbor, length) pairs per node.
		\param start: The node to start from.
		\return: A pair of dictionaries, the distance per node and the node it was
			reached from (None for the starting node).
		"""
		distances = {start: 0.0}
		previous = {start: None}
		queue = [(0.0, start)]
		while queue:
			distance, node = heapq.heappop(queue)
			if distance > distances[node]:
				continue
			for neighbor, length in graph.get(node, ()):
				candidate = distance + length
				if candidate < distances.get(neighbor, float("inf")):
					distances[neighbor] = candidate
					previous[neighbor] = node
					heapq.heappush(queue, (candidate, neighbor))
		return distances, previous

	def furthest_chain(self, graph, start):
		r"""
		List the nodes on the way from a starting node to the node furthest away from
		it, in the order they are passed.

		Reading the way back over the predecessors is what makes the order reliable.
		Simply walking the pixels from one neighbor to the next gets stuck: in an
		8-connected skeleton a bend offers two ways on at once and the wrong one ends
		in a dead end halfway along. Sorting the pixels by their distance would work
		on a plain piece of line, but not where a fork area hangs off the middle of
		one - the pixel of the fork would be sorted into the middle of the line
		without touching its neighbors there.

		\param graph: A graph of (neighbor, length) pairs per node.
		\param start: The node to start from.
		\return: A list of nodes, beginning with the starting node.
		"""
		distances, previous = self.shortest_paths_from(graph, start)
		node = max(distances.items(), key=lambda entry: entry[1])[0]

		chain = []
		while node is not None:
			chain.append(node)
			node = previous[node]
		chain.reverse()
		return chain

	def furthest_end_point(self, distances, exclude=None):
		r"""
		Pick the loose end that is furthest away in a set of measured distances.
		Junctions are skipped: the main line has to end in a loose end.

		\param distances: The distances as returned by distances_from().
		\param exclude: A node to leave out, so that a sweep cannot end where it began.
		\return: The furthest end node, or None if there is none.
		"""
		candidates = [(distance, node) for node, distance in distances.items()
					  if node[0] == "end" and node != exclude]
		if not candidates:
			return None
		return max(candidates)[1]

	def find_branch_segments(self, skeleton):
		r"""
		Split the skeleton into its segments at the junctions.

		A segment is an uninterrupted run of line pixels: the piece between two
		junctions, the piece between a junction and a loose end, or a whole part of
		the skeleton that never branches at all. The forks themselves belong to no
		segment, they are cut out beforehand (see find_junction_zones).

		What a segment is attached to tells the three cases apart: no junction means
		a line standing on its own, exactly one junction plus one loose end means a
		side branch, everything else connects junctions and therefore carries the
		line itself.

		\param skeleton: A binary skeletonized image.
		\return: A list of dictionaries, one per segment, with "pixels" (the pixels
			it consists of), "length" (its length measured from the junctions it hangs
			on, see measure_segment_length), "junctions" (the junctions it touches,
			mapped to the pixel of each where the segment meets it) and "end_points"
			(its loose ends).
		"""
		binary = np.asarray(skeleton) > 0
		neighbor_count = self.count_neighbors(binary)
		junction_zones = self.find_junction_zones(binary)
		segment_mask = binary & ~junction_zones

		junction_labels, _ = label(junction_zones, structure=CONNECTIVITY_8)
		segment_labels, _ = label(segment_mask, structure=CONNECTIVITY_8)
		shape = binary.shape

		# Collect the pixels of every segment in one pass; going over the image once
		# per segment would mean scanning it hundreds of times on a real crack.
		pixels_per_segment = {}
		for row, col in zip(*np.where(segment_mask)):
			pixels_per_segment.setdefault(segment_labels[row, col], set()).add((int(row), int(col)))

		segments = []
		for pixels in pixels_per_segment.values():
			# The ends of a segment are the pixels with at most one neighbor inside
			# it; a loose end is one that has no other neighbor in the skeleton either.
			ends = [pixel for pixel in pixels if len(self.neighbors_within(pixel, pixels, shape)) <= 1]
			end_points = [pixel for pixel in ends if neighbor_count[pixel] == 1]

			# Every pixel has to be checked, not only the ends: a fork area is wider
			# than a single pixel and can touch a segment anywhere along it.
			junctions = {}
			for pixel in pixels:
				junctions.update(self.find_adjacent_junctions(pixel, junction_labels, shape))

			segments.append({
				"pixels": pixels,
				"length": self.measure_segment_length(pixels, end_points or ends, junctions, shape),
				"junctions": junctions,
				"end_points": end_points,
			})
		return segments

	def measure_segment_length(self, pixels, ends, junctions, shape):
		r"""
		Measure how long a segment is.

		Measured along the pixels from one end to the other, and from the junctions
		the segment hangs on rather than from its own first pixel, so that the length
		of a side branch is the distance from the fork to its tip.

		This is the one place a length is measured. The pruning compares it against
		its threshold and the export shows it, so if the two were measured
		differently, "branches shorter than 50" would mean something other than the
		length on screen.

		\param pixels: The pixels of the segment.
		\param ends: The ends of the segment, the loose ones first if there are any.
			Empty for a segment that closes into a ring, which is measured all the
			way around instead.
		\param junctions: The junctions the segment touches, mapped to one pixel each.
		\param shape: The shape of the skeleton image.
		\return: The length of the segment in pixels.
		"""
		measured = set(pixels) | set(junctions.values())

		if not ends:
			# A crack that closes into a ring has no end to start at and none to stop
			# at, so the way to the furthest pixel would only reach halfway around it.
			# Cutting the ring open at one pixel leaves a piece of line, and hanging
			# that pixel back on both ends closes it again, so every step is counted
			# exactly once.
			cut = next(iter(pixels))
			opened = self.pixel_graph(measured - {cut}, shape)
			around = self.furthest_chain(opened, self.neighbors_within(cut, measured, shape)[0])
			return self.measure_chain_length([cut] + around + [cut])

		graph = self.pixel_graph(measured, shape)
		# Two sweeps, so that a piece running between two forks is measured from the
		# one to the other and not only up to the far one: starting at an end of the
		# segment itself leaves the fork behind the start uncounted. Where a segment
		# has a loose end, both sweeps end up on the same way and nothing changes.
		return self.measure_chain_length(self.furthest_chain(graph, self.furthest_chain(graph, ends[0])[-1]))

	def measure_chain_length(self, chain):
		r"""
		Measure how long a chain of neighboring pixels is.

		Counting the pixels is not a length: a slanted line is drawn as a staircase,
		and a step across the diagonal covers about sqrt(2) pixels, not one. Adding
		the steps up with their exact geometric size (Freeman) fixes that but
		overshoots the other way by up to 8 %, because the staircase itself is longer
		than the line it stands for - it runs along two sides of a triangle instead of
		the hypotenuse.

		How much staircase there is can be read off the number of direction changes,
		which is why the corners are subtracted; the two step weights sit a little
		below their geometric values for the same reason. The three together are set
		so that the error cancels out over all directions a line can run in. That is
		what matters here: a crack runs through many directions, and only an error
		that averages to zero stops adding up along it. The price is the one case
		where the length would be known exactly - a run straight along a row or column
		comes out about 2 % short - and that case does not survive a real crack, which
		never stays on the grid for long.

		Every step still adds at least STRAIGHT_WEIGHT - CORNER_WEIGHT, so a longer
		chain can never come out shorter than a piece of it and the pruning threshold
		keeps its meaning.

		\param chain: The pixels in the order they are passed, as returned by
			furthest_chain().
		\return: The length of the chain in pixels.
		"""
		straight = diagonal = corners = 0
		last_step = None
		for first, second in zip(chain, chain[1:]):
			step = (second[0] - first[0], second[1] - first[1])
			if step[0] == 0 or step[1] == 0:
				straight += 1
			else:
				diagonal += 1
			if last_step is not None and step != last_step:
				corners += 1
			last_step = step
		return STRAIGHT_WEIGHT * straight + DIAGONAL_WEIGHT * diagonal - CORNER_WEIGHT * corners

	def measure_skeleton_length(self, skeleton):
		r"""
		Measure the total length of all the lines the skeleton consists of.

		This is the length of the crack as it is exported: every line of the skeleton
		counts, the side branches that survived the cleaning included. What it says
		about the crack is the same as counting the pixels used to say, only that a
		slanted line is no longer measured too short.

		The fork areas belong to no segment (see find_branch_segments), so summing the
		segments alone would lose them. Measuring every segment on to the middle of
		the fork it hangs on closes that gap: the middle is where the branches meet,
		so that is the point each of them runs to, and each piece in between is
		counted once, by the one branch it belongs to. Leaving it out is not a
		rounding error - it costs a few pixels per fork, on a frayed crack with twenty
		forks around 6 % of the length.

		\param skeleton: A binary skeletonized image.
		\return: The total length in pixels.
		"""
		binary = np.asarray(skeleton) > 0
		shape = binary.shape
		junction_labels, _ = label(self.find_junction_zones(binary), structure=CONNECTIVITY_8)

		pixels_per_junction = {}
		for row, col in zip(*np.where(junction_labels)):
			pixels_per_junction.setdefault(int(junction_labels[row, col]), set()).add((int(row), int(col)))

		# How far every pixel of a fork area is from its middle, measured inside the
		# area. Done once per fork, because several segments meet at the same one.
		reach = {junction: self.distances_from(self.pixel_graph(pixels, shape),
											   self.junction_center(pixels, shape))
				 for junction, pixels in pixels_per_junction.items()}

		total = 0.0
		for segment in self.find_branch_segments(binary):
			total += segment["length"]
			for junction, pixel in segment["junctions"].items():
				total += reach[junction][pixel]
		return total

	def junction_center(self, pixels, shape):
		r"""
		Pick the pixel in the middle of a fork area, the one none of its pixels is far
		from. That is where the branches meet, so it is the point their lengths are
		measured to.

		\param pixels: The pixels of one fork area.
		\param shape: The shape of the skeleton image.
		\return: The (row, col) pixel in the middle.
		"""
		graph = self.pixel_graph(pixels, shape)
		# The pixel itself breaks a tie, so that the same fork always gives the same
		# middle and a length cannot depend on the order the pixels came in.
		return min(pixels, key=lambda pixel: (max(self.distances_from(graph, pixel).values()), pixel))

	def pixel_graph(self, pixels, shape):
		r"""
		Build a graph of neighboring pixels, weighted with the distance between them.

		\param pixels: The pixels to connect.
		\param shape: The shape of the skeleton image.
		\return: A dictionary mapping a pixel to a list of (neighbor, distance) pairs.
		"""
		graph = {}
		for pixel in pixels:
			graph[pixel] = [(neighbor, 1.0 if neighbor[0] == pixel[0] or neighbor[1] == pixel[1] else DIAGONAL_STEP)
							for neighbor in self.neighbors_within(pixel, pixels, shape)]
		return graph

	def neighbors_within(self, pixel, pixels, shape):
		r"""
		List the neighbors of a pixel that belong to a given set of pixels.

		\param pixel: The (row, col) pixel to look around.
		\param pixels: The set of pixels a neighbor has to belong to.
		\param shape: The shape of the skeleton image.
		\return: A list of neighboring pixels.
		"""
		row, col = pixel
		return [(row + row_offset, col + col_offset)
				for row_offset, col_offset in NEIGHBOR_OFFSETS
				if 0 <= row + row_offset < shape[0] and 0 <= col + col_offset < shape[1]
				and (row + row_offset, col + col_offset) in pixels]

	def find_adjacent_junctions(self, pixel, junction_labels, shape):
		r"""
		Find the junctions a segment pixel is attached to.

		Usually there is one, but two forks can sit so close to each other that the
		pixel between them touches both.

		\param pixel: The (row, col) pixel to look around.
		\param junction_labels: The labelled fork areas of the skeleton.
		\param shape: The shape of the skeleton image.
		\return: A dictionary mapping the label of every adjoining junction to one of
			its pixels.
		"""
		row, col = pixel
		junctions = {}
		for row_offset, col_offset in NEIGHBOR_OFFSETS:
			neighbor = (row + row_offset, col + col_offset)
			if 0 <= neighbor[0] < shape[0] and 0 <= neighbor[1] < shape[1] and junction_labels[neighbor]:
				junctions.setdefault(int(junction_labels[neighbor]), neighbor)
		return junctions

	def is_removable_pixel(self, skeleton, pixel):
		r"""
		Check whether a pixel can be dropped without tearing the skeleton apart.

		A pixel may go when its set neighbors still hang together without it, which
		is the case if they form a single group. A real junction has one group per
		branch around it and is therefore kept, while the pixel left over where a
		removed branch used to fork off sits beside the line and has only one.

		\param skeleton: A binary skeletonized image.
		\param pixel: The (row, col) pixel to test.
		\return: True if the pixel is not needed to hold the skeleton together.
		"""
		return self.count_neighbor_groups(skeleton, pixel) <= 1

	def remove_leftover_junctions(self, skeleton, candidates):
		r"""
		Drop what a removed side branch leaves behind at the fork it grew out of.

		The fork is not part of the branch, so once the branch is gone the pixels
		that led into it are still there and sit on the line as a small stub.
		Repeated until nothing changes, because a fork covers two or three pixels
		that only become removable one after the other.

		\param skeleton: A binary skeletonized image, modified in place.
		\param candidates: The pixels to check, normally the fork areas.
		\return: The skeleton without the leftover stubs.
		"""
		removed_one = True
		while removed_one:
			removed_one = False
			for pixel in candidates:
				if skeleton[pixel] and self.is_removable_pixel(skeleton, pixel):
					skeleton[pixel] = 0
					removed_one = True
		return skeleton

	def remove_small_components(self, skeleton, max_length):
		r"""
		Remove the parts of the skeleton that are too short as a whole.

		A crack lying on its own is not a branch of anything, so the rules for
		branches do not apply to it and there is nothing it could be measured
		against. It is measured end to end instead and drops out when the whole of it
		is shorter than the threshold, which is what clears the specks and short
		strokes the detection leaves lying around the real crack.

		\param skeleton: A binary skeletonized image, modified in place.
		\param max_length: Parts shorter than this are removed completely.
		\return: True if anything was removed.
		"""
		components, component_count = label(np.asarray(skeleton) > 0, structure=CONNECTIVITY_8)
		segments = self.find_branch_segments(skeleton)
		graph = self.build_segment_graph(segments)

		# Which part of the image a segment (and with it every node on it) belongs to.
		lengths = {}
		component_of_node = {}
		for segment in segments:
			component = int(components[next(iter(segment["pixels"]))])
			# A part without any fork consists of a single segment and is not in the
			# graph at all, so its own length has to count as well.
			lengths[component] = max(lengths.get(component, 0.0), segment["length"])
			for node in self.segment_nodes(segment):
				component_of_node[node] = component

		# The length of a branched part is the longest way through it, found with the
		# same double sweep as the main endpoints.
		visited = set()
		for node in graph:
			if node in visited:
				continue
			distances = self.distances_from(graph, node)
			visited.update(distances)
			furthest = max(distances.items(), key=lambda entry: entry[1])[0]
			spread = self.distances_from(graph, furthest)
			component = component_of_node[node]
			lengths[component] = max(lengths.get(component, 0.0), max(spread.values()))

		too_short = [component for component in range(1, component_count + 1)
					 if lengths.get(component, 0.0) < max_length]
		if not too_short:
			return False
		skeleton[np.isin(components, too_short)] = 0
		return True

	def remove_small_branches(self, skeleton, max_branch_length, main_endpoints):
		r"""
		Remove short side branches from the skeleton.

		A side branch is a segment that hangs on exactly one junction and ends in a
		loose end. Only those are considered, and each of them is removed as a whole
		or not at all. Everything that carries a crack itself stays untouched: the
		pieces between two junctions and the segments ending in a main endpoint.

		A crack lying on its own has no branches and is measured end to end instead
		(see remove_small_components), so that the short strokes left around the real
		crack can be cleared with the same threshold.

		That distinction is the point of this method. Walking away from an endpoint
		and deleting pixels along the way, as it used to do, shortened every long
		branch by the threshold on each run, so cleaning repeatedly ate up the
		skeleton instead of only clearing the branches off it.

		\param skeleton: A binary skeletonized image.
		\param max_branch_length: Side branches shorter than this are removed.
		\param main_endpoints: The endpoints marking the ends of the main lines; the
			segments ending there are kept whatever their length.
		\return: The cleaned skeleton image with the short side branches removed.
		"""
		main_points = np.asarray(main_endpoints if main_endpoints is not None else []).reshape(-1, 2)
		protected = {(int(row), int(col)) for row, col in main_points}

		cleaned = np.asarray(skeleton).copy()
		# Parts of the skeleton that are too short on their own go first; afterwards
		# only branches of the remaining cracks are left to look at.
		self.remove_small_components(cleaned, max_branch_length)
		# Removing a branch can turn the twig it grew on into a side branch itself,
		# so this runs until nothing is left to remove. That way one click does the
		# whole job and clicking again provably changes nothing.
		while self.remove_side_branch_layer(cleaned, max_branch_length, protected):
			pass
		return cleaned

	def remove_side_branch_layer(self, skeleton, max_branch_length, protected):
		r"""
		Remove every side branch that is currently too short, one round.

		\param skeleton: A binary skeletonized image, modified in place.
		\param max_branch_length: Side branches shorter than this are removed.
		\param protected: The endpoints whose segments have to be kept.
		\return: True if anything was removed, False if there was nothing to do.
		"""
		# Taken before anything is removed: afterwards a fork that lost a branch is
		# no longer recognisable as one, and its leftovers would go unnoticed.
		junction_zones = self.find_junction_zones(skeleton)

		removed = []
		for segment in self.find_branch_segments(skeleton):
			is_side_branch = len(segment["junctions"]) == 1 and len(segment["end_points"]) == 1
			if not is_side_branch:
				continue
			if segment["end_points"][0] in protected:
				continue
			if segment["length"] >= max_branch_length:
				continue
			removed.extend(segment["pixels"])

		if not removed:
			return False
		self.remove_pixels(skeleton, removed, junction_zones, protected)
		return True

	def remove_pixels(self, skeleton, pixels, junction_zones, protected=frozenset()):
		r"""
		Take pixels out of the skeleton and tidy up the fork they hung on.

		\param skeleton: A binary skeletonized image, modified in place.
		\param pixels: The pixels to remove.
		\param junction_zones: The fork areas as they were before the removal.
		\param protected: Pixels the cleanup has to leave alone.
		\return: The skeleton without those pixels.
		"""
		for pixel in pixels:
			skeleton[pixel] = 0
		# Only pixels of a fork area are up for the cleanup, so nothing can be eaten
		# away further down the line, and never a main endpoint.
		candidates = {pixel for pixel in zip(*(axis.tolist() for axis in np.where(junction_zones)))
					  if pixel not in protected}
		return self.remove_leftover_junctions(skeleton, candidates)

	# def find_longest_path(self, skeleton):
	# 	G = nx.Graph()
	# 	rows, cols = np.where(skeleton > 0)
	#
	# 	for r, c in zip(rows, cols):
	# 		for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
	# 			nr, nc = r + dr, c + dc
	# 			if (nr, nc) in zip(rows, cols):
	# 				G.add_edge((r, c), (nr, nc), weight=1)
	#
	# 	end_points = list(zip(*np.where(self.find_end_points(skeleton))))
	# 	if len(end_points) < 2:
	# 		return []
	#
	# 	longest_path = []
	# 	max_length = 0
	#
	# 	for i in range(len(end_points)):
	# 		for j in range(i + 1, len(end_points)):
	# 			try:
	# 				path = nx.shortest_path(G, source=end_points[i], target=end_points[j], weight='weight')
	# 				if len(path) > max_length:
	# 					max_length = len(path)
	# 					longest_path = path
	# 			except nx.NetworkXNoPath:
	# 				continue
	#
	# 	return longest_path
	#
	# def extract_main_skeleton(self, skeleton):
	# 		longest_path = self.find_longest_path(skeleton)
	# 		new_skeleton = np.zeros_like(skeleton)
	#
	# 		for point in longest_path:
	# 			new_skeleton[point] = 1
	#
	# 		return new_skeleton
