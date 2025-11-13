# Test 07 - Bootstrap Analysis

## Purpose

Run bootstrap-based performance estimates and tables for the evaluation cohort, producing pivot tables with AUC, sensitivity/precision operating points, odds ratios and other KPIs. Optionally runs comparator analysis when alternative predictions are provided.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Reference run (contains baseline bootstrap JSON and cohort parameters)
- `BT_JSON`: Path to bootstrap features JSON (defaults to `${FIRST_WORK_DIR}/json/bootstrap/bt_features.json`)
- `BT_COHORT`: Path to bootstrap cohorts params (defaults to `${FIRST_WORK_DIR}/json/bootstrap/bt.params`)
- `SUB_CODES`: Comma-separated sub-cohort identifiers (used to run per-sub-cohort bootstraps)
- Optional: `ALT_PREDS_PATH` to run comparator bootstrap between predictions
- Optional: `CONTROL_WEIGHT` to adjust weighting of controls

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 7
```

Or include as part of the full suite:

```bash
./run.sh
```

Check `${WORK_DIR}/bootstrap` for output pivot tables and reports.

## What This Test Does

- Joins samples (`${WORK_DIR}/Samples/relabeled.samples`) with predictions from `${FIRST_WORK_DIR}/compare/3.test_cohort.preds` (or `${FIRST_WORK_DIR}/predictions/all.preds` if present) to produce `${WORK_DIR}/bootstrap/all.preds`.
- Filters to eligible predictions and produces `${WORK_DIR}/bootstrap/eligible_only.preds`.
- Sets up arrays of sensitivity, FPR and precision working points used for bootstrap KPIs.
- Invokes [bootstrap_app](../../../bootstrap_app) with the provided `BT_JSON` and `BT_COHORT` to generate pivot outputs and per-cohort bootstrap results under `${WORK_DIR}/bootstrap/mes.bt*` and pivot text files `${WORK_DIR}/bootstrap/*.pivot_txt`.
- For each `SUB_CODES` member, creates per-sub-cohort prediction files and runs bootstrap again (with `sample_per_pid=1` for sub-cohorts).
- Runs `bootstrap_format.py` to aggregate pivot reports into TSV tables like `${WORK_DIR}/bootstrap/bt.just_MES.tsv`.
- If `ALT_PREDS_PATH` is provided, fits a comparator to the cohort and runs an additional bootstrap to compare the model against the alternative predictions, producing `${WORK_DIR}/bootstrap/comperator.bt*` and aggregated tables `${WORK_DIR}/bootstrap/bt.MES_comperator.tsv`.

## Output Location

- Bootstrap pivot and pivot text: `${WORK_DIR}/bootstrap/*.pivot_txt`
- Aggregated tables: `${WORK_DIR}/bootstrap/bt.just_MES.tsv`, `${WORK_DIR}/bootstrap/bt.MES_comperator.tsv` (if comparator run)
- Per-sub-cohort bootstrap files: `${WORK_DIR}/bootstrap/<subcode>.bt` and `<subcode>.preds`

## How to Interpret Results

- Open pivot tables (`.pivot_txt`) and aggregated TSV files to inspect AUC, sensitivity/precision points, ORs, LIFT, and other measures across cohorts and groups.
- Compare comparator tables to see whether the alternative predictions outperform the model in specific cohorts or overall.

## Common failure modes and suggestions

- Mismatch between sample IDs and prediction files when joining:
    * Ensure sample files use the expected ID columns and prediction files have matching ID columns.
- `bootstrap_app` or `bootstrap_format.py` missing or failing:
    * Confirm these CLI tools are available and their versions are compatible with the `BT_JSON` being used.
- Large sample sizes causing long runtime:
    * Use subsampling arguments in `bootstrap_app` (e.g., `sample_per_pid`, `sample sizes`) to speed up analysis.

## Example output snippets

1) Aggregated bootstrap TSV header (example):

```text
Cohort	Measure	Value
Age:50-75	AUC_Mean	0.85123
```

2) Console summary after running: 

```text
Please refer to /path/to/work_dir/bootstrap/bt.just_MES.tsv
```

## Notes and Implementation Details

- The test computes eligible-only predictions by filtering out lines with missing eligibility fields.
- Working points for sensitivity, precision and FPR are hard-coded arrays in the script and can be customized as needed.
- Control weighting can be passed via `CONTROL_WEIGHT` to adjust bootstrap behaviour for class imbalance.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/bootstrap/mes.bt.pivot_txt`
- `${WORK_DIR}/bootstrap/bt.just_MES.tsv`
- `${WORK_DIR}/bootstrap/*.bt` (per-cohort)
