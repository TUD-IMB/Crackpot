# Measuring the Skeleton Length

This page describes how the skeleton length in the results export stage is measured.
Entering the stage calls `MainWindow.calculate_crack_properties()`, which hands the skeleton of every image to
`SkeletonProcessor.measure_skeleton_length()` and adds the lines drawn by hand.
The summary for users is in the handbook, section *How the Skeleton Length is Measured*
([src/crackpot/resources/docs/README.md](../src/crackpot/resources/docs/README.md)).

The length matters beyond its own column in the export: the mean crack width is the crack area divided by it,
so every error in the length turns into an error of the width.
Measuring it takes three decisions: which lines count, how a chain of pixels is turned into a length,
and how the pieces of a branched skeleton are put together.

The figures below use the same notation as [SkeletonCleaning.md](SkeletonCleaning.md): `o` marks a skeleton pixel,
`·` the background.
They and all numbers on this page are the output of the `SkeletonProcessor` methods named in them.

## 1. What is Measured

The skeleton length is the total length of all lines of the cleaned skeleton, including the side branches that
survived the cleaning, plus the lines drawn by hand.
It is not the length of the longest way through the crack.

The reason is the mean width.
The crack area counts every pixel of the mask, the area of the branches included.
Dividing it by the longest way only would make the mean width systematically too large;
only the total length refers to the same set of lines as the area.

The lines drawn by hand (`created_lines`) are straight lines between two points,
so their length is simply the distance between their ends.
It is added on top of the length of the automatic skeleton.

Both lengths are in pixels. The calibration turns them into millimeters:

```
skeleton_length_mm = (automatic skeleton + lines drawn by hand) * resolution
crack_area_mm2     = crack pixels * resolution²
crack_width_mm     = crack pixels / (automatic skeleton + lines drawn by hand) * resolution
```

`resolution` is the value in mm per pixel confirmed in the calibration stage.

## 2. Measuring a Chain of Pixels

The skeleton draws a slanted line as a staircase.
The example is a line running 12 pixels to the right and 5 up, whose true length is exactly 13:

```
· · · · · · · · · · · o o
· · · · · · · · · o o · ·
· · · · · · o o o · · · ·
· · · · o o · · · · · · ·
· · o o · · · · · · · · ·
o o · · · · · · · · · · ·
```

It consists of 13 pixels, joined by 7 straight and 5 diagonal steps, and changes direction 10 times.
There are three ways to turn this into a length:

- **Counting the pixels** gives 13 here, but a diagonal step covers about 1.41 pixels and is still counted as one.
  Along a line at 45 degrees, almost 30 % of the length is lost this way.
- **Adding up the steps** with their geometric size, 1 and √2, gives 14.071.
  This is the chain code length of Freeman (1961).
  It overshoots, because the staircase is longer than the line it stands for:
  it runs along two sides of a small triangle instead of along its hypotenuse.
- **Weighting the steps and subtracting the corners**, as `measure_chain_length()` does, gives 12.980:

```
length = 0.980 * straight steps + 1.406 * diagonal steps - 0.091 * corners
```

The number of direction changes tells how much staircase a chain contains, which is why the corners are subtracted.
The two step weights sit slightly below their geometric values for the same reason.
The three weights are the ones of Vossepoel and Smeulders (1982); they are the module constants
`STRAIGHT_WEIGHT`, `DIAGONAL_WEIGHT` and `CORNER_WEIGHT` in `skeletonprocessor.py`, together with the full references.

The weights are chosen so that the error cancels out over all directions a line can run in.
This is what matters for a crack: it runs through many directions, and only an error that averages out
does not add up along its course.
The price is the one case in which counting would be exact: a line running along a row or a column comes out 2 % short.
A real crack rarely follows the grid for long, so this carries little weight.
For straight lines of about 200 pixels in different directions, the three methods give:

