# Test_13 - model explainability

## Overview
The goal is to "feel/taste" the data or what the model does.
We will want to see real data examples of high risk patients report + analyze most common reason for getting flagged.
It will do that analysis on top 1000 patients.

## Input
- WORK_DIR - output work directory
- EXPLAINABLE_MODEL - path for model with explainability
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- EXPLAIN_JSON - json for bootstrap filtering
- EXPLAIN_COHORT - optional filter of samples to focus on explainability samples

## Output
$WORK_DIR/ButWhy/explainer_examples

- group_stats*.tsv - Summary table of most common reasons. For example:
```
 Group    Frequency    Percentage    leading_feature_1    feature_frequency_1    leading_feature_2    feature_frequency_2    leading_feature_3
Smoking    996    99.7    Smoking.Smoking_Years    992    Smoking.Smok_Pack_Years_Max    693    Smoking.Never_Smoker
ICD9_Diagnosis.ICD9_CODE:496    537    53.8    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_10950    537    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_365    537    
BMI    405    40.5    BMI.max.win_0_1095    390    BMI.last.win_0_180    358    BMI.max.win_0_180
WBC    282    28.2    WBC.last.win_0_1095    226    WBC.last.win_0_180    198    WBC.min.win_0_180
Platelets    271    27.1    Platelets.last_delta.win_0_1095    193    Platelets.slope.win_0_1095    192    Platelets.min.win_0_180
Age    200    20    111    1    113    1    116
```
We can see the in LungFlag most important risk factor that repeats itself is Smoking - which appears in 99.7% of the times in top 3 reasons - The leading feature inside is Smoking.Smoking_Years
After it we can see COPD diagnosis that appears 53.8% of the times in top 3 and than BMI - 40.5% and then WBC 28.2%
- 
test_report.*.tsv - report example of high risk patients each several grouped rows described the same patient but with different risk factor from most important to least important. Example:
```
pid    time    outcome    pred_0    Tree_iterative_covariance    Code_Description    Specific_Feature_Inside_Group(optional)...                        
100192    20100913    1    0.445575    Smoking:=1.51313(27.38%)        Smoking.Smoking_Years(40.13972):=0.94721(64.44%)        Smoking.Never_Smoker( 0):=0.22725(15.46%)                
100192    20100913    1    0.445575    WBC:=0.70804(12.81%)        WBC.min.win_0_180(12.6):=0.151(27.51%)        WBC.last.win_0_1095(17.5):=0.11922(21.72%)        WBC.last.win_0_180(17.5):=0.11428(20.82%)        
100192    20100913    1    0.445575    Platelets:=0.48661(8.81%)        Platelets.min.win_0_180(395):=0.16023(36.41%)        Platelets.last_delta.win_0_1095(35):=0.0843(19.15%)                
100192    20100913    1    0.445575    BMI:=0.43598(7.89%)        BMI.last.win_0_180(25.53):=0.06451(21.86%)        BMI.max.win_0_1095(26.95):=0.04568(15.48%)        BMI.range_width.win_365_730(1.77):=0.03247(11.00%)        BMI.max.win_0_180(26.24):=0.03156(10.69%)
100192    20100913    1    0.445575    Neutrophils#:=0.42125(7.62%)        Neutrophils#.range_width.win_365_730(21.49):=0.06566(20.60%)        Neutrophils#.std.win_365_730(6.09858):=0.0565(17.73%)        Neutrophils#.range_width.win_0_1095(24.1):=0.051(16.01%)        
100192    20100913    1    0.445575    ICD9_Diagnosis.ICD9_CODE:496:=0.29496(5.34%)    496|Chronic_airway_obstruction_not_elsewhere_classified|ICD9_CODE:496|ICD9_DESC:496:Chronic_airway_obstruction_not_elsewhere_classified    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_10950( 1):=0.33176(93.77%)    496|Chronic_airway_obstruction_not_elsewhere_classified|ICD9_CODE:496|ICD9_DESC:496:Chronic_airway_obstruction_not_elsewhere_classified    ICD9_Diagnosis.category_dep_set_ICD9_CODE:496.win_0_365( 0):=-0.02205(6.23%)    496|Chronic_airway_obstruction_not_elsewhere_classified|ICD9_CODE:496|ICD9_DESC:496:Chronic_airway_obstruction_not_elsewhere_classified            
100192    20100913    1    0.445575    Triglycerides:=0.23074(4.18%)        Triglycerides.range_width.win_0_1095( 0):=0.08213(60.18%)        Triglycerides.max.win_0_1095(69):=0.04217(30.90%)                
100192    20100913    1    0.445575    Hematocrit:=0.19547(3.54%)        Hematocrit.min.win_0_1095(37.9):=0.0481(45.39%)        Hematocrit.slope.win_0_1095(-0.62271):=0.0296(27.94%)                
100192    20100913    1    0.445575    Neutrophils%:=0.16415(2.97%)        Neutrophils%.range_width.win_0_1095(50.2):=0.08764(37.97%)        Neutrophils%.min.win_0_1095(30.8):=0.06082(26.36%)                
100192    20100913    1    0.445575    ICD9_Diagnosis.ICD9_CODE:786:=-0.1153(2.09%)    786|Symptoms_involving_respiratory_system_and_other_chest_symptoms|ICD9_CODE:786|ICD9_DESC:786:Symptoms_involving_respiratory_system_and_other_chest_symptoms    ICD9_Diagnosis.category_dep_set_ICD9_CODE:7866.win_0_365( 0):=-0.03598(72.11%)    786.6|Swelling_mass_or_lump_in_chest|ICD9_CODE:7866|ICD9_CODE:786.6|ICD9_DESC:786.6:Swelling_mass_or_lump_in_chest    ICD9_Diagnosis.category_dep_set_ICD9_CODE:7866.win_0_10950( 0):=-0.0075(15.03%)    786.6|Swelling_mass_or_lump_in_chest|ICD9_CODE:7866|ICD9_CODE:786.6|ICD9_DESC:786.6:Swelling_mass_or_lump_in_chest            
SCORES    100192    20100913    ###                                    
PID_VIEWER_URL    =HYPERLINK("http://node-04:8196/pid,100192,20100913,prediction_time,Smoking_Status&Smoking_Duration&P_White&P_Red&Platelets&P_Diabetes&P_Cholesterol&P_Liver&P_Renal&ICD9_Diagnosis&Race&Lung_Cancer_Location","Open Viewer")                                            
```
We can see a single patient 100192 that recieved score 0.445575 on time 20100913 and is indeed a case (outcome is 1). The main reason is Smoking, shap value of 1.51 (27.38% of the shap values sum in absolute). the main feature is Smoking_Years which is 40.13 and Never_smoker is 0 so he is current or past smoker. 
Then WBC with 0.708 of shap value (12.81%), the minimum WBC was 12.6 which is quite high and last value was 17.5. 
We can see for example that "ICD9_Diagnosis.ICD9_CODE:786" is negative - protective with low value of -0.11. The feature ICD9_Diagnosis.category_dep_set_ICD9_CODE:7866.win_0_10950  has value of "0" So patient doesn't have this diagnosis in the past 10 years.
