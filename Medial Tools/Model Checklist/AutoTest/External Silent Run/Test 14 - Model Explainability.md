# Test 14 - Model Explainability

## Purpose

Generate explainer-based reports and group-level feature summaries for the top predicted test samples. Produces group->feature mappings and a compact group statistics table.

## Required Inputs

- `WORK_DIR`: working directory with `compare/3.test_cohort.preds` and model artifacts
- `MODEL_PATH` and `EXPLAINABLE_MODEL_PATH` (model with explainability hooks; expected under `${WORK_DIR}/model/`)
- `TOP_EXPLAIN_PERCENTAGE`: integer percent (used to select top scoring samples)
- `TOP_EXPLAIN_GROUP_COUNT`: integer number of top groups to include in final stats

## How to Run
```bash
./run.specific.sh 14
```
Or run the full suite:
```bash
./run.sh
```

## What This Test Does

- Selects the top `TOP_EXPLAIN_PERCENTAGE` percent highest-scoring unique patients from `${WORK_DIR}/compare/3.test_cohort.preds` to build explainer examples.
- Runs `CreateExplainReport` against the explainer model (`EXPLAINABLE_MODEL_PATH`) and the selected samples to create `${WORK_DIR}/ButWhy/explainer_examples/test_report.tsv`.
- Reformat and aggregate the explainability output to:
    - Map groups to features and features to signal categories
    - Produce group histograms and a final `group_stats_final.tsv` containing Group, Frequency, Percentage and leading features

## Output Location

- `${WORK_DIR}/ButWhy/explainer_examples/test_report.tsv`
- `${WORK_DIR}/ButWhy/explainer_examples/group_stats_final.tsv`
- temporary files under `${WORK_DIR}/tmp/` used during reformatting

## How to Interpret Results

- `test_report.tsv` contains detailed per-sample explainer output. Use it to inspect example explanations.
- `group_stats_final.tsv` summarizes how many examples belong to each explanation group and lists top features per group — useful to prioritize group-level analyses.

## Troubleshooting

- If `CreateExplainReport` fails, run it manually with the selected sample file `${WORK_DIR}/ButWhy/explainer_examples/top.samples` to inspect errors.
- If expected groups/features are missing, check `TOP_EXPLAIN_PERCENTAGE` and `TOP_EXPLAIN_GROUP_COUNT` values (they control sample selection and report granularity).

## Files to inspect

- `${WORK_DIR}/ButWhy/explainer_examples/test_report.tsv`
- `${WORK_DIR}/ButWhy/explainer_examples/group_stats_final.tsv`
- `${WORK_DIR}/tmp/*` intermediate mapping files
