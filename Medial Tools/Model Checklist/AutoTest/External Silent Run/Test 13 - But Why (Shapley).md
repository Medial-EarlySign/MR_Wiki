# Test 13 - But Why (Shapley)

## Purpose

Produce Shapley explanations and global feature-importance visualizations for the model using the test cohort. Helps identify which features drive predictions and create per-feature explainability graphs.

## Required Inputs

- `WORK_DIR`: working directory containing repository and model artifacts
- `MODEL_PATH`: path to the fitted model (expected `${WORK_DIR}/model/model.medmdl`)
- `${WORK_DIR}/rep/test.repository` and `${WORK_DIR}/Samples/3.test_cohort.samples`

## How to Run
```bash
./run.specific.sh 13
```
Or run as part of the suite:
```bash
./run.sh
```

## What This Test Does

- Requests SHAP values from [Flow](../../../../Infrastructure%20C%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md) twice: grouped by signal category and ungrouped (full features). Outputs are written to `${WORK_DIR}/ButWhy/shapley_grouped.report` and `${WORK_DIR}/ButWhy/shapley.report`.
- Uses `feature_importance_printer.py` to generate global HTML reports:
    - `${WORK_DIR}/ButWhy/Global.html` (grouped)
    - `${WORK_DIR}/ButWhy/Global.ungrouped.html`
- Generates per-feature HTML files under `${WORK_DIR}/ButWhy/single_features/` by expanding the ungrouped SHAP report.
- Patches HTML files to use a local Plotly JS (`../js/plotly.js`).

## Output Location

- `${WORK_DIR}/ButWhy/` — contains `shapley.report`, `shapley_grouped.report`, `Global.html`, `Global.ungrouped.html`, and `single_features/` HTMLs.

## How to Interpret Results

- `Global.html` gives a ranked list of feature groups and their aggregate importance. Use it to identify which signal categories contribute most to the model.
- `single_features/` contains per-feature SHAP distribution plots useful for detailed investigation.

## Troubleshooting

- Missing model or repository: ensure `MODEL_PATH` and `${WORK_DIR}/rep/test.repository` exist.
- `Flow` failures: run the `Flow --shap_val_request` command manually to debug arguments (e.g.).
- Plotly not loading: ensure `../js/plotly.js` exists relative to the generated HTML; the test rewrites script tags to `../js/plotly.js`.

## Files to inspect

- `${WORK_DIR}/ButWhy/shapley.report`
- `${WORK_DIR}/ButWhy/shapley_grouped.report`
- `${WORK_DIR}/ButWhy/Global*.html`
- `${WORK_DIR}/ButWhy/single_features/*.html`
