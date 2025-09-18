# Guide for Common Actions

## Common Actions

### 1. Match MedSamples by Year or Criteria
This process allows you to subsample your data by matching medical samples based on a specific year or other defined criteria. A primary application is to eliminate the influence of temporal information from your dataset. This ensures that your model does not learn to exploit the time a sample was collected for prediction, and instead, relies on features independent of a given year.

This technique is also useful for evaluating a model's performance when you remove a specific signal information gain. For example, you can match samples by age to see how your model performs when it can't directly use age as a predictor. The model will still see age, but conditioning on its value will result equal probability to be a case, so the model will not be able to use age directly to gain performance benefit.

See: [Using Flow To Prepare Samples and Get Incidences](../Using%20the%20Flow%20App/Using%20Flow%20To%20Prepare%20Samples%20and%20Get%20Incidences.md#matching-פarameters)

### 2. Train a Model from JSON
refer to [Flow](../Using%20the%20Flow%20App/index.md#training-a-model)

### 3. Calculate Model Score on Samples
refer to [Flow](../Using%20the%20Flow%20App/index.md#predictingapplying-a-model)

### 4. Create Feature Matrix for Samples
refer to [Flow](../Using%20the%20Flow%20App/index.md#creating-a-feature-matrix-for-samples)

### 5. Adjust Model
Add or retrain rep_processor or post_processor components. Useful for calibration or explainability or adding/adjusting existing model.
See: [adjust_model](../adjust_model.md)  

### 6. Change Model
Remove or modify model components (e.g., enable debug logs, limit memory usage of the model by defining smaller batch sizes).  
See: [change_model](../change_model)  

### 7. Simplify Model / Remove Signals
Iteratively add or remove signals to simplify the model.  
See: [Iterative Feature Selector](../Iterative%20Feature%20Selector.md)  

### 8. Analyze Feature Importance & Model Behavior
Analyze Global feature importance and also features interaction and effect on model output of each important feature/signal.
See: [Feature Importance](../../Infrastructure%20C%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md)
There is also automatic test that uses those tools in model development: [Feature Importance Test](../Model%20Checklist/AutoTest/Development%20kit/Test_05%20-%20But%20why.md))

### 9. Bootstrap Performance Analysis
See: [bootstrap_app](../bootstrap_app)

### 10. Compare/Estimate Model Performance on Different Repository
Test model on external repository.  
See: [TestModelExternal](../TestModelExternal.md)  
Can be compiled in AllTools.

### 11. Create and Load Repository from Files
See: [Load new repository](../../Repositories/Load%20new%20repository.md)

### 12. Create Random Splits for Train/Test/All Patients
Please refer [Using Splits](../Using%20the%20Flow%20App/Split%20Files.md#create-random-splits-for-patients)

### 13. Filter Train/Test by TRAIN Signal
```bash
FilterSamples --rep $REPOSITORY_PATH --samples $INPUT_SAMPLES_PATH --output $OUTPUT_SAMPLES_PATH --filter_train $FILTER_TRAIN_VAL
```

- TRAIN == 1: Training set (70%)
- TRAIN == 2: Test set (20%)
- TRAIN == 3: Validation set (10%)

### 14. Print Model Info

Please refer to [Flow Model Info](../Using%20the%20Flow%20App/index.md#print-trained-model-information)

### 15. Filter Samples by BT Cohort
Include `json_mat` even if not required by definition.
```bash
FilterSamples --filter_train 0 --rep ${REP_PATH} --filter_by_bt_cohort "Time-Window:90,730;Age:50,80;Suspected:0,0;Ex_or_Current:1,1" --samples ${INPUT} --output ${OUTPUT} --json_mat ${JSON}
```
Please refer to [bootstrap_app](../bootstrap_app/index.md) to learn more on the `--filter_by_bt_cohort` syntax of filtering

### 16. Check Model Compatibility with Repository / Suggest Adjustments

When applying a model to a different repository, some modifications may be necessary.  
For instance, MedModel strictly checks for the presence of required signals. If a signal is missing but not critical, you can explicitly mark it as acceptable by adding a rep processor for an ["empty" signal](../../Infrastructure%20C%20Library/01.Rep%20Processors%20Practical%20Guide/How%20to%20create%20an%20empty%20signal).  
For further guidance, see [Flow fit_model_to_rep](../Using%20the%20Flow%20App/Fit%20MedModel%20to%20Repository.md).

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
