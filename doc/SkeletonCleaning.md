# Removing Short Skeleton Branches

This page describes what happens behind **Remove Branches Shorter Than (px)** in the skeleton extraction stage.
The button calls `MainWindow.clean_skeleton_branches()`, which determines the ends of the main lines and hands the
skeleton to `SkeletonProcessor.remove_small_branches()`.
The summary for users is in the handbook, section *How Short Branches are Removed*
([src/crackpot/resources/docs/README.md](../src/crackpot/resources/docs/README.md)).

The skeleton of a real crack rarely consists of clean lines alone.
An irregular crack edge leaves short spurs that stick out of the line without being a crack of their own.
The cleaning takes these spurs off, and only these.
Every branch is either kept as a whole or removed as a whole, and the crack itself is never shortened,
so pressing the button again with the same threshold changes nothing.

The figures below show the steps on small examples: `o` marks a skeleton pixel, `·` the background.
They are the output of the `SkeletonProcessor` methods named in them.

## 1. Finding the Forks

Every skeleton pixel is examined together with the eight pixels around it.
`count_neighbors()` counts how many of them belong to the skeleton: one neighbor means a loose end,
two a piece of line, three or more a possible fork.

Three neighbors are not enough to be sure, though.
The pixels right next to a fork have three or four neighbors as well, although nothing branches off there,
as the pixels around the fork of the T junction show.
The same happens at the corner of every step of a staircase, which is how a slanted line is drawn on the pixel grid.
For every pixel with three or more neighbors, `count_neighbor_groups()` therefore reads the eight surrounding
pixels as a ring, clockwise in the order of `NEIGHBOR_OFFSETS`, and counts every place where background turns
into skeleton as the start of a new group.
A real fork has one group for every branch leaving it, so three or more.
The neighbors of the pixels beside it touch each other and form only two groups.
`find_branch_points()` marks the pixels with three or more groups as forks (`●`),
`find_end_points()` the pixels with exactly one neighbor as loose ends.

```
T junction        Adjacent          X crossing
                  forks

1. count_neighbors: how many of the 8 surrounding pixels are set

· · · · · · ·     · · · · 1 · ·     · · · 1 · · ·
· · · · · · ·     · · · · 2 · ·     · · · 2 · · ·
· · · · · · ·     · · · · 4 · ·     · · · 4 · · ·
1 2 3 3 3 2 1     1 2 3 4 4 3 1     1 2 4 4 4 2 1
· · · 4 · · ·     · · · 4 · · ·     · · · 4 · · ·
· · · 2 · · ·     · · · 2 · · ·     · · · 2 · · ·
· · · 1 · · ·     · · · 1 · · ·     · · · 1 · · ·

2. count_neighbor_groups: separate groups around pixels with 3+ neighbors

· · · · · · ·     · · · · o · ·     · · · o · · ·
· · · · · · ·     · · · · o · ·     · · · o · · ·
· · · · · · ·     · · · · 2 · ·     · · · 2 · · ·
o o 2 3 2 o o     o o 2 3 3 2 o     o o 2 4 2 o o
· · · 2 · · ·     · · · 2 · · ·     · · · 2 · · ·
· · · o · · ·     · · · o · · ·     · · · o · · ·
· · · o · · ·     · · · o · · ·     · · · o · · ·

3. find_branch_points: forks are pixels with 3+ groups

· · · · · · ·     · · · · o · ·     · · · o · · ·
· · · · · · ·     · · · · o · ·     · · · o · · ·
· · · · · · ·     · · · · o · ·     · · · o · · ·
o o o ● o o o     o o o ● ● o o     o o o ● o o o
· · · o · · ·     · · · o · · ·     · · · o · · ·
· · · o · · ·     · · · o · · ·     · · · o · · ·
· · · o · · ·     · · · o · · ·     · · · o · · ·
```

What a group is can be seen at the T junction from above.
`x` is the pixel looked at, and the ring lists its eight neighbors clockwise, starting at the top:

```
Fork of the T junction        Pixel left of the fork

· · ·                         · · ·
o x o                         o x o
· o ·                         · · o

ring: · · o · o · o ·         ring: · · o o · · o ·
      3 groups → fork               2 groups → no fork
```

A group is a run of neighbors that follow each other on the ring without background in between.
They touch each other and lead away in the same direction, so they belong to the same branch.
Both pixels have three neighbors, but only at the fork are all three separated by background.
Beside the fork, the right and the lower right neighbor touch and count as one group.
The ring is closed, so a run that crosses its start, from the upper left to the top neighbor, is one group as well.

## 2. Cutting the Skeleton into Segments

`find_junction_zones()` widens each fork by the skeleton pixels immediately around it (`+`).
This fork area is needed to separate the branches, which in an 8-connected line one pixel wide still touch each
other diagonally around the fork pixel.
Forks directly next to each other, such as the two in the second example above, end up in one area,
as they form a single crossing.

