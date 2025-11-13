
# Actions Index

## Overview

This guide summarizes some tasks and workflows for working with MedSamples, models, and repositories. Each section provides a brief description and links to detailed instructions or related tools.

---

### 1. Match MedSamples by Year or Other Criteria
Subsample your data by matching medical samples based on year or other criteria. This helps remove temporal bias, ensuring your model does not learn from the sample collection time, but instead relies on independent features.

This approach is also useful for evaluating model performance when removing the information gain of a specific signal. For example, matching by age allows you to test model performance when age cannot be directly exploited as a predictor. The model still sees age, but conditioning on its value equalizes the probability of being a case, so age cannot be used for performance gain.

See: [Using Flow To Prepare Samples and Get Incidences](../Using%20the%20Flow%20App/Using%20Flow%20To%20Prepare%20Samples%20and%20Get%20Incidences.md#matching-פarameters)

### 2. Train a Model from JSON
See: [Flow](../Using%20the%20Flow%20App/index.md#training-a-model)

### 3. Calculate Model Score on Samples
See: [Flow](../Using%20the%20Flow%20App/index.md#predictingapplying-a-model)

### 4. Create Feature Matrix for Samples
See: [Flow](../Using%20the%20Flow%20App/index.md#creating-a-feature-matrix-for-samples)

### 5. Adjust Model
Add or retrain `rep_processor` or `post_processor` components for calibration, explainability, or to modify an existing model.
See: [adjust_model](../adjust_model.md)

### 6. Change Model
Remove or modify model components (e.g., enable debug logs, limit memory usage by setting smaller batch sizes).
See: [change_model](../change_model)

### 7. Simplify Model / Remove Signals
Iteratively add or remove signals to simplify the model.
See: [Iterative Feature Selector](../Iterative%20Feature%20Selector.md)

### 8. Analyze Feature Importance & Model Behavior
Analyze global feature importance, feature interactions, and the effect of each important feature or signal on model output.
See: [Feature Importance](../../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md)

Automated tests for feature importance are available: [Feature Importance Test](../Model%20Checklist/AutoTest/Development%20kit/Test_05%20-%20But%20why.md)

You can also use [model_signal_importance](../model_signals_importance.md). This tool keeps the model fixed (no retraining or signal changes), but evaluates the effect of providing or removing specific signals from the input. This is useful for frozen models to assess the impact of signal availability (e.g., if a client can or cannot provide certain inputs).

### 9. Bootstrap Performance Analysis
See: [bootstrap_app](../bootstrap_app)

### 10. Compare or Estimate Model Performance on a Different Repository, Comparre samples
TestModelExternal is a tool designed to compare differences between repositories or sample sets when applying a model. It builds a propensity model to distinguish between repositories or samples, revealing differences and enabling straightforward comparison of feature matrices. The main goal is to identify complex patterns when comparing data.
See: [TestModelExternal](../TestModelExternal.md)

### 11. Create and Load Repository from Files
See: [Load new repository](../../Infrastructure%20Library/DataRepository/Load%20new%20repository.md)

### 12. Create Random Splits for Train/Test/All Patients
See: [Using Splits](../Using%20the%20Flow%20App/Split%20Files.md#create-random-splits-for-patients)

### 13. Filter Train/Test by TRAIN Signal
```bash
FilterSamples --rep $REPOSITORY_PATH --samples $INPUT_SAMPLES_PATH --output $OUTPUT_SAMPLES_PATH --filter_train $FILTER_TRAIN_VAL
```

- `TRAIN == 1`: Training set (70%)
- `TRAIN == 2`: Test set (20%)
- `TRAIN == 3`: Validation set (10%)

### 14. Print Model Info
See: [Flow Model Info](../Using%20the%20Flow%20App/index.md#print-trained-model-information)

### 15. Filter Samples by BT Cohort
Include `json_mat` even if not required by definition.
```bash
FilterSamples --filter_train 0 --rep ${REP_PATH} --filter_by_bt_cohort "Time-Window:90,730;Age:50,80;Suspected:0,0;Ex_or_Current:1,1" --samples ${INPUT} --output ${OUTPUT} --json_mat ${JSON}
```
See: [bootstrap_app](../bootstrap_app/index.md) for details on the `--filter_by_bt_cohort` syntax.

### 16. Check Model Compatibility with Repository / Suggest Adjustments
When applying a model to a different repository, some adjustments may be needed.

For example, MedModel strictly checks for required signals. If a signal is missing but not critical, you can mark it as acceptable by adding a rep processor for an ["empty" signal](../../Infrastructure%20Library/01.Rep%20Processors%20Practical%20Guide/How%20to%20create%20an%20empty%20signal).
For more information, see [Flow fit_model_to_rep](../Using%20the%20Flow%20App/Fit%20MedModel%20to%20Repository.md).

---

## Fixing Missing Dictionary Definitions

When training on one repository and testing on another, you may encounter missing diagnoses.

To find missing codes:
```bash
Flow --print_model_signals --f_model $MODEL_NAME --rep $REP --transform_rep 1 --output_dict_path $PATH
```

To resolve:

- Add missing codes to the target dictionary, matching SECTION codes as needed.
- For example:
   - Add `ICD9_CODE:786.09` if missing.
   - Add `ICD9_CODE:420-429.99` for range codes.
   - For named codes (e.g., `MALIGNANT_NEOPLASM_OF_LIP_ORAL_CAVITY_AND_PHARYNX`), find the equivalent numeric code (e.g., `140-149`) and add it.

Can be compiled in AllTools.
