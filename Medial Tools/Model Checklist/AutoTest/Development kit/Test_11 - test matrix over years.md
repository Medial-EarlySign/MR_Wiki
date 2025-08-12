# Test_11 - test matrix over years

## Overview
Tests of model features over the years. What changes in the features between different years?
We want to make sure there are no biases or something important that is time sensitive.
It takes the test samples and compares the most recent prediction date samples to the least recent prediction date samples and creates propensity model that tries to differentiate between samples.

## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples

## Output
- $WORK_DIR/compare_years
    - Global.html - the most important features in the propensity model that are different between the years
    - features_diff - A directory that compares each of the important features in the propensity model - least recent to most recent on the same graph.
    - single_features - But why single feature analysis directory for each of the important features in the propensity model analysis
    - compare_rep.txt - text file that compare the average value of each feature
    - test_propensity.bootstrap.pivot_txt - the propensity model performance
Please go over on the most important different features and decide if that's OK
