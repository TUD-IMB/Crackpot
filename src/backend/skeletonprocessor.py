import numpy as np
from scipy.ndimage import convolve


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

	def add_skeleton(self, image_path, skeleton):
		r"""
		Store a skeletonized image associated with its image path.

		\param image_path: The file path of the image.
		\param skeleton: The skeletonized image as a NumPy array.
		"""
		self.skeletons[image_path] = skeleton

	def find_end_points(self, skeleton):
		r"""
		Detect endpoints in a skeletonized image.
		Apply a convolution kernel to identify pixels with only one connected neighbor.

		\param skeleton: A binary skeletonized image.
		\return: A boolean array marking endpoint locations.
		"""
		kernel = np.array([[1, 1, 1],
						   [1, 10, 1],
						   [1, 1, 1]])
		filtered = convolve(skeleton.astype(np.uint8), kernel)
		end_points = (filtered == 11)
		return end_points

	def find_branch_points(self, skeleton):
		r"""
		Identify branch points in a skeletonized image.
		Apply a convolution kernel to detect pixels with three or more connected neighbors.

		\param skeleton: A binary skeletonized image.
		\return: A boolean array marking branch point locations.
		"""
		kernel = np.array([[1, 1, 1],
						   [1, 10, 1],
						   [1, 1, 1]])
		filtered = convolve(skeleton.astype(np.uint8), kernel)
		branch_points = (filtered >= 13) & (skeleton == 1)
		return branch_points

	def find_main_endpoints(self, skeleton):
		r"""
		Determine the two most distant endpoints in the skeleton.
		Find all endpoints and calculate the pair with the maximum Euclidean distance.

		\param skeleton: A binary skeletonized image.
		\return: A NumPy array containing the two main endpoints.
		"""
		end_points = np.column_stack(np.where(self.find_end_points(skeleton)))
		if len(end_points) < 2:
			return end_points
		max_distance = 0
		main_endpoints = (end_points[0], end_points[1])
		for i in range(len(end_points)):
			for j in range(i + 1, len(end_points)):
				dist = np.sum((end_points[i] - end_points[j]) ** 2)
				if dist > max_distance:
					max_distance = dist
					main_endpoints = (end_points[i], end_points[j])
		return np.array(main_endpoints)

	def remove_small_branches(self, skeleton, max_branch_length, main_endpoints):
		r"""
		Remove small branches from the skeleton.
		Iterate through endpoints, trace branches, and remove those small branches shorter than
		the specified length threshold.

		\param skeleton: A binary skeletonized image.
		\param max_branch_length: The maximum length of branches to remove.
		\param main_endpoints: The two main endpoints to preserve.
		\return: The cleaned skeleton image with small branches removed.
		"""
		branch_points = self.find_branch_points(skeleton)
		end_points = self.find_end_points(skeleton)
		skeleton_copy = skeleton.copy()
		rows, cols = np.where(end_points)
		for row, col in zip(rows, cols):
			if [row, col] in main_endpoints.tolist():
				continue
			length = 0
			path = [(row, col)]
			while length < max_branch_length:
				neighbors = skeleton_copy[row - 1:row + 2, col - 1:col + 2]
				if np.sum(neighbors) == 2:
					skeleton_copy[row, col] = 0
					length += 1
					row, col = np.where(neighbors == 1)
					if len(row) == 0 or len(col) == 0:
						break
					row, col = row[0] + path[-1][0] - 1, col[0] + path[-1][1] - 1
					# if branch_points[row, col]:
					# 	break
					path.append((row, col))
				else:
					break
			if length < max_branch_length:
				for r, c in path:
					skeleton_copy[r, c] = 0
		return skeleton_copy

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


