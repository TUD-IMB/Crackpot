# Crackpot - Crack width evaluation based on crack pictures


## Introduction

This projects aims to automatically extract the crack properties from photographs of cracks.
It supports batch processing of images through several stages, 
mainly focusing on crack region detection, crack skeleton extraction, and mean crack width calculation based on calibrated resolution.
Manual edit tools are available at specific stages where refinement of the automated results is necessary.

The workflow consists of the following stages:
- [Calibration Stage](#calibration-stage)
- [Image Upload Stage](#image-upload-stage)
- [Crack Detection Stage](#crack-detection-stage)
- [Mask Edit Stage](#mask-edit-stage)
- [Skeleton Extraction Stage](#skeleton-extraction-stage)
- [Results Export Stage](#results-export-stage)



## Interface Structure

The user interface consists of five main parts:

1. **Top Workflow Status Bar**: Displays the current stage within the workflow.
Six icons correspond to the six stages described earlier.  
   - White icons represent incomplete stages.
   - Green icons indicate completed stages.
   - A green-bordered icon highlights the current active stage.

2. **Right-Side Tool Panel**: Provides the available tools and operations for each stage.

3. **Bottom Thumbnail Browser**: Displays thumbnails of all loaded images.
The main image can be switched by clicking on a thumbnail or by using the left and right navigation buttons.

4. **Center Toolbar for Image Actions**: Offers tools for zooming in, zooming out, and deleting the currently displayed image.

5. **Main Image Display and Editing Area**: The central area of the interface is used to displaying and editing the selected image.


> The UI icons are sourced from [Huge Icons](https://icon-sets.iconify.design/hugeicons/), 
and are licensed under the [MIT License](./src/resources/license/icon_MIT_LICENSE.txt).


![Interface Overview](./doc/images_en/ui.png)

## Calibration Stage

This stage calculates the resolution (millimeters per pixel) required for subsequent analysis.
If the resolution is already known, it can be directly entered into the resolution field and confirmed.
Otherwise, the resolution can be calibrated by uploading an image (such as a ruler or reference object).

If image-based calibration is used, a calibration point selection tool is available in the tool panel on the right side.
By selecting two points on the uploaded image, the software will automatically calculate the number of pixels between the selected points.
After entering the actual physical distance corresponding to these points, the resolution will be computed automatically.

> When uploading an image, please ensure that the file path does not contain special characters such as `ü`, `ö`, `ä`, etc., as this may cause upload errors.

![Calibration Image](./doc/images_en/cali.png)

## Image Upload Stage

In this stage, images intended for analysis can be uploaded in batches.
After uploading, all images will appear as thumbnails in the browser at the bottom of the interface.
Clicking on a thumbnail will display the corresponding full-size image in the main viewing area.

> When uploading an image, please ensure that the file path does not contain special characters such as `ü`, `ö`, `ä`, etc., as this may cause upload errors.

![Image Upload](./doc/images_en/upload.png)


## Crack Detection Stage

In this stage, a model is used to perform crack detection on the uploaded images.
After selecting a model and proceeding to the next stage, the software will automatically generate crack masks on the uploaded images within a few seconds.

> The default model currently integrated is from [Concrete Crack Segmentation](https://github.com/Subham2901/Concrete_Crack_Segmentation),
which is licensed under the [MIT License](./src/resources/license/model_MIT_LICENSE.txt). 


![Crack Detection](./doc/images_en/model.png)

## Mask Edit Stage

Since model detection results may contain errors, the Mask Edit Stage provides the ability to manually adjust the detected crack areas.
The available editing tools include:

- Brush: Add Brush & Delete Brush
- Brush Size
- Brush Shape: Round (default) & Square
- Opacity Slider: Allow adjusting the transparency to compare between the original image (0%) and the crack mask (100%).

![Mask Edit](./doc/images_en/editmask.png)

## Skeleton Extraction Stage

In this stage, the skeleton structure of the detected cracks is extracted by clicking the **Skeletonization** button.

The extracted skeleton often contains small branches.
To clean up the structure, small branches can be automatically removed by clicking the **Remove Small Branches** button.


![Skeleton Extract](./doc/images_en/skeleton.png)

During the skeleton extraction and small branch removal process, some major skeleton structures may be lost.
Manual adjustment tools are therefore provided to allow corrections and additions as needed.

The available skeleton editing tools include:

- **Add Skeleton Point**: After selecting this tool, clicking on the image will create a skeleton point.
Clicking a second time at another location will automatically connect the two points, forming a skeleton line between them.
To start a new, independent skeleton segment without connecting to the previous point, right-click at the desired location to create an unconnected skeleton point.

- **Remove Skeleton Point**: Clicking on an existing skeleton point will delete the selected point along with any skeleton lines passing through it.

> Since the skeleton extraction is based on the crack mask obtained in the previous stage, it is recommended to refine 
and clean the crack regions well during the Crack Detection Stage. This will help achieve a better extracted skeleton result.


![Skeleton Edit](./doc/images_en/skeletonedit.png)


## Results Export Stage

After completing the previous steps, the final stage displays the analysis results based on the detected crack masks, extracted skeletons, and the calibrated resolution.

The interface presents, for each image:
- File Name
- Crack Area
- Skeleton Length
- Mean Crack Width

An export function is provided to allow batch exporting of these results into a `.csv` file by selecting a target output path.

![Results Export](./doc/images_en/result.png)


After completing the analysis, clicking the **Finish** button will clear the current results and return the workflow to the initial stage, ready for a new round of analysis.

If any stage needs to be modified during the process (e.g., uploading additional images, adjusting the crack mask, or refining the skeleton), it is possible to navigate back to the corresponding stage by clicking the stage indicator at the top of the interface.

> After returning to a previous stage and making modifications, it is recommended to rerun all subsequent stages to ensure the results are properly updated.
Directly jumping to the final stage without re-executing intermediate stages may lead to inconsistent or outdated results.
Please Always follow the workflow sequence after making any changes.



## Software stack
- Backend/Logic: Python3
- Frontend: Qt6/PySide6

## Authors
Bertram Richter and Xiaoli Song
