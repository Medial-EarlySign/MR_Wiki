# Model Validation Checklist

## Data Distribution and Performance
- Analyze sample distribution over time: count controls and cases by year and month.
- Perform bootstrapping on the validation set (and preferably on a future time set). For the future set, also assess performance on the same patients.
    - Evaluate performance (AUC and other metrics) across years, months, and time windows.
    - Assess results by age group, sex, and key comorbidities (e.g., diabetes, COPD, CVD).
    - Check minimal membership period and presence/absence of key lab tests, if relevant.
- Assess calibration on the same samples used for bootstrapping.

## Model Analysis
- Conduct ButWhy analysis:
    - Examine global feature importance, with and without grouping signals.
    - Analyze contributions of individual features: for important features, report mean score, outcome, and Shapley value for each value bin.
- Evaluate coverage and lift for risk groups at various PR cutoffs. For example, determine the prevalence of COPD patients with hospital admissions and the proportion captured in top x, y, z PR cutoffs.
- Print feature matrix: report mean and CI/STD for each feature to identify outliers or unreasonable values (can be done on large test/train matrices).
- Compare matrices across years:
    - Analyze score distributions over multiple years.
    - Build a propensity model to differentiate between years and identify changing features.

## Fairness and Bias
- Assess fairness and bias:
    - Without matching: compare across sex, age groups, insurance, race, and socio-demographic factors.
    - With matching: control for important clinical or explanatory features.

## External and Baseline Validation
- Validate externally on different datasets.
- Compare to a simple baseline model: assess not only performance but also which patients are flagged. Use ButWhy analysis to understand population differences.

## Sensitivity and Robustness
- Perform sensitivity analysis:
    - Add noise to lab values.
    - Shift dates.
    - Remove lab values to simulate missing data.
- Ensure the model applies cleaning procedures to all signals.

---

## Applying to New Datasets Without Labels
- Compare test matrix to training repository matrix: check feature moments using [TestModelExternal](../TestModelExternal.md) or train a propensity model.
    - Also compare score distributions, both raw and after matching on key factors.
- Run ButWhy importance analysis on the test set and compare with the training repository.
- Report statistics on outliers detected by cleaning procedures.

---

## Test Kit for Model Validation
For models in development, external validation with labels, or silent run, see the tools in this repository: [https://github.com/Medial-EarlySign/MR_Tools](https://github.com/Medial-EarlySign/MR_Tools), for example under `MR_Tools/AutoValidation`.
