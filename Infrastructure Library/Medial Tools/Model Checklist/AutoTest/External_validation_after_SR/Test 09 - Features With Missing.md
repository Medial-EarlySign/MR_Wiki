# Test 09 - Features With Missing Values Analysis

## Purpose

Run feature analysis that specifically inspects missingness patterns for a selected set of important features. Computes statistics and plots for features where missing values are informative or prevalent.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Reference run (contains model and rep)
- `MODEL_PATH`: Path to the model to be used for generating features
- `CONFIG_DIR`: Directory holding `feat_resolution.tsv` and similar config files
- `CMP_FEATURE_RES`: Comma-separated list of feature:resolution tokens used to define the top features and per-feature resolution

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 9
```

Or include as part of the full suite:

```bash
./run.sh
```

Outputs are placed under `${WORK_DIR}/outputs/features_stats.with_missings.tsv` and `${WORK_DIR}/outputs/graphs_with_missings`.

## What This Test Does

- Loads the repository with `med.PidRepository()` and initializes it with `${WORK_DIR}/rep/test.repository`.
- Loads the model from `${FIRST_WORK_DIR}/model/model.medmdl`, fits it to the repository, and applies feature generators to the samples (`${WORK_DIR}/Samples/3.test_cohort.samples`), producing a feature DataFrame.
- Selects `top_features` from `CMP_FEATURE_RES` and applies per-feature resolution adjustments.
- For each feature:
    - Computes overall, case, and control means, stds and missingness percentages (missing is expected to be coded as `-65336`).
    - Writes results to `${WORK_DIR}/outputs/features_stats.with_missings.tsv`.
    - Generates plots (markers+lines) saved under `${WORK_DIR}/outputs/graphs_with_missings` (plotly HTML files).
    - Computes KLD between case and control distributions and prints results.

## Output Location

- Stats TSV: `${WORK_DIR}/outputs/features_stats.with_missings.tsv`
- Graphs: `${WORK_DIR}/outputs/graphs_with_missings` (one HTML per feature)

## How to Interpret Results

- Use the TSV to quickly see which features have high missingness and how that differs between cases and controls.
- Open HTML graphs to inspect distribution patterns and whether missingness behaves differently across outcome groups.
- Elevated KLD suggests the feature's distribution differs notably between cases and controls (including missingness patterns).

## Common failure modes and suggestions

- Failure to load repository or model:
    * Ensure `${WORK_DIR}/rep/test.repository` and `${FIRST_WORK_DIR}/model/model.medmdl` exist.
- Feature name mismatches or multiple substring matches:
    * The script matches features by substring and will fail if it finds zero or multiple matches. Confirm naming conventions.
- Missing `med` Python package or model runtime dependencies:
    * Ensure the runtime Python environment has the `med` package and project helpers installed.

## Notes and Implementation Details

- Feature resolution is applied by rounding values to the specified resolution in `CMP_FEATURE_RES`.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/outputs/features_stats.with_missings.tsv`
- `${WORK_DIR}/outputs/graphs_with_missings/*.html`
