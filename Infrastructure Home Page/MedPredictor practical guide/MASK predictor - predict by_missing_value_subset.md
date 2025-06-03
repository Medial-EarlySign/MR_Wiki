# MASK predictor - predict by_missing_value_subset
****
When a model uses BMI (for example), and a sample has no BMI, the 'standard' approach is leave the relevant features as NaN or impute (impute is usually better).
MASK model takes a different approach - it would score the sample based on a model trained without BMI.
****
****
```
PARAMS="predictor_type=xgb;masks_params=Smoking_Intensity|BMI|Fev1|Hemoglobin,Hematocrit,Platelets,WBC,MCH,Eosinophils%,Neutrophils%,Neutrophils#,RDW,RBC,MCHC-M|ALT,ALKP,Albumin;masks_tw=0,365,365,365,365;predictor_params=${XGB_PARAMS}"
```
A mask is list of signals, separated by ",". Masks are separated by "|". This example has 5 masks:
- Mask 0: Smoking_Intensity
- Mask 1: BMI
- Mask 2: Fev1
- Mask 3: Hemoglobin,Hematocrit,Platelets,WBC,MCH,Eosinophils%,Neutrophils%,Neutrophils#,RDW,RBC,MCHC-M
- Mask 4: ALT,ALKP,Albumin
****
** **- the code would train 2 power #masks predictors. In this example - 32 predictors, each with parameter as in predictor_params, but with different list of features:
- Predictor 0 includes all the features.
- Predictor 1 includes all the features but those associated with mask 0.
- Predictor 2 includes all the features but those associated with mask 1.
- Predictor 3 includes all the features but those associated with mask 1 and mask 0.
- ...
- Predictor 10 includes all the features but those associated with mask 3 and mask 1.
The mask code supports only these features:
- Signals with features of type "last in time window", e.g. WBC.last.win_0_to_365
  - 365, the time window for looking for missing value in predict, see next, is defined in the parameter mask_tw
  - If WBC is signal in a mask, all WBC features would be dropped (and not just the 'indicator feature' WBC.last.win_0_to_365)
- Smoking Intensity - the masks would drop smoking pack years features as well (as one is calculated from the other plus smoking duration)
For every Predictor, we run Calibrator, so score is risk, and it makes more sense to compare scores coming from different predictors (in bootstrap after predict) 
** **- to chose the right model per sample:
- For every mask, the code checks if more than 50% of the signals are missing.
- 
To check if a feature is missing, we look in features.masks, so predict should look like
```
Flow --get_model_preds --rep $REP --f_samples $SAMPLES --f_model $MODEL --f_preds $PREDS --change_model_init "object_type_name=MedModel;change_command={generate_masks_for_features=1}" 
```
- Every mask has time window, given in the mask_tw parameter.
  - For mask 1, BMI, the time window in the example is 365. The code check if BMI.last.win0_to_365 is missing.
  - If a mask has more than one feature, e.g. Mask 3 in the example, it would check for 50% missing or more.
  - Smoking Intensity is treated differently - time window is irrelevant and the code check whether the signal exists ever or not.
- Based on the relevant masks for each sample, the right predictor is chosen.
- In the above example, if a sample has no Smoking Intensity ever, and no BMi in the last 365 days, but he has Fev1 in the last 365 days as well as the majority of signals from Mask 4 and 5, then his score would come from predictor 3.
- Standard output of predict (per prediction batch) includes:
  - frequency of each mask - % of missing values per mask
  - frequency of predictor used
The predictor return scores before and after calibration.
****
- How to choose features for masks?
  - Based on feature importance
  - Grouped by blood panels
  - If Some signals are highly correlated, they should be in the same mask (because if we mask one of them, the sub-model will use the other one)
****
We ran two tests:
- LungFlag: train on KP, tests mostly on THIN
- AAA: train and test on Geisinger with cross validation
In both cases we saw no significant change from XGB straightforward, with and without calibration 
Note that for each model we used the same XGB parameters as in the full model - i.e. we haven't run optimization on top of the mask model, as we cannot do it in our current infrastructure and we decided to skip testing it manually.
We hoped for better results. But, the good news is the strength of XGB  
 
 
 
 
