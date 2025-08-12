# Test_15 - compare to baseline model

## Overview
The goal is to compare our model to baseline model.
We will compare performance and correlation, which patient get flagged and how are they different? what baseline model misses that we capture?

## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- BASELINE_MODEL_PATH - path to baseline model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- BT_JSON - bootstrap json to filter cohort
- BT_COHORT - bootstrap cohort to filter cohort
- BASELINE_COMPARE_TOP - Which top percentage to take for comparing (default is 5%)

## Output
- $WORK_DIR/ButWhy.baseline - But why for baseline model. Global.html, Global.ungrouped.html, single_features directory
- $WORK_DIR/bootstrap/bt_baseline_compare.tsv - compares bootstrap result with baseline
- $WORK_DIR/compare_to_baseline/correlation.txt - correlation of scores
- $WORK_DIR/compare_to_baseline - result of training propensity model that tries to differentiate which top  "BASELINE_COMPARE_TOP" our model flags compares to baseline flag in top BASELINE_COMPARE_TOP.
    - Global.html - most important signals in that propensity model . Describe which features our model uses more/different than baseline
    - single_features - a directory with butwhy analysis of each important feature in that model
    - compare_rep.txt - a text table that compares each of the features mean, std, etc in both samples - the one our model flags compared to baseline
- $WORK_DIR/compare_to_baseline/baseline_coverage_by_mes_$BASELINE_COMPARE_TOP.html - How much intersection/coverage of baseline flagged individuals are covered by our model in different cutoffs
- $WORK_DIR/compare_to_baseline/compare_Age_top_flagged.html - comparing flagged age by both models
