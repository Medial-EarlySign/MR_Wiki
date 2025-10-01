
# Test 06: Bootstrap Results

## Purpose
Assess model performance stability and reliability using bootstrap resampling. This test estimates variability and confidence intervals for key metrics, ensuring robust and reproducible results.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `PREDS_CV` or `TEST_SAMPLES`: Test samples or cross-validation predictions
- `BT_JSON`: JSON file for bootstrap analysis
- `BT_COHORT`: Bootstrap cohort definitions

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 6
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Applies bootstrap analysis to model predictions
- Calculates performance metrics with variability and confidence intervals
- Helps verify that results are not due to random chance or overfitting

## Output Location
- Results are saved in `${WORK_DIR}/bootstrap`
- Main output file: `bt.pivot_txt` (see [Bootstrap output legend](../../../bootstrap_app/Bootstrap%20legend.md) for details)

## How to Interpret Results
- Review confidence intervals and variability for each metric
- Use results to assess model robustness and generalizability