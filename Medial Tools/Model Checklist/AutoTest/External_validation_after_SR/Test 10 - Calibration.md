# Test 10 - Calibration Test

## Purpose

Run calibration checks for the model on the evaluation cohort. Produces calibration pivot tables and bootstrap calibration graphs showing model calibration across score bins, time windows, and cohorts.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Reference run (used to obtain baseline predictions)
- `BT_COHORT_CALIBRATION`: Cohorts file for calibration analysis
- `BT_JSON_CALIBRATION`: Bootstrap JSON for calibration-specific metrics
- Optional: `ALT_PREDS_PATH` for comparator predictions

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 10
```

Or include as part of the full suite:

```bash
./run.sh
```

Check `${WORK_DIR}/calibration` for calibration outputs and graphs.

## What This Test Does

- Joins samples with predictions similar to Test 07 to create `${WORK_DIR}/bootstrap/all.preds` and filters to `${WORK_DIR}/bootstrap/eligible_only.preds`.
- Validates `BT_COHORT_CALIBRATION` contains yearly breakdowns and warns if not present.
- Invokes `TestCalibration` with the provided cohorts and JSON model to produce calibration outputs under `${WORK_DIR}/calibration/test_calibration` and calibration graphs under `${WORK_DIR}/calibration/graphs`.
- Prints a brief numeric summary of mean score and incidence.

## Output Location

- Calibration outputs: `${WORK_DIR}/calibration/test_calibration` (tables and pivot files)
- Calibration graphs: `${WORK_DIR}/calibration/graphs`

## How to Interpret Results

- Open pivot tables and graphs to inspect calibration curves across bins, cohorts, and time windows.
- Confirm expected calibration behaviour (e.g., predicted probabilities aligned with observed incidence per bin).

## Common failure modes and suggestions

- Missing `TestCalibration` utility or incompatible flags:
    * Ensure `TestCalibration` exists and the JSON/params supplied match the utility's expected schema.
- Insufficient sample size for fine-grained binning:
    * Adjust `pred_binning_arg` or `bt_params` to use fewer bins or fewer bootstrap loops.

## Example output snippets

[TestCalibration tool outputs](../../../Calibrate%20model,%20and%20calibration%20test.md)

## Notes and Implementation Details

- The script uses `pred_binning_arg` with `iterative_merge` and parameters tuned to create up to 100 bins with minimum counts; it also runs `loopCnt=500` bootstrap samples by default.
- Calibration requires a good spread of predicted scores; if all scores are near a single value, binning will collapse and calibration plots will be uninformative.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/calibration/test_calibration` (pivot and summary tables)
- `${WORK_DIR}/calibration/graphs/*`

