
# Test 07: Feature Importance

## Purpose
Assess the importance of each input signal in the model by measuring the impact on performance when the signal is excluded. This approach focuses on signals present in the last year or three years, ensuring that rare but important signals are not undervalued. See [model_signals_importance](../../../model_signals_importance.md) for methodology details.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `BT_JSON_FAIRNESS`: JSON file for bootstrap analysis
- `FAIRNESS_BT_PREFIX`: Bootstrap cohort definition for feature importance focus

## Prerequisites
- Requires predictions file results from Test_06 (bootstrap results)

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 7
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- For each signal, measures the change in model performance (e.g., AUC) when the signal is omitted
- Focuses analysis on cohorts where the signal exists in the last year/three years
- Avoids undervaluing rare but important signals

## Output Location
- Results file: `${WORK_DIR}/ButWhy/feature_importance.sorted_final.tsv`
	- For each signal: number of samples with non-missing values, and importance score (impact on AUC if excluded)

## How to Interpret Results
- Use the sorted importance file to identify key signals driving model performance
- Check for signals that are rare but have high impact
- Use results to guide feature selection and model refinement
 