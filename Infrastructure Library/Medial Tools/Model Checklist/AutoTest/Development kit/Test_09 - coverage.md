# Test 09: Coverage

## Purpose
Verify that the model correctly identifies and flags high-risk groups, ensuring coverage of critical populations as defined by custom rules.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `configs/coverage_groups.py`: Python file with pandas rules to define high-risk groups

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 9
```
Or include as part of the full suite:
```bash
./run.sh
```
## What This Test Does
- Uses custom rules (from `coverage_groups.py`) to define high-risk cohorts in your data
- Checks how well the model flags these groups compared to random selection
- Calculates coverage metrics and lift for each group at multiple score cutoffs

## Output Location
- Main log: `${WORK_DIR}/09.test_coverage.log`

## Example: Defining a Risk Group
Suppose we want to flag undiagnosed CKD patients with low eGFR (<65):
```python
# Use getcol to find columns in the feature matrix DataFrame "df"
eGFR = getcol(df, 'eGFR_CKD_EPI.last.win_1_360')
# Define groups in the cohort_f dictionary
cohort_f['eGFR<65'] = df[eGFR] < 65
```

## Example Output
```text
Cohort eGFR<65 :: Has 19426 patient in cohort out of 605636 (3.2%)
Analyze cutoff 1.0% with score 0.51042 => covered 2246 (11.6%), total_flag 6057 (1.0%), 37.1% has condition in flagged. Lift=11.6
Analyze cutoff 3.0% with score 0.28844 => covered 5906 (30.4%), total_flag 18170 (3.0%), 32.5% has condition in flagged. Lift=10.1
Analyze cutoff 5.0% with score 0.19112 => covered 8761 (45.1%), total_flag 30282 (5.0%), 28.9% has condition in flagged. Lift=9.0
Analyze cutoff 10.0% with score 0.09499 => covered 13650 (70.3%), total_flag 60564 (10.0%), 22.5% has condition in flagged. Lift=7.0
```

## How to Interpret Results
- Review the lift values for each cutoff: high lift means the model flags high-risk patients much more often than random
- Check the percentage of the cohort covered at each cutoff
- Use these metrics to validate that the model is useful for identifying key populations

In the example output interpertation:
The model targets patients with an eGFR below 65 (a cohort of 19,426 patients, or 3.2% of the total population of 605,636).
Using a 1% population cutoff (score≥0.51042), the model flags 6,057 patients. Within this flagged group:

* 2,246 patients (or 11.6% of the total eGFR<65 group) are correctly identified.
* The "**lift**" is 11.6, meaning the flagged patients are 11.6 times more likely to have eGFR<65 than a randomly selected patient.
* The **Precision** (or probability of having eGFR<65 in the flagged group) is 37.1% (2,246/6,057). While most flagged patients have eGFR≥65, over a third have eGFR<65.