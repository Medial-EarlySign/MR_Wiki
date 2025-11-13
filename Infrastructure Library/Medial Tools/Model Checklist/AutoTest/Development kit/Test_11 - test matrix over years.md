
# Test 11: Matrix Over Years

## Purpose
Analyze how model features change over time, comparing samples from the most recent and least recent prediction dates. This helps detect temporal biases, shifts, or time-sensitive patterns in the data and model.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 11
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Compares feature matrices from the most recent and least recent prediction dates
- Builds a propensity model to differentiate between samples from different years. Uses [TestModelExternal](../../../TestModelExternal.md) tool for more details.
- Highlights features that change over time and may introduce bias

## Output Location
- `$WORK_DIR/compare_years/`
    - `Global.html`: Most important features in the propensity model (differences between years)
    - `features_diff/`: Graphs comparing each important feature (least recent vs. most recent)
    - `single_features/`: But Why analysis for each important feature in the propensity model
    - `compare_rep.txt`: Text file comparing average values of each feature
    - `test_propensity.bootstrap.pivot_txt`: Propensity model performance metrics

## How to Interpret Results
- Review the most important features that differ between years
- Inspect feature comparison graphs for trends, shifts, or anomalies
- Use findings to identify and address potential temporal biases in your model
