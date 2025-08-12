# Test_05 - But why

## Overview
Tests model feature importance with shapley
## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples path

## Output
$WORK_DIR/ButWhy:

- Global.html - global signals importance in the model
- Global.ungrouped.html - Global features importance in the mode
- single_features directory - Each of the most important feature ButWhy analysis
  - For each one of the importance feature it plots stratification of the feature value and how the model respond to each value
    - Mean outcome for each feature value - Which is probability to be a case. We can see the relation between feature value and the outcome
    - Mean score for each feature value - we can see the relation between feature value and the score (suppose to be similar to outcome graph)
    - Mean+Confidence interval of Shapley value for each feature value. We want it to behave differently then outcome in some cases. For example: Flu complications - Age is risk factor, young and old individual are at risk - U shape graph of risk as function of age.When we use BMI, BMI for little children is low - so outcome relation to BMI acts also as U shape, but model shapley values does not - It "understand" that low BMI is not reasonTo increase score (it's due to younger age which we already take into account by using age).
