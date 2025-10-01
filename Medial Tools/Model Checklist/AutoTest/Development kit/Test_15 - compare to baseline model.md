
# Test 15: Compare to Baseline Model

## Purpose
Compare your model to a baseline model by evaluating performance, correlation, and which patients are flagged. This analysis highlights differences, improvements, and cases your model captures that the baseline misses.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to your model
- `BASELINE_MODEL_PATH`: Path to the baseline model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `BT_JSON`: Bootstrap JSON for cohort filtering
- `BT_COHORT`: Bootstrap cohort definition
- `BASELINE_COMPARE_TOP`: Top percentage of predictions to compare (default: 5%)

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 15
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Compares top X% of flagged patients between your model and the baseline
- Calculates performance metrics, overlap scores, and correlation
- Trains a propensity model to differentiate patients flagged by each model
- Analyzes which features are used differently by your model vs. baseline

## Output Location
- `$WORK_DIR/ButWhy.baseline/`: But Why analysis for baseline model (Global.html, Global.ungrouped.html, single_features)
- `$WORK_DIR/bootstrap/bt_baseline_compare.tsv`: Bootstrap results comparison
- `$WORK_DIR/compare_to_baseline/correlation.txt`: Correlation of scores between models
- `$WORK_DIR/compare_to_baseline/`: Propensity model results
    - `Global.html`: Most important signals differentiating flagged patients
    - `single_features/`: But Why analysis for each important feature
    - `compare_rep.txt`: Table comparing feature means, std, etc. for flagged patients
- `$WORK_DIR/compare_to_baseline/baseline_coverage_by_mes_$BASELINE_COMPARE_TOP.html`: Coverage/intersection of flagged individuals at different cutoffs
- `$WORK_DIR/compare_to_baseline/compare_Age_top_flagged.html`: Comparison of flagged ages by both models

## How to Interpret Results
- Use overlap and coverage metrics to see how much your model improves on the baseline
- Review propensity model outputs to understand which features drive differences
- Check correlation and age comparisons for additional insights
