# Test 17 - Estimate Performance from Calibration

## Purpose

Compute model predictions using a calibrated model and run a specialized `PerformanceFromCalibration` tool to summarize performance metrics derived from the calibrated predictions.

## Required Inputs

- `WORK_DIR`: working directory containing repository and model artifacts
- Calibrated model path: expected `${WORK_DIR}/model/model.medmdl` (the script uses `CALIBRATED_MODEL_PATH`)
- `${WORK_DIR}/rep/test.repository` and `${WORK_DIR}/Samples/3.test_cohort.samples`

## How to Run
```bash
./run.specific.sh 17
```
Or run within the full suite:
```bash
./run.sh
```

## What This Test Does

- Produces predictions using the calibrated model with [Flow](../../../Using%20the%20Flow%20App/index.md#predictingapplying-a-model) and writes `${WORK_DIR}/compare/test.calibrated.preds`.
- Runs `PerformanceFromCalibration --preds <preds> --output <WORK_DIR>/pref_from_calibration/result` to analyze calibrated predictions and produce a summary output.
    - The Flow call may include a memory limit modification if `MEMORY_LIMIT` is set; the script injects a model change via `--change_model_init` when applicable.

## Output Location

- `${WORK_DIR}/compare/test.calibrated.preds`
- `${WORK_DIR}/pref_from_calibration/result`

## How to Interpret Results

- The `result` file contains performance summaries produced by `PerformanceFromCalibration`. Use it to compare calibrated vs uncalibrated predictions and to estimate expected performance under calibration adjustments.

> **Performance Estimation Warning!** The performance metrics derived from this cohort analysis are highly sensitive to noise and should be treated with caution.

This estimation method relies on the assumption that the model is perfectly calibrated on the test dataset, which may introduce inaccuracies. Since even minor calibration errors can significantly skew the performance estimates, the methodology detailed in [Test 11: Estimate Performances](Test%2011%20-%20Estimate%20Performances.md) is the preferred and more robust approach for determining actual model performance. Anyway, this method is also available. 

## Troubleshooting

- `Flow` failures or memory issues: if Flow fails due to memory, set `MEMORY_LIMIT` in `env.sh` to an appropriate value.
- Missing calibrated model: ensure `${WORK_DIR}/model/model.medmdl` exists and is the calibrated variant you expect.

## Files to inspect

- `${WORK_DIR}/compare/test.calibrated.preds`
- `${WORK_DIR}/pref_from_calibration/result`
