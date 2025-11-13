
# Test 12: Fairness

## Purpose
Assess model fairness by comparing performance (e.g., sensitivity) across sensitive groups at the same score cutoff. The goal is to ensure similar probability of being flagged by the model when you are a case, regardless of group (e.g., gender, ethnicity).

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `BT_JSON_FAIRNESS`: Bootstrap JSON for filtering cohorts
- `FAIRNESS_BT_PREFIX`: Bootstrap cohort definition for fairness testing
- `config/fairness_groups.cfg`: Defines the groups to compare
	- Each line: two or more group definitions ([bootstrap cohort filter format](../../../../../Infrastructure%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format), separated by `|`), tab-delimited with display names (also separated by `|`)
	- Example:
		```tsv
		Gender:1,1|Gender:2,2	Males|Females
		```

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 12
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Uses cohort definitions from `fairness_groups.cfg` to compare model performance across groups
- Calculates AUC, sensitivity and specificity, at common cutoffs (5%, 10%)
- Performs statistical tests (chi-square) to assess significance of differences
- If unfairness is detected, applies matching (e.g., by age) and re-evaluates fairness

## Output Location
- `$WORK_DIR/fairness/`
	- `fairness_report.tsv`: Summary table comparing sensitivity, specificity, and AUC at 5% and 10% cutoffs
	- `fairness_report.*`: Statistical chi-square results for sensitivity differences (one file for each cutoff)
	- `Graph_fairness`: Plots sensitivity vs. score threshold for each group (with confidence intervals)
	- `graph_matched`: Plots after matching (e.g., by age) if fairness is not met

## How to Interpret Results
- Look for low chi-square values and similar sensitivity across groups in `fairness_report.tsv`
- Use `Graph_fairness` to visually compare sensitivity curves
- If needed, review matched results in `graph_matched` to see if fairness improves
