# Test 15 - Features and Flag

## Purpose

Compare distributions of important features between flagged and non-flagged samples in both the test and reference datasets. Produces per-feature statistics, per-gender histograms, and ratio plots highlighting where flagged populations differ.

## Required Inputs

- `WORK_DIR`: working directory containing compare matrices and prediction files
- `CMP_FEATURE_RES`: comma-separated list of feature identifiers with resolution (used to select and bucket features)
- `TOP_EXPLAIN_PERCENTAGE`: used to compute the flagged cutoff (script computes CUTOFF = 100 - TOP_EXPLAIN_PERCENTAGE)
- Files expected:
  - `${WORK_DIR}/compare/rep_propensity.matrix`
  - `${WORK_DIR}/compare/rep_propensity_non_norm.matrix`
  - `${WORK_DIR}/compare/3.test_cohort.preds`
  - `${WORK_DIR}/compare/reference.preds`

## How to Run
```bash
./run.specific.sh 15
```
Or include in the full run:
```bash
./run.sh
```

## What This Test Does

- Reads normalized and non-normalized propensity matrices and prediction files.
- Parses `CMP_FEATURE_RES` to extract features and their binning resolution. Rounds feature values to the requested resolution.
- Splits samples into flagged vs not-flagged using the percentile cutoff derived from test predictions (`CUTOFF = 100 - TOP_EXPLAIN_PERCENTAGE`).
- Computes per-feature stats (means, std, missing%) for flagged and not-flagged groups in both test and reference and writes `features_and_flag.csv`.
- Produces HTML bar charts per-feature showing percentage distributions for Test_Flagged, Test_Not_Flagged, Ref_Flagged, Ref_Not_Flagged and additional ratio charts (files under `${WORK_DIR}/features_and_flag/*.html`).

## Output Location

- `${WORK_DIR}/features_and_flag/features_and_flag.csv`
- `${WORK_DIR}/features_and_flag/<feature>.html` and `<feature>_ratio.html` per-feature visualization files

## How to Interpret Results

- Use `features_and_flag.csv` to compare means/stds and missing rates between flagged and not-flagged groups across test and reference.
- Use per-feature HTMLs to visually inspect whether flagged subjects have different distributions and whether those patterns are consistent with the reference dataset.

## Troubleshooting

- Feature name matching errors: the script searches columns by substring and assumes a single exact match; mismatches will raise errors-confirm `CMP_FEATURE_RES` aligns with column names in the matrices.
- Missing matrices or predictions: run Tests 03 and 05 first to ensure `${WORK_DIR}/compare/*` artifacts exist.
- Plot rendering: HTMLs reference `../js/plotly.js`; ensure the asset exists or change the path.

## Files to inspect

- `${WORK_DIR}/features_and_flag/features_and_flag.csv`
- `${WORK_DIR}/features_and_flag/*.html`
