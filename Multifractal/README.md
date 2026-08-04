# Organoid Contour Multifractal Analysis Pipeline

This code quantifies the morphological complexity of organoid segmentation masks across experimental batches and time points using local Hölder exponent estimation and multifractal spectrum analysis.

The script processes predicted organoid mask images, extracts the largest contour boundary for each organoid, and applies a spatial sandbox method to compute local Hölder exponents. It computes a complexity metric defined as the range of Hölder exponents and calculates the Shannon entropy of the exponent distribution.

---

## Expected Directory Structure

Before running the script, ensure your raw dataset and supporting files are organized as follows:

```text
.
├── Stitched_AR.csv
├── main_analysis.py
└── data_new/
    ├── batch1/
    │   ├── day10/
    │   │   └── predicted_masks/
    │   │       └── mask_image_1_predmask.png
    │   └── day24/
    │       └── ...
    ├── batch2/
    └── Stitched/
