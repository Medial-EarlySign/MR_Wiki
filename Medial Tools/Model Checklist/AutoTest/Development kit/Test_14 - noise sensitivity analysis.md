# Test_14 - noise sensitivity analysis

## Overview
Tests the model sensitivity for noise - noise in missing values, shifting dates backward and shifting the values (see that there is no resolution problem for example).

## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- TRAIN_SAMPLES_BEFORE_MATCHING - the training samples
- BT_JSON - bootstrap json to filter cohort
- BT_COHORT - bootstrap cohort to filter cohort
- NOISER_JSON - Path to noiser json config
- TIME_NOISES, VAL_NOISES, DROP_NOISES - parameters to control the noise
## Depends:
[test_06](Test_06%20-%20bootstrap%20results.md)

## Output
$WORK_DIR/test_noiser/results
- time_analysis.csv - How the noise in time effect the model in different noise levels
- value_analysis.csv - How the noise in values effect the model in different noise levels
- drop_analysis.csv - How dropping tests effect the model in different drop levels
