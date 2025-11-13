# Test 08 - Age of Flagged Analysis

## Purpose

Generate age and temporal analyses for flagged cases/controls across specified cohorts. Produces graphs and statistics for cases and controls stratified by cohorts defined in the `COHORTS` environment variable.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Reference run (contains rep and bootstrap JSON)
- `COHORTS`: A pipe-separated list of cohort definitions; each item should be `name=features` where `features` is a filter string understood by `FilterSamples`/bootstrap
- Optional: `ALT_PREDS_PATH` for comparator comparisons

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 8
```

Or include as part of the full suite:

```bash
./run.sh
```

Outputs are stored under `${WORK_DIR}/age_of_flagged`.

## What This Test Does

- If `ALT_PREDS_PATH` is not set, prints a message noting comparator comparisons will be skipped.
- For each cohort listed in `COHORTS`:
    - Uses `FilterSamples` to create cohort-specific prediction files `${WORK_DIR}/bootstrap/<cohort_name>.preds` if not present.
    - Invokes `age_of_flagged.py` (a Python helper) to compute and plot age distributions and other temporal statistics for the given cohort; outputs go under `${WORK_DIR}/age_of_flagged`.

## Output Location

- Per-cohort age analysis: `${WORK_DIR}/age_of_flagged` (HTML or image outputs and supporting data files)
- Per-cohort prediction files used as input: `${WORK_DIR}/bootstrap/<cohort>.preds`

## How to Interpret Results

- Open the plots in `${WORK_DIR}/age_of_flagged` to inspect age distributions among flagged (predicted high-risk) patients and controls.
- Compare cohort-specific plots to check consistency (e.g., older average age in one cohort may indicate selection bias).

## Common failure modes and suggestions

- Misformatted `COHORTS` variable:
    * Ensure `COHORTS` contains entries like `cohortName=featureFilter` separated by `|`.
- Missing `FilterSamples` or `age_of_flagged.py` helper scripts:
    * Ensure the referenced helpers are available under `${CURR_PT}/resources` or on PATH.
- Missing input predictions or samples:
    * Confirm `${WORK_DIR}/bootstrap/eligible_only.preds` exists and prediction files referenced by `${FIRST_WORK_DIR}` are present.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/age_of_flagged/*` (per-cohort graphs)

