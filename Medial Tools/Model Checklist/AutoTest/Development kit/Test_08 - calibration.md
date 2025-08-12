# Test_08 - calibration

## Overview
Tests that the model calibration performance if applicable.
For calibration information please refer to [Calibrate model, and calibration test](/Medial%20Tools/Guide%20for%20common%20actions/Calibrate%20model,%20and%20calibration%20test.md)

## Input
- WORK_DIR - output work directory
- CALIBRATED_MODEL - path for calibrated model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES_CALIBRATION - test samples for calibration
- BT_JSON_CALIBRATION - json for bootstrap analysis
- BT_COHORT_CALIBRATION - bootstrap cohort definition to focus on calibration
 
## Output
${WORK_DIR}/calibration

- bt.pivot_txt - bootstrap results of calibration measurement
- *.html  - calibration graph result for each cohort - for each score bin, plots observed mean outcome, expected confidence internal, etc.
