# Test 05 - Compare Matrices & Feature Analysis

## Purpose

Compare the matrix produced by the silent/external run against a reference matrix and generate feature-level difference reports and visualizations (including Shap/ButWhy analyses). The test produces interactive HTML reports (Plotly) and global/single-feature explainability outputs for inspection.
This is similar to [Silent Run Test (no labels) - 05](../External%20Silent%20Run/Test%2005%20-%20Compare%20Repository%20with%20Reference%20Matrix.md). Now we loaded the repository and have outcome. The stratification and comparasing can also stratify by the outcome.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `MODEL_PATH`: Path to the model used for generating matrices (by default pulled from `${FIRST_WORK_DIR}/model/model.medmdl`)
- `REFERENCE_MATRIX`: CSV path to the reference matrix to compare against
- `CMP_FEATURE_RES`: Comma-separated feature resolution definitions used for feature-subsetting in the no-overfitting run


## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 5
```

Or include as part of the full suite:

```bash
./run.sh
```

Check `${WORK_DIR}/compare` and `${WORK_DIR}/compare.no_overfitting` for results and HTML visualizations.

## What This Test Does

- Calls [TestModelExternal](../../../TestModelExternal.md) to compare the model applied to the test repository against the `REFERENCE_MATRIX`. Outputs are written to `${WORK_DIR}/compare`.
    - Uses sampling limits (`MAX_SIZE=500000`) and various subsampling parameters to limit memory use.
    - Produces feature-level `shapley_report.tsv` under `${WORK_DIR}/compare`.
- Runs `feature_importance_printer.py` to build a global and single-feature HTML visualizations under `${WORK_DIR}/compare/ButWhy`.
- Runs a second comparison under `compare.no_overfitting` with a restricted feature set derived from `CMP_FEATURE_RES` to check results when removing possibly overfitted features.
- Fixes plotly.js script tag paths in output HTML files so they link correctly from the final docs location.

## Output Location

- Primary comparison outputs: `${WORK_DIR}/compare`
- No-overfitting comparison outputs: `${WORK_DIR}/compare.no_overfitting`
- Feature explainability HTML reports: `${WORK_DIR}/compare/ButWhy` and `${WORK_DIR}/compare.no_overfitting/ButWhy`
- Shapley reports: `${WORK_DIR}/compare/shapley_report.tsv`

## How to Interpret Results

- Open `${WORK_DIR}/compare/` and use same methodology as in [Test 05 in Silent Run](../External%20Silent%20Run/Test%2005%20-%20Compare%20Repository%20with%20Reference%20Matrix.md)
- Review `${WORK_DIR}/compare/compare_rep.txt` for a textual summary of the comparison.
- Use the `ButWhy` HTMLs to understand global and single-feature contributions and check whether important features behave similarly between the silent run and the reference.
- The `compare.no_overfitting` run restricts features based on `CMP_FEATURE_RES` and can reveal whether top differences are driven by a small set of features.

## Common failure modes and suggestions

- Large matrices exceed memory or time limits:
    * Adjust `MAX_SIZE` and subsample parameters in the script to reduce processing size.
- Missing `TestModelExternal` or `feature_importance_printer.py` utilities:
    * Ensure these are available on PATH.
- Plotly template or `plot.py` not found:
    * Confirm `plot.py` exists in PATH and that its `templates/plot_with_missing.html` file is reachable.
- Incorrect `CMP_FEATURE_RES` formatting:
    * The script expects comma-separated tokens like `FeatureA:0.1,FeatureB:10`-ensure formatting matches.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/compare/compare_rep.txt`
- `${WORK_DIR}/compare/shapley_report.tsv`
- `${WORK_DIR}/compare/ButWhy/Global.html`
- `${WORK_DIR}/compare.no_overfitting/ButWhy/Global.html`
