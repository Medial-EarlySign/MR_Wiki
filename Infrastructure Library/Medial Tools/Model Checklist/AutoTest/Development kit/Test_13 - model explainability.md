
# Test 13: Model Explainability

## Purpose
Explore and interpret model predictions by analyzing real data examples of high-risk patients and identifying the most common reasons for being flagged. The analysis focuses on the top 1000 patients with the highest scores.
We want to test both model correctness and our explainability method before production.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `EXPLAINABLE_MODEL`: Path to the model with explainability features
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `EXPLAIN_JSON`: JSON for bootstrap filtering
- `EXPLAIN_COHORT`: (Optional) Filter to focus on specific explainability samples

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 13
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Uses MES explainability extension to generate explanations for model behavior ([method reference](https://patents.google.com/patent/US20240161005A1))
- Analyzes the top 1000 high-risk patients to find the most common contributing features
- Provides statistical summaries and detailed examples for exploration

## Output Location
- `$WORK_DIR/ButWhy/explainer_examples/`
	- `group_stats*.tsv`: Summary tables of the most common reasons for high scores (e.g., Smoking, COPD diagnosis, BMI, WBC)
	- `test_report.*.tsv`: Example reports for high-risk patients, showing grouped rows by risk factor from most to least important

## Example Output
**group_stats*.tsv** (summary of common reasons in high-risk patients):
```
Group    Frequency    Percentage    leading_feature_1    feature_frequency_1    leading_feature_2    feature_frequency_2    leading_feature_3
Smoking    996    99.7    Smoking.Smoking_Years    992    Smoking.Smok_Pack_Years_Max    693    Smoking.Never_Smoker
ICD9_Diagnosis.ICD9_CODE:496    537    53.8    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_10950    537    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_365    537    
BMI    405    40.5    BMI.max.win_0_1095    390    BMI.last.win_0_180    358    BMI.max.win_0_180
WBC    282    28.2    WBC.last.win_0_1095    226    WBC.last.win_0_180    198    WBC.min.win_0_180
Platelets    271    27.1    Platelets.last_delta.win_0_1095    193    Platelets.slope.win_0_1095    192    Platelets.min.win_0_180
Age    200    20    111    1    113    1    116
```

### How to Interpret this file
The most influential risk factors identified by the model are listed below, based on how frequently they appear in a patient's top three reasons for a high risk score.

We can see that the most important risk factor in that model that repeats itself is Smoking - which appears in 99.7% of the times in top 3 reasons - The leading feature inside is Smoking.Smoking_Years.
The next contributer is COPD diagnosis that appears 53.8% of the times in top 3 and than BMI - in 40.5% and then WBC 28.2%

**test_report.*.tsv** (example patient report):
```
pid    time    outcome    pred_0    Tree_iterative_covariance    Code_Description    Specific_Feature_Inside_Group(optional)...
100192    20100913    1    0.445575    Smoking:=1.51313(27.38%)        Smoking.Smoking_Years(40.13972):=0.94721(64.44%)        Smoking.Never_Smoker( 0):=0.22725(15.46%)
100192    20100913    1    0.445575    WBC:=0.70804(12.81%)        WBC.min.win_0_180(12.6):=0.151(27.51%)        WBC.last.win_0_1095(17.5):=0.11922(21.72%)        WBC.last.win_0_180(17.5):=0.11428(20.82%)
... (additional rows for other features)

100192    20100913    1    0.445575    ICD9_Diagnosis.ICD9_CODE:786:=-0.1153(2.09%)    Symptoms_involving_respiratory_system_and_other_chest_symptoms|ICD9_CODE:786    ICD9_Diagnosis.category_dep_set_ICD9_CODE:7866.win_0_365( 0):=-0.03598(72.11%)    
```

### How to Interpret this file
This output file uses SHAP values to explain how each variable contributes to a patient's final risk score.
For patient **100192**, the risk score was 0.445575, which correctly predicted the Case (Outcome=1).

* **Positive SHAP Values** (Risk-Increasing): Indicate features that push the score higher (toward greater risk).
* **Negative SHAP Values** (Protective/Risk-Decreasing): Indicate features that push the score lower.

The patient's risk is heavily dominated by two features:

1. **Smoking**: This is the main contributor, accounting for 27.38% of the total absolute SHAP value sum with a score of +1.51. The core feature, Smoking_Years, is high at 40.13, confirming a long history of smoking. 
2. **WBC (White Blood Cell Count)**: This is the second-largest factor, contributing +0.708 (or 12.81% of the total). The patient's WBC level is elevated (last measured at 17.5), which significantly increases the risk assessment.

Conversely, a specific diagnosis ICD9_Diagnosis.ICD9_CODE:786 (Symptoms_involving_respiratory_system_and_other_chest_symptoms) is shown to be slightly protective with a SHAP value of -0.11. This negative value is due to the patient lacking this diagnosis (feature value of 0) in the preceding 10 years, which mildly reduces the overall calculated risk.


## How to Interpret Results
- Use summary tables to identify the most frequent risk factors among high-risk patients
- Review individual patient reports to understand which features contribute most to their risk scores
- Look for expected patterns (e.g., Smoking as a top risk factor in lung cancer) and ensure explanations are clinically meaningful
