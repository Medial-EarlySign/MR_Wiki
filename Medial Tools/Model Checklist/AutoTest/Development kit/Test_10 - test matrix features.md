# Test_10 - test matrix features

## Overview
Tests of model features - plots important features. We want to make sure there are no outliers, "junk" values in the matrix that the model can use.
## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- config/feat_resolution.tsv - defines resolution for features that we are going to print [Optional].

##  Depends
[test_05](../Test_05%20-%20But%20why) - Will use the feature importance to select which features to plot.

## Output
- $WORK_DIR}/outputs/features_stats.tsv - a table with stats on each feature divided into cases/controls. Mean,Std, missing values percentage. Please go over to see the values are OK
- $WORK_DIR}/outputs/graphs - graph for each feature - please have a look and see the distribution.
 
