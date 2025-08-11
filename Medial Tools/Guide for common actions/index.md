# Guide for Common Actions

## General Notes
1. To search within a program's help documentation, use:  
   `app --help_ $SEARCH_KEYWORDS`  
   Example: `Flow --help_ match` lists all arguments matching "match".
2. The Flow app uses "switches" to select its mode. Specify only one switch per command.  
   Example: `Flow --simple_train` activates simple training mode.

## Common Actions

### 1. Match MedSamples by Year or Criteria
See: [Using Flow To Prepare Samples and Get Incidences](/Medial%20Tools/Using%20the%20Flow%20App/Using%20Flow%20To%20Prepare%20Samples%20and%20Get%20Incidences)

### 2. Train a Model from JSON
**Simple Training:**  
```bash
Flow --simple_train --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_model $PATH_TO_OUTPUT_TO_STORE_MODEL
```
**Cross-validation:**  
See: [train_test mode](/Medial%20Tools/Using%20the%20Flow%20App/train_test%20mode)

**Optimizer for Best Parameters:**  
See: [Optimizer](/Medial%20Tools/Optimizer)  
Can be compiled in AllTools.

### 3. Calculate Model Score on Samples
**Get Model Predictions:**  
```bash
Flow --get_model_preds --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_preds $OUTPUT_PATH_TO_STORE_SAMPLES
```

### 4. Create Feature Matrix for Samples
**From Model:**  
```bash
Flow --get_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
```
**Directly from JSON:**  
```bash
Flow --get_json_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
```

### 5. Adjust Model
Add or retrain rep_processor or post_processor components. Useful for calibration or explainability.  
See: [adjust_model](/Medial%20Tools/adjust_model)  
Can be compiled in AllTools.

### 6. Change Model
Remove or modify model components (e.g., enable debug logs, test normalization).  
See: [change_model](/Medial%20Tools/change_model)  
Can be compiled in AllTools.

### 7. Simplify Model / Remove Signals
Iteratively add or remove signals to simplify the model.  
See: [Iterative Feature Selector](/Medial%20Tools/Iterative%20Feature%20Selector)  
Can be compiled in AllTools.

### 8. Analyze Feature Importance & Model Behavior
"But Why" graphs for feature validation.  
See: [Feature Importance with shapley values analysis](/Medial%20Tools/Using%20the%20Flow%20App/Feature%20Importance%20with%20shapley%20values%20analysis)

### 9. Bootstrap Performance Analysis
See: [bootstrap_app](/Medial%20Tools/bootstrap_app)

### 10. Compare/Estimate Model Performance on Different Repository
Test model on external repository.  
See: [TestModelExternal](/Medial%20Tools/TestModelExternal)  
Can be compiled in AllTools.

### 11. Create and Load Repository from Files
See: [Load new repository](/Medial%20Tools/Using%20the%20Flow%20App/Load%20new%20repository)

### 12. Create Random Splits for Train/Test/All Patients
```bash
Flow --create_splits "nsplits=$SPLIT_NUMBER" --rep $REPOSITORY_PATH --f_split $OUTPUT_PATH
```

### 13. Filter Train/Test by TRAIN Signal
```bash
FilterSamples --rep $REPOSITORY_PATH --samples $INPUT_SAMPLES_PATH --output $OUTPUT_SAMPLES_PATH --filter_train $FILTER_TRAIN_VAL
```
- TRAIN == 1: Training set (70%)
- TRAIN == 2: Test set (20%)
- TRAIN == 3: Validation set (10%)

### 14. Print Model Info
```bash
Flow --print_model_info --f_model $MODEL ...
```
Inspect trained model details.

### 15. Filter Samples by BT Cohort
Include `json_mat` even if not required by definition.
```bash
FilterSamples --filter_train 0 --rep ${REP_PATH} --filter_by_bt_cohort "Time-Window:90,730;Age:50,80;Suspected:0,0;Ex_or_Current:1,1" --samples ${INPUT} --output ${OUTPUT} --json_mat ${JSON}
```

### 16. Check Model Compatibility with Repository / Suggest Adjustments

When applying a model to a different repository, some modifications may be necessary.  
For instance, MedModel strictly checks for the presence of required signals. If a signal is missing but not critical, you can explicitly mark it as acceptable by adding a rep processor for an ["empty" signal](/Infrastructure%20Home%20Page/Rep%20Processors%20Practical%20Guide/How%20to%20create%20an%20empty%20signal).  
For further guidance, see [Flow fit_model_to_rep](../Using%20the%20Flow%20App/Fit%20MedModel%20to%20Repository).

---

## Fixing Missing Dictionary Definitions

When training on one repository and testing on another, missing diagnoses may occur.  
To find missing codes:
```bash
Flow --print_model_signals --f_model $MODEL_NAME --rep $REP --transform_rep 1 --output_dict_path $PATH
```
To resolve:
- Add missing codes to the target dictionary, matching SECTION codes as needed.
- For example:
  - Add `ICD9_CODE:786.09` if missing.
  - Add `ICD9_CODE:420-429.99` for range codes.
  - For named codes (e.g., `MALIGNANT_NEOPLASM_OF_LIP_ORAL_CAVITY_AND_PHARYNX`), find the equivalent numeric code (e.g., `140-149`) and add accordingly.

Can be compiled in AllTools