| Direction | True length | Counting the pixels | Adding up the steps | Estimator |
|---|---|---|---|---|
| 0° | 200.0 | 201 (+0.5 %) | 200.0 (+0.0 %) | 196.0 (-2.0 %) |
| 10° | 200.1 | 198 (-1.0 %) | 211.5 (+5.7 %) | 201.6 (+0.8 %) |
| 22.5° | 200.4 | 186 (-7.2 %) | 216.9 (+8.2 %) | 200.1 (-0.1 %) |
| 30° | 199.8 | 174 (-12.9 %) | 214.4 (+7.3 %) | 198.9 (-0.5 %) |
| 45° | 199.4 | 142 (-28.8 %) | 199.4 (+0.0 %) | 198.2 (-0.6 %) |

Every step adds at least 0.980 - 0.091 = 0.889 pixels, so a longer chain can never come out shorter than a piece of it.
The cleaning relies on this, as it compares the same lengths against its threshold.

A detailed comparison of these and other estimators, with the error of each plotted over the direction of the line,
is on the blog of Cris Luengo: <https://www.crisluengo.net/archives/310/>.

## 3. Walking Along a Segment

A skeleton is rarely a single chain.
`measure_skeleton_length()` therefore cuts it into segments with `find_branch_segments()`,
the same segments the cleaning works with (see [SkeletonCleaning.md](SkeletonCleaning.md), section 2),
and measures each one with `measure_segment_length()`.

To measure a segment, its pixels have to be put into order first.
`pixel_graph()` connects every pixel with its neighbors, weighted with the geometric distance of 1 or √2,
and `furthest_chain()` follows the longest way through this graph.
It does so twice, starting the second time from where the first one ended,
so that a piece between two forks is measured from one fork to the other.
The chain found this way is then measured with the three weights of section 2.
Finding the way and measuring it are kept apart on purpose:
the way needs the true distances, the length needs the estimator.

A segment starts at the pixel of the fork area it touches, not at its own first pixel,
so a side branch is measured from its tip up to the fork area.

A crack that closes into a ring without any fork has no end to start at.
The longest way would then only reach halfway around.
`measure_segment_length()` cuts such a ring open at one pixel, measures the remaining line
and hangs the removed pixel back on both ends, so that every step is counted exactly once.
A ring with a radius of 40 pixels, whose true length is 251.3, is measured as 251.8 (+0.2 %);
counting its 228 pixels would give -9.3 %.

## 4. Forks

The fork areas (`+` below) belong to no segment: they are cut out to separate the branches.
Adding up the segments alone would lose them, a few pixels for every fork.
`measure_skeleton_length()` therefore continues every segment from the fork area pixel it touches
to the middle of the area (`●`).
The middle is where the branches meet, so it is the point each of them runs to,
and every piece in between is counted once, by the branch it belongs to.

```
· · · · · · · · · · · · ·
· · · · · · · · · · · · ·
· a a a a + ● + b b b b ·
· · · · · · + · · · · · ·
· · · · · · c · · · · · ·
· · · · · · c · · · · · ·
· · · · · · c · · · · · ·
· · · · · · c · · · · · ·
· · · · · · · · · · · · ·
```

`junction_center()` takes the pixel of the area that no other pixel of it is far from,
and the pixel coordinates break a tie, so that the same fork always has the same middle.
The distance inside the area is measured with the geometric step sizes, as the area is only a few pixels large.

The cleaning compares a side branch without the part inside the fork area (see [SkeletonCleaning.md](SkeletonCleaning.md),
section 3), so a branch contributes about one pixel more to the exported length than it is compared with.

## 5. Limits

- The skeleton ends about half a crack width before each end of the mask, because it runs along the middle of the crack.
  Every crack is therefore measured about one crack width too short.
  For a long, thin crack this is negligible; for a short, wide one it is not.
  A straight crack 200 pixels long and 21 pixels wide is measured as 177.6 pixels.
- The length is that of the cleaned skeleton, so it depends on the threshold chosen for
  **Remove Branches Shorter Than (px)**. Spurs that are not removed count as crack.
- Lines drawn by hand are added on top of the automatic skeleton without comparing the two.
  A line drawn along a part of the crack that the automatic skeleton already covers is counted twice.
- Lines along a row or a column of the image come out 2 % short (section 2).
