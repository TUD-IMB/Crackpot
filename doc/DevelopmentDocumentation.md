# Development Documentation

The development documentation outlines how Crackpot is built, breaking it down into six main parts:
the **Workflow** the application leads through, **UI Development**, the **Core Functional Classes**,
the **Data Model**, **Internationalization**, and the **Code Documentation** this page is part of.

Some parts of the code are described on pages of their own:

- [SkeletonCleaning.md](SkeletonCleaning.md): how short branches are removed from the skeleton.
- [SkeletonLength.md](SkeletonLength.md): how the skeleton length is measured.
- [Packaging.md](Packaging.md): how a version is built and published on PyPI.

How to use the application is described in the handbook,
[src/crackpot/resources/docs/README.md](../src/crackpot/resources/docs/README.md).

# Workflow

Crackpot guides a set of images through five stages.
Each stage has its own page in the stacked widget `stageStack` on the right-hand side of the main window,
and `MainWindow.set_stage()` switches between them.
The top status bar shows which stages have been reached (`ProgressManager`).

| Stage | Page | What happens | Main methods |
|---|---|---|---|
| 0 Calibration | `calibrationPage` | Two points on an image with a known distance give the resolution in mm per pixel. | `upload_calibration_image()`, `calculate_pixel_distance()`, `confirm_resolution()` |
| 1 Image Upload | `uploadPage` | The images to analyze are loaded into the thumbnail list. | `upload_figures()` |
| 2 Masking | `maskingPage` | The crack area is detected automatically or drawn by hand. | `apply_model_detection()`, `draw_on_image()`, `clean_mask_patches()` |
| 3 Skeleton Extraction | `skeletonPage` | The crack mask is thinned to a line one pixel wide, cleaned and edited. | `apply_skeletonization()`, `clean_skeleton_branches()`, `create_node()`, `delete_node()` |
| 4 Results Export | `exportPage` | Length, area and mean width are computed and exported. | `calculate_crack_properties()`, `export_to_csv()` |

Entering stage 4 always computes the results anew, so they reflect the latest masks and skeletons.

# UI Development

The user interface is created with **PySide6**.
We use **Qt Designer** to set up the overall components and layout.
The components and content are then further customized and populated using code.

## Layout Design with Qt Designer

The whole main window is laid out in `src/crackpot/resources/ui/main.ui`.
Qt Designer ships with PySide6 and is started with `pyside6-designer`.
The **Object Inspector** and **Property Editor** allow adjusting the attributes of each component,
like the object name, tooltip, size, and other properties.
Widgets are named after what they are (`skeletonPage`, `nodeAddButton`), because the code refers to
every widget by its object name.

### Converting `.ui` Files to Python Files

`pyside6-uic` converts `main.ui` into the Python module `src/crackpot/frontend/ui/uimain.py`.
This module is generated: it is overwritten by every conversion and must never be edited by hand.
Every change to the layout is made in `main.ui`.
The conversion is run through `convertpyfile.py` (see *Automatic Build*), which also rewrites the
`import icon_rc` line written by `pyside6-uic` into a package import: under its bare name, the resource module is
not found once Crackpot runs as an installed package.

## Icons

The interface icons are monochrome SVG files in `src/crackpot/resources/icons`.
At runtime, `MainWindow.apply_icon_color()` repaints them in the text color of the active color scheme,
so they stay visible in both the light and the dark scheme.

Rendering SVG icons needs the Qt SVG library, which is imported explicitly in
`src/crackpot/frontend/ui/__init__.py`.
The import looks unused, but without it all icons stay blank on Windows.

### Converting `.qrc` Files to Python Files

The icons are collected in the resource file `icon.qrc`, which `pyside6-rcc` converts into
`src/crackpot/frontend/ui/icon_rc.py`.

### Icon Resources and License

