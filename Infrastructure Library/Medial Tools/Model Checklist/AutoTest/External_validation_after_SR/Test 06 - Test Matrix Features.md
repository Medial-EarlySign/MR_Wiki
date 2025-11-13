# Test 06 - Matrix Feature Statistics & KLD Analysis

## Purpose

Compute per-feature statistics comparing the silent/external run matrix against a reference matrix and produce plots and Kullback–Leibler divergence (KLD) metrics for the top features derived from a Shap/ButWhy report. The test writes per-feature HTML graphs and a `features_stats.tsv` summary.
This is similar to [Silent Run Test (no labels) - 10](../External%20Silent%20Run/Test%2010%20-%20Compare%20Important%20Feature.md). Now we loaded the repository and have outcome. The stratification and comparasing can also stratify by the outcome.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Path to the reference run (used to obtain the original model and shapley report)
- `MODEL_PATH`: Path to the model to be used on the repository (by default taken from `${FIRST_WORK_DIR}/model/model.medmdl`)
- `REFERENCE_MATRIX`: CSV path to the reference matrix
- `CONFIG_DIR`: Directory containing config files such as `feat_resolution.tsv`
- `CMP_FEATURE_RES`: Comma-separated list used to determine top features and resolutions

Script-level required params (from the script header):

- `REQ_PARAMETERS=['WORK_DIR', 'FIRST_WORK_DIR', 'MODEL_PATH', 'REFERENCE_MATRIX', 'CONFIG_DIR']`

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 6
```

Or include as part of the full suite:

```bash
./run.sh
```

Check `${WORK_DIR}/outputs/graphs` and `${WORK_DIR}/outputs/features_stats.tsv` for results.

## What This Test Does

- Validates that a Shap/ButWhy report exists under `${FIRST_WORK_DIR}/ButWhy/shapley.report` and fails if not present.
- Optionally reads a resolution file `${CONFIG_DIR}/feat_resolution.tsv` to apply trimming and resolution rules for plotting.
- Reads the top features from the Shapley report (top 25 positive importance features plus `pred_0`).
- Loads the repository matrix for `${WORK_DIR}/Samples/3.test_cohort.samples` using `get_matrix()` and loads the reference CSV.
- For each selected feature:
  - Applies trimming/resolution rules if provided.
  - Computes mean, std, and missing rates overall, for cases, and for controls.
  - Writes per-feature HTML bar plots (via `plot_graph`) to `${WORK_DIR}/outputs/graphs`.
  - Computes KLD between cases and controls and prints the metric.
- Summarizes per-feature stats in `${WORK_DIR}/outputs/features_stats.tsv`.

## Output Location

- Feature graphs: `${WORK_DIR}/outputs/graphs` (one HTML per feature)
- Stats TSV: `${WORK_DIR}/outputs/features_stats.tsv`

## How to Interpret Results

- Open the generated HTML files to visually inspect the distribution of feature values between cases, controls and reference.
- Use `features_stats.tsv` to get a tabular summary of mean, std, and missingness across groups.
- KLD values printed to stdout indicate how separable feature distributions are between cases and controls; higher KLD suggests more divergence.

## Common failure modes and suggestions

- Missing `shapley.report` under `${FIRST_WORK_DIR}/ButWhy`:
    * Run [ButWhy analysis](../External%20Silent%20Run/Test%2013%20-%20But%20Why%20(Shapley).md) (feature importance) before running this test in Silent Run
- Feature name mismatches between the Shap report and repository matrix columns:
    * Confirm that feature naming conventions match (the script searches by substring match and expects exactly one match per selected feature).
- Large reference matrices or memory issues when loading matrices:
    * Use a machine with sufficient memory or sample/reduce the dataset before running.

## Example output snippets

This is similar to [Silent Run Test (no labels) - 10](../External%20Silent%20Run/Test%2010%20-%20Compare%20Important%20Feature.md), but with stratification by outcome.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/outputs/graphs/*.html`
- `${WORK_DIR}/outputs/features_stats.tsv`
