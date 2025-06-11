# Test_07 - feature importance

## Overview
Tests that the model feature importance in different way - how each signal impact model performance if we will not "send" it to the model.
We will test each signal in a group that the signal exists, otherwise important signals but very rare will get low importance and we don't want necessarily this to happen.

## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- BT_JSON_FAIRNESS - json for bootstrap analysis
- FAIRNESS_BT_PREFIX - bootstrap cohort definition to focus on feature importance
 
## Depends:
Test_06 -  predictions file results

## Output
$WORK_DIR}/ButWhy/feature_importance.sorted_final.tsv - file with sorted signals importance.
For each signal - how many of the samples has this signal (feature are not missing values) and how important is it (impact on AUC if you don't pass it to the model).
 
