# Guide for common actions
## **General comments:**
1. If you want to search inside a "help" of a program for something you can run "app --help_ $SEARCH_KEYWORDS". For example to list all arguments for matching "Flow --help_ match"
2. Flow app has several "switches" that selects what the app does. You need to specify which one you want to use (please select only 1, even if you can select more then 1 and 2 different things in 1 command). For example "Flow --simple_train" will turn on the simple_train mode
## **Common Actions:**
1. ### Matching MedSamples by years or by other criteria - [Using Flow To Prepare Samples and Get Incidences](/Medial%20Tools/Using%20the%20Flow%20App/Using%20Flow%20To%20Prepare%20Samples%20and%20Get%20Incidences)
2. ### Traing a model from json:
Simplest option using Flow:
**Train model from json (simple_train)**
```bash
Flow --simple_train --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_model $PATH_TO_OUTPUT_TO_STORE_MODEL
```
A more complex option using "train_test" for cross validation - [train_test mode](/Medial%20Tools/Using%20the%20Flow%20App/train_test%20mode)
Using Optimizer to select the best option for training from several training samples and parameters of the predictor (Running the model with several XGBoost/LightGBM or other model parameters to choose the best parameters for the predictor) - [Optimizer](/Medial%20Tools/Optimizer)
Can be compiled in AllTools
###  3. Calculate score for model on samples
**Calculate score from model (get_model_preds switch)**
```bash
Flow --get_model_preds --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_preds $OUTPUT_PATH_TO_STORE_SAMPLES
```
### 4. Create feature matrix for samples from matrix
**Create feature matrix for samples from matrix (get_mat)**
```bash
Flow --get_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
# Create directly from json to store "learn matrix":
Flow --get_json_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
```
5. Adjust model - Add rep_processor or post_processor to an existig modelUseful for adding calibration/explainability post processors for and existing model (Will retrain only those components). Can be used to add rep_processor that doesn't require learning - simple cleaner, history_limit, panel_completer, etc - [adjust_model](/Medial%20Tools/adjust_model)Can be compiled in AllTools
### 6. Change model
Useful for removing components from the model or changing components information that doesn't impact training - for example turning on "debug verbose logs", testing the matrix creation with normalization and imputers, etc. - [change_model](/Medial%20Tools/change_model)
Can be compiled in AllTools
### 7. Simplifying model and removing signals
when we want to simplify a model by removing signals bottom-up (adding signals greedy  iteratively) ot top-down (removing signals greedy iteratively) - [Iterative Feature Selector](/Medial%20Tools/Iterative%20Feature%20Selector)
Can be compiled in AllTools
### 8. Analysing feature importance and model behaviour  - "But Why" graphs for important features
Important for model validation - [Feature Importance with shapley values analysis](/Medial%20Tools/Using%20the%20Flow%20App/Feature%20Importance%20with%20shapley%20values%20analysis)
### 9. Bootstrap analysis of performance
[bootstrap_app](/Medial%20Tools/bootstrap_app)
### 10. Generating MedRegistry or/and MedSamples based on config definitions -  defining an outcome
[create_registry](/Medial%20Tools/create_registry)
Can be compiled in AllTools
### 11. Compare/Estimate model performance on different repository - Can be used to test repository
[TestModelExternal](/Medial%20Tools/TestModelExternal)
Can be compiled in AllTools
### 12. Create and load repository from files:
[Load new repository](/Medial%20Tools/Using%20the%20Flow%20App/Load%20new%20repository)
### 13. Create random splits file on train/test/all patients:
**Flow create_splits**
```bash
Flow --create_splits "nsplits=$SPLIT_NUMBER" --rep $REPOSITORY_PATH --f_split $OUTPUT_PATH
```
### 14. Filter Train/Test by TRAIN signal
**Flow create_splits**
```bash
FilterSamples --rep $REPOSITORY_PATH --samples $INPUT_SAMPLES_PATH --output $OUTPUT_SAMPLES_PATH --filter_train $FILTER_TRAIN_VAL
#Will check for TRAIN == FILTER_TRAIN_VAL. If FILTER_TRAIN_VAL=1, will Filter Training set 70% of the patients, 2 - Test set 20% and 3 - validation, 10% of patients
```
### 15. Print model info
```bash
Flow --print_model_info --f_model $MODEL ...
```
Ability to inspect trained model
### 16. Filter samples by bt cohort
Note that you must include json_mat even when the bt_cohort definition do not require it.
```bash
FilterSamples --filter_train 0 --rep ${REP_PATH} --filter_by_bt_cohort "Time-Window:90,730;Age:50,80;Suspected:0,0;Ex_or_Current:1,1" --samples ${INPUT} --output ${OUTPUT} --json_mat ${JSON}
```
 
### How to fix missing dict definitions
When training model on one repository, and checking on another, some required diagnosis might be missing.
To resolve, we need to find the missing diagnosis (otherwise, in every trial Flow reports the 1st problem), and update the dictionaries.
To find:
```bash
Flow --print_model_signals --f_model $MODEL_NAME --rep $REP --transform_rep 1 --output_dict_path $PATH
```
To resolve (examples):
- missing code 786.09. Add it to target dictionary after finding ICD9_CODE:786.09 in the target dictionary, using the same SECTION code
- missing code 420-429. Add it to target dictionary after finding ICD9_CODE:420-429.99 in the target dictionary, using the same SECTION code
- missing code 'MALIGNANT_NEOPLASM_OF_LIP_ORAL_CAVITY_AND_PHARYNX'. Finding in the original dict that it is equivalent 140-149, and  add it to target dictionary after finding ICD9_CODE:140-149 in the target dictionary, using the same SECTION code
 
Can be compiled in AllTools
