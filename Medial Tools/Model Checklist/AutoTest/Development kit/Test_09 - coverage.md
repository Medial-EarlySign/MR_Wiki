# Test_09 - coverage

## Overview
Tests that the model flags expected high risk population. The high risk population is defined by rule based like age, and other features.
 
## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- configs/coverage_groups.py - rules with pandas to define the groups
 
## Output
$WORK_DIR}/09.test_coverage.log
We defined a "risk" group for undiagnosed CKD by taking patients with low egfr level < 65.
We defined the group like this in coverage_groups.py
```python
# Usage with getcol to search for columns inside "df" DataFrame. The DataFrame is created based on model feature matrix.
eGFR=getcol(df, 'eGFR_CKD_EPI.last.win_1_360')
# Define Groups and store in dictionary "cohort_f" - The key is the name of the cohort, Value is the filter with pandas on DataFrame "df". 
cohort_f['eGFR<65'] = df[eGFR]<65
```
Example output:
```
Cohort eGFR<65 :: Has 19426 patient in cohort out of 605636 (3.2%)
Analyze cutoff 1.0% with score 0.51042 => covered 2246 (11.6%), total_flag 6057 (1.0%), 37.1% has condition in flagged. Lift=11.6
Analyze cutoff 3.0% with score 0.28844 => covered 5906 (30.4%), total_flag 18170 (3.0%), 32.5% has condition in flagged. Lift=10.1
Analyze cutoff 5.0% with score 0.19112 => covered 8761 (45.1%), total_flag 30282 (5.0%), 28.9% has condition in flagged. Lift=9.0
Analyze cutoff 10.0% with score 0.09499 => covered 13650 (70.3%), total_flag 60564 (10.0%), 22.5% has condition in flagged. Lift=7.0
```
We can see that there are 19426 that meets the criteria eGFR<65 out of 605636 which is 3.2%.
We can see results for several cutoffs - But in all cutoffs the "lift" is high - for example 11.6 in cutoff of 1% (which is 0.51042) - so patients in this group are getting flagged 11.6 more times then random patient.
This captures 2246 patients out of all 19426 patients with eGFR<65, which is 11.6%. Cutoff of 1% which is score>=0.51042 flags 6057 which is indeed 1% out of population 605636.
The probability to have eGFR<65 in the flagged population is 37.1% (2246 / 6057) - so most patients that are getting flagged are with last eGFR>65 (not trivial) but many of them 37.1% with eGFR<65.
 
 
