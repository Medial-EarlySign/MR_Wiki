
# Test 10: Matrix Features

## Purpose
Visualize and analyze the distribution of important model features, helping to detect outliers, unusual values, or "junk" data that could affect model performance.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `config/feat_resolution.tsv`: (Optional) Defines resolution for feature plots

## Depends On
- [Test 05: But Why](Test_05%20-%20But%20why.md): Uses feature importance to select which features to plot

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 10
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Generates matrix plots for selected features, highlighting their value distributions
- Uses `feat_resolution.tsv` (if provided) to control plot resolution
- Helps identify outliers, missing values, and distribution issues in processed features

## Output Location
- `${WORK_DIR}/outputs/features_stats.tsv`: Table with statistics for each feature (mean, std, missing value percentage, split by cases/controls)
- `${WORK_DIR}/outputs/graphs`: Graphs for each feature showing value distributions

## How to Interpret Results
- Review feature statistics for reasonable values and balance
- Inspect graphs for outliers, skewed distributions, or unexpected patterns
- Use findings to refine feature engineering and improve model robustness