`find_branch_segments()` cuts out the fork areas, and the skeleton falls apart into segments:
the pieces between two forks, or between a fork and a loose end.
For every segment it records its pixels, the fork areas it touches, its loose ends and its length.
A segment that hangs on exactly one fork area and ends in a loose end is a side branch
(`a`, `b`, `c`, `e`, `h`, `i` below), and only side branches are candidates for removal.
The same segments are the unit the removal by mouse click works with (`MainWindow.delete_skeleton_segment()`).

```
· · · · · · · a a + ● + b b · · · · · · · · · ·
· · · · · · · · · · + · · · · · · · · · · · · ·
· · · · c · · · · · d · · · · · · · · · · · · ·
· · · · c · · · · · d · · · · · · · · · · · · ·
· · · · + · · · · · + · · · · · · · · · · · · ·
e e e + ● + f f f + ● + g + ● + h h h h h h h h
· · · · · · · · · · · · · · + · · · · · · · · ·
· · · · · · · · · · · · · · i · · · · · · · · ·
· · · · · · · · · · · · · · i · · · · · · · · ·
· · · · · · · · · · · · · · i · · · · · · · · ·
· · · · · · · · · · · · · · i · · · · · · · · ·
· · · · · · · · · · · · · · i · · · · · · · · ·
```

## 3. Measuring and Protecting

`measure_segment_length()` measures a segment along its pixels with the length estimator of
`measure_chain_length()`, the same one the exported skeleton length uses (see [SkeletonLength.md](SkeletonLength.md)).
A side branch is measured from its tip up to the pixel where it meets the fork area.
The part inside the fork area belongs to no segment here; `measure_skeleton_length()` adds it on top for the export,
so a branch contributes about one pixel more to the exported length than it is compared with here.
A side branch is removed if its length is strictly below the threshold.

Two kinds of segment are never removed, whatever their length:

- Segments between two forks, as they carry the crack itself.
- The two segments at the ends of the main line.

The main line is the longest way through a crack, measured along the skeleton.
`find_main_endpoints()` finds its two ends with a double sweep over the graph of segments (`build_segment_graph()`),
separately for every connected part of the image.
`clean_skeleton_branches()` determines them once, before the cleaning starts.

A part of the skeleton that is shorter than the threshold as a whole, such as a short stroke left over by the
detection, is no branch of anything. `remove_small_components()` measures every connected part along its longest
way and removes those shorter than the threshold completely. This runs once, before the side branches are looked at.

## 4. Removing in Rounds

`remove_side_branch_layer()` removes all side branches that are currently too short, in one round:
it collects them first and removes them afterwards.
Removing each one straight away would change the forks the others hang on while they are still being looked at,
and the result would depend on the order the segments came in.
`remove_pixels()` then tidies up the pixels a removed branch leaves behind in its fork area
(`remove_leftover_junctions()`), without ever touching a main endpoint.

Removing branches can turn what they grew on into a side branch itself.
In the example, `d` connects two forks at first and is therefore kept.
Once `a` and `b` are gone, the upper fork no longer exists, so `d` now ends loose and is removed in the second round.
`remove_small_branches()` therefore repeats the rounds until one removes nothing.

With a threshold of 4 px, the example is cleaned as follows:

| Segment | Kind | Length (px) | Result |
|---|---|---|---|
| a, b, c | side branch | 1.96 | removed in round 1 |
| d | between two forks | 2.94 | kept in round 1, removed in round 2 as a side branch |
| e, h | ends of the main line | 2.94 and 7.84 | kept, protected |
| f, g | between two forks | 3.92 and 1.96 | kept |
| i | side branch | 4.90 | kept, not shorter than the threshold |

After round 1:

```
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · o · · · · · · · · · · · · ·
· · · · · · · · · · o · · · · · · · · · · · · ·
· · · · · · · · · · o · · · · · · · · · · · · ·
o o o o o o o o o o o o o o o o o o o o o o o o
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
```

After round 2, the final result:

```
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · · ·
· · · · · · · · · · · · · · · · · · · · · · · ·
o o o o o o o o o o o o o o o o o o o o o o o o
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
· · · · · · · · · · · · · · o · · · · · · · · ·
```

## 5. Limits

- Only two ends per crack are protected. In a network of cracks, the outer ends of the other cracks are loose ends
as well, and a branch of the network that is shorter than the threshold is removed like a spur.
- The main line is simply the longest way through the crack. If a side branch reaches further than the actual end
of the crack, the main line runs through that branch instead, and the real end becomes an ordinary side branch.
- Manually drawn skeleton lines are not part of the cleaning. They are stored separately from the skeleton image
(`created_nodes` and `created_lines` in the skeleton results of `MainWindow`), so they are neither removed nor taken
into account when deciding what counts as a side branch.