The icons are taken from [Huge Icons](https://icon-sets.iconify.design/hugeicons/),
which are licensed under the MIT License, see `src/crackpot/resources/license/icon_MIT_LICENSE.txt`.

## Automatic Build

The script `src/convertpyfile.py` runs all conversions in one go:
`pyside6-uic` for the `.ui` file, `pyside6-rcc` for the `.qrc` file,
`pyside6-lupdate` to update the translation source, and `pyside6-lrelease` to compile it (see *Internationalization*).
Run it after every change to `main.ui`, `icon.qrc` or a translatable text:

```
python src/convertpyfile.py
```

The script is a development tool and not part of the installed package.
`icon_rc.py` records the file dates of the icons and therefore changes with every run;
if no icon was changed, that change can be discarded.

# Core Functional Classes

The code lives in the package `crackpot` under `src/crackpot`, split into a backend without any user interface
and a frontend. Below is an introduction of each module.

## Entry Point

**`main.py`**: Starts the application.
Before the main window is created, it replaces missing standard streams (the `crackpot` command runs without a
console on Windows) and gives the application its own identity in the Windows taskbar.

**`version.py`**: The version number and release date.
It is the only place the version is written: `pyproject.toml` reads it when the package is built,
and the About dialog shows it.

## Backend

**`edgedetection.py`**: The automatic crack detection, a pre-trained Keras model in
`src/crackpot/resources/model/my_model.keras`.
`EdgeDetection.detect_edges()` scales an image down to the 256 × 256 pixels the model expects and the
predicted mask back up to the image size.
TensorFlow is an optional dependency (the `tensorflow` extra, see [Packaging.md](Packaging.md)),
so it is imported only when the model is actually loaded;
`is_detection_available()` checks whether it is installed without importing it.
`dice_coef()`, `dice_coef_loss()` and `IOU()` are only needed to load the model, which was trained with them.

**`maskprocessor.py`**: Removes small, disconnected patches from a crack mask, which are usually noise of the
detection rather than cracks.

**`skeletonprocessor.py`**: Everything that works on the skeleton:
finding loose ends and forks, cutting the skeleton into segments, measuring lengths, finding the main line of a
crack and removing short side branches.
How short branches are removed is described step by step in [SkeletonCleaning.md](SkeletonCleaning.md),
how lengths are measured in [SkeletonLength.md](SkeletonLength.md).

## Frontend

**`mainwindow.py`**: The main window. It holds the data of the session, connects the widgets to their
actions and implements the stages: drawing on the mask, editing the skeleton, zooming, the calculation of the
results, the export, and saving and loading projects.

**`progressmanager.py`**: The status bar at the top, which marks the current stage and the stages reached.

**`documentationdialog.py`**: Shows the handbook inside the application, in the current language.
It renders the Markdown file with `QTextBrowser`, so it works offline.

**`aboutdialog.py`**: The About dialog with the version, the authors, the copyright and the license.

**`ui/`**: The modules generated from `main.ui` and `icon.qrc` (see *UI Development*).

## Utilities

**`utils/utils.py`**: `resource_path()` locates files under `src/crackpot/resources`,
both in an installed package and in a standalone build made with PyInstaller.

# Data Model

## Session Data

The results of a session are kept in three dictionaries of `MainWindow`, each keyed by the path of an image:

- **`prediction_results`**: The crack mask of every image, a 2D array with values from 0 (background) to 1 (crack).
- **`skeleton_results`**: The skeleton of every image, with the keys
  - `skeleton`: the automatic skeleton as a binary image, addressed as (row, column);
  - `branch_points`, `end_points`: the forks and loose ends of `skeleton`, derived from it;
  - `created_nodes`, `created_lines`: the points and lines drawn by hand, as (x, y) coordinates and pairs of them.
    They are kept apart from the skeleton image, so the automatic cleaning never touches them
    (see [SkeletonCleaning.md](SkeletonCleaning.md));
  - `longest_path`: the largest connected part of the skeleton, kept under this name for older project files;
  - `selected_points`: kept for older project files as well.
- **`crack_results`**: What stage 4 computes per image: `crack_pixels`, `crack_area_mm2`,
  `skeleton_length_px`, `skeleton_length_mm` and `crack_width_mm`.
  The length is that of the automatic skeleton plus the lines drawn by hand;
  the mean width is the crack area divided by that length (see [SkeletonLength.md](SkeletonLength.md)).

## Display and Coordinates

Two coordinate orders are in use:
image arrays such as the mask and the skeleton are addressed as (row, column),
while positions on screen and the points drawn by hand are (x, y).
Every conversion between the two swaps the order.

The image is always kept in its full resolution.
Masks, skeletons and markers are drawn into the full resolution image,
and `render_current_view()` scales the result to the current `zoom_factor` only for display.
Scaling down first would destroy the skeleton lines, which are one pixel wide.

Everything else is derived from the zoom factor:

- `convert_to_image_coords()` turns a mouse position into image coordinates with it.
- `overlay_line_scale()` gives the number of image pixels per screen pixel, and `overlay_size_in_pixels()` converts
  a size meant for the screen into the size to draw with.
  The skeleton points and the width of the skeleton lines therefore keep their size on screen at every zoom level.
  The brush and the calibration points are sizes in the image instead and grow with the zoom,
  and so does the cursor circle that shows them (`cursor_circle_size()`).
- `node_click_tolerance()` gives how far a click may miss a point or a line and still count as a hit.
  It follows the radius the points are drawn with, so the cursor circle shows the area a click reaches.
  Placing a new point (`snap_to_skeleton()`) and deleting a line (`find_clicked_segment()`) use the same tolerance.

## Project Files

**File → Export Project** writes a session into a `.crackpot` file (`MainWindow.export_project()`),
and **Import Project** restores it (`import_project()`), including the stage it was saved in.
A project file is JSON:

- The images are referenced by their path relative to the project file, not copied into it.
- Masks and skeleton images are stored as PNG, base64-encoded, instead of as a list of pixel values.
- `branch_points` and `end_points` are not stored; they are derived from the skeleton again on import.
- Result keys that were renamed since an older version are translated back on import
  (`_RENAMED_CRACK_RESULT_KEYS`), so older project files keep loading.

## Stored Settings

Choices that should survive a restart are kept with `QSettings` under the organization
"Institut für Massivbau, TU Dresden" and the application "Crackpot":

| Key | Meaning | Set in |
|---|---|---|
| `language` | `english` or `german` | Setting → Language |
| `cursor_color` | Color of the cursor circle | Setting → Colors |
| `skeleton_color` | Color of the automatic skeleton | Setting → Colors |
| `manual_skeleton_color` | Color of the points and lines drawn by hand | Setting → Colors |

The defaults of the colors are in `DEFAULT_COLORS` at the top of `mainwindow.py`.

# Internationalization (i18n)

In the `.ui` file, any widget property marked as translatable, and in the code any string enclosed in
`self.tr()`, is flagged for translation.
We use **Qt Linguist** to translate the application into German.

## Generate Translation Files

`pyside6-lupdate` scans `main.ui` and all Python files of the frontend for translatable texts and merges them
into the translation source `src/crackpot/resources/translations/crackpot_de.ts`.
`convertpyfile.py` does this as one of its steps.
New texts then appear as unfinished entries and are translated in **Qt Linguist** (`pyside6-linguist`).

Texts that no longer exist stay in the `.ts` file, marked as vanished.
To drop them, run `pyside6-lupdate` once by hand with the option `-no-obsolete` placed before `-ts`.

## Release and Use with QTranslator

`pyside6-lrelease` compiles the `.ts` file into `crackpot_de.qm`, which is what the application loads.
`MainWindow.switch_language()` installs or removes a `QTranslator` with this file and retranslates all widgets,
so the language changes without a restart.

## Handbook

The handbook is not part of the translation files.
It exists as two Markdown files, `README.md` and `README_de.md` in `src/crackpot/resources/docs`,
and a change to one of them has to be made in the other as well.

# Code Documentation

## Docstrings

Classes and methods are documented with docstrings in the following form:

```
def create_node(self, clicked_pos, connect_to_previous=True):
	r"""
	Create a skeleton node at the clicked position and optionally connect it to the previous node.

	\param clicked_pos: The QPoint position where the user clicked.
	\param connect_to_previous: Boolean indicating whether to connect to the last node.
	"""
```

The `r` in front of the quotes keeps Python from reading `\param` as an escape sequence.
`\param` and `\return` are Doxygen commands, which turn into a table of parameters in the generated documentation.

## Pages in the `doc` Folder

The handbook tells users what a function does.
Where the reasoning behind it needs more room, the handbook keeps a short summary
and a page in the `doc` folder goes through the details, like [SkeletonCleaning.md](SkeletonCleaning.md)
and [SkeletonLength.md](SkeletonLength.md).
These pages are in English only and are not part of the installed package.
Their figures and numbers are computed with the methods they describe,
so they can be checked against the code again after it has changed.

## Doxygen

This documentation is generated with [Doxygen](https://www.doxygen.nl) from the docstrings, the top-level
`README.md` and the pages in the `doc` folder.
The settings are in the `Doxyfile` in the repository root. With Doxygen and Graphviz installed, run

```
doxygen Doxyfile
```

and open `Documentation/html/index.html`.
Graphviz draws the call graphs of every method.
The `Documentation` folder is generated and therefore excluded from version control.
