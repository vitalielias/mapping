
# FEI Thermofisher SEM to JSON

**Description:**

The SEM to JSON component is able to intelligently extract metadata from microscopy metadata files originating from FEI/Thermofisher instruments generated through research by employing the [Python Hyperspy library](https://hyperspy.org/index.html). For SEM data, most instruments are able to write and embed the metadata directly into the research images in `TIFF` format. The metadata is then extracted from these images and mapped to the existing [SEM schema](https://github.com/kit-data-manager/Metadata-Schemas-for-Materials-Science/blob/main/SEM-FIB%20Tomography/SEM_FIB_Tomography_Acquisition_Main.json), resulting in a `JSON` metadata document adhering to the aforementioned and agreed-upon schema.

The tool has some limitations; some older SEM instruments are unable to embed the metadata in the `TIFF` files, and therefore an automatic extraction is not possible. This is indicated in the result file if it happens to be the case.

This component may be used to process a single research image in `.tiff` format, or a zipped directory containing the `.tiff` files may be uploaded to enable batch processing.

- **Input:**
  - SEM research image in `.tiff` format, OR;
  - Compressed directory containing the SEM research images in `.zip` format.

- **Output:**
  - Structured metadata document in `.json` format, OR;
  - Compressed directory in `.zip` format containing the metadata documents for each image in the user-provided zip directory.

## Warnings
This plugin is still under development and therefore requires some additional parameters to be configured for extraction, namely the units of many values, which still need to be entered manually by the user at the moment.
