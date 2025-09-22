
# TestModelExternal

TestModelExternal is a tool designed to compare differences between repositories or sample sets when applying a model. It builds a propensity model to distinguish between repositories or samples, revealing differences and enabling straightforward comparison of feature matrices. The main goal is to identify complex patterns when comparing data.

You can use this tool to:

- **Compare feature matrices from different repositories** to check model transferability and detect issues in new repositories, such as:
    - Bugs in data handling, eligibility, or client data extraction
    - Estimating expected model performance in a new repository, even without labels, using the propensity model
- **Compare samples within the same repository**, for example, to analyze data from different years and identify feature differences.

TestModelExternal is part of the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository and can be compiled under [AllTools](../Installation/index.md#3-mes-tools-to-train-and-test-models).

## Mode 1: Compare When Both Repositories Are Available

Required arguments:

- `model_path`: Path to the binary MedModel to test (required in all modes)
- `rep_test`: Repository for testing and comparison. In the propensity model, data from this repository is labeled as 1.
- `samples_test`: Path to MedSamples for the test repository
- `output`: Directory for output files
- `rep_trained`: Path to the trained model's repository (or reference repository)
- `samples_train`: Path to MedSamples from the training repository (ensure the same method/eligibility rules are used in both datasets)
- `predictor_type`, `predictor_args`: Parameters for the propensity model to distinguish between repositories
- `calibration_init_str`: Calibration arguments for the propensity model's post-processor

Optional arguments:

- `smaller_model_feat_size`: If > 0, creates an additional smaller propensity model using the top X features
- `additional_importance_to_rank`: Path to a SHAP report (from "Flow --shap_val_request") to rank differences combined with [feature importance](../Infrastructure%20C%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md)
- `features_subset_file`: File to filter features from the MedModel
- `fix_train_res`: If > 0, sets feature resolution in training to match the test set
- `sub_sample_train`: Integer to limit the maximum number of training samples (0 = no subsampling)
- `sub_sample_test`: Integer to limit the maximum number of test samples (0 = no subsampling)
- `train_ratio`: Train/test split ratio (test set is used to report propensity model performance)
- `bt_params`: Bootstrap parameters for the propensity model
- `binning_shap_params`: Parameters for SHAP report analysis on the propensity model
- `group_shap_params`: Grouping arguments for SHAP analysis
- `shap_auc_threshold`: If AUC is below this value, SHAP analysis is skipped to save time
- `print_mat`: If > 0, prints the propensity matrix (0 = labels for train samples, 1 = labels for test samples)

## Mode 2: Compare When Repositories Are Not on the Same Machine

In this mode, leave `rep_trained` and/or `samples_train` empty.

Required arguments:

- `model_path`: Path to the binary MedModel to test (required in all modes)
- `rep_test`: Repository for testing and comparison (labeled as 1 in the propensity model)
- `samples_test`: Path to MedSamples for the test repository
- `output`: Directory for output files
- `strata_json_model`: JSON file for creating strata and collecting statistics
- `strata_settings`: Strata settings for collecting statistics

When comparing to a different repository on another machine, also provide either:

- `train_matrix_csv`: A CSV matrix from the reference to compare with
- `strata_train_features_moments`: File for the reference statistics to compare with the specified path. Created in "train" repository and controled with `strata_json_model`, `strata_settings`

The `train_matrix_csv` can be created in the reference by [generating a feature matrix](Using%20the%20Flow%20App/index.md#creating-a-feature-matrix-for-samples) and is the prefered way when possible

## Mode 3: Compare Different Samples Within the Same Repository

Provide different `samples_train` and `samples_test` paths, and use the same values for `rep_train` and `rep_test` to indicate the same repository.

## Example Output

The tool creates a propensity model and generates a SHAP report for this model. It also produces a `compare_rep.txt` file, which compares feature averages and standard deviations.

You can use the resulting propensity model to assess expected performance when controlling for changes in your variables of interest.

See examples usages:

- [AutoTest - Test Matrix Over Years](Model%20Checklist/AutoTest/Development%20kit/Test_11%20-%20test%20matrix%20over%20years.md)
- [AutoTest - Compare Flags of Baseline Model vs MES Model](Model%20Checklist/AutoTest/Development%20kit/Test_15%20-%20compare%20to%20baseline%20model.md)
- [AutoTest - Estimate Performance from Propensity Model](Model%20Checklist/AutoTest/External%20Silent%20Run/Test%208%20-%20Estimate%20Performances.md)