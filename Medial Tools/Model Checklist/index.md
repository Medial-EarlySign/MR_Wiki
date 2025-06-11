# Model Checklist
- Samples distribution over time - #controls, #cases for each year, each month
- Bootstrap on validation set (AND prefered future time set). On future time set also asset performance on same patients
  - Performance in different years, months - AUC and other measurements
  - Performance in different time windows
  - Performance on different age groups, sex, important comorbidities (diabetes, COPD, CVD)
  - Minimal membership period, with\without important lab tests if relevant
- Calibration assesment - on same samples as bootstrap
- ButWhy analysis
  - Global feature importance with\without grouping of signals
  - Single features contribution analysis - for the important features, mean score, outcome, and shapley value contribution for each feature value bin
- Coverage/Lift on risk groups in different PR cutoffs. For examle how many COPD patients with hospital admission we have (prevalence), and how much out of them are captured in top x,y,z PR cutoffs (coverage)
- Print matrix - mean feature value and CI/STD for each feature - look for outliers and unreasonable numbers - can be done on large test/train matrtix
- Matrix differences over the years - take several years and compare
  - Check score distribution on several years
  - Build propensity model to differentite between different years and see which features changes 
- Fairness /Bias analysis
  - wihtout matching:different sex, age groups, insurance, race, socio-demographic info?
  - with matching of important features "clinical", or accepted for explanations
- External Validation on different datasets
- Compare to simple baseline model - compare not only performance, but also the flagged patients to understand who the model flags - ButWhy on the population differences 
- Sensitivity analysis to noise:
  - Noise in lab values
  - Shifting of dates
  - Missing values - removing lab values
 
**Check the model has cleaners on all signals**
 
Applying on new dataset without labels for validation:
- Test matrix difference from training repository matrix - compare feature moments with [TestModelExternal ](/Medial%20Tools/TestModelExternal)and\or try to train propensity model.
  - Also compare score distribution + score distribution after matching important factors.
- Test ButWhy importance on the test set - compare with training repo
- Stats of outliers from cleaners
 
## Test Kit for validation of models Under some stage: Development, External with labels, Silent_Run:
In this Tools git repository: [http://bitbucket:7990/scm/med/mr_tools.git](http://bitbucket:7990/scm/med/mr_tools.git) under for example: $MR_ROOT/Tools/AutoValidation. In Windows: U:\Alon\MR\Tools\AutoValidation
 
