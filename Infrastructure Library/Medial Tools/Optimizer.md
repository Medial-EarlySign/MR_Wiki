
## Overview

The Optimizer is designed to tune the hyperparameters of your model. It evaluates performance on both the test set and the training set (to assess overfitting and generalization error). A penalty factor, controlled by the `generelization_error_factor` argument, is applied when selecting the best configuration if the generalization error is high.

The Optimizer saves its progress, so if a failure occurs, it can resume from where it left off (unless the override flag is set or output folders are deleted). This is especially useful for long-running processes.

Although the main focus is on `MedPredictor` parameters, you can also specify sample weights and different training samples, and combine these options as needed. The Optimizer is part of the [AllTools](../../Installation/index.md#3-mes-tools-to-train-and-test-models) compilation.



## Arguments

- `--rep`: Path to the repository.
- `--train_samples_files`: File with training samples (one per line). Optionally, two extra columns for case/control values (comma-separated).
- `--test_samples_files`: File with test samples (one per line). Optionally, two extra columns for case/control values (comma-separated).
- `--train_test_samples_single` (default: 0): If true, `train_samples_files` and `test_samples_files` are used directly as MedSamples (not as file paths). Useful when there is only one MedSamples option for training.
- `--splits_file`: File specifying splits (IDs separated by spaces).
- `--train_cases_labels`: Comma-separated values defining cases for training. If empty, no transformation.
- `--train_control_labels`: Comma-separated values defining controls for training. If empty, no transformation.
- `--test_cases_labels`: Comma-separated values defining cases for testing.
- `--test_control_labels`: Comma-separated values defining controls for testing.
- `--train_till_time` (default: -1): If >0, filters training data up to this time; data after is used for testing.
- `--change_to_prior` (default: -1): If >0, randomly subsamples cases/controls to reach this prior.
- `--down_sample_train_count` (default: 0): If not zero, downsamples training set to this count.
- `--down_sample_test_count` (default: 0): If not zero, downsamples test set to this count.
- `--json_model`: Path to the model JSON file.
- `--matching_strata` (default: "Time,year,1"): Strata arguments for matching.
- `--matching_json`: JSON for matching, if required.
- `--matching_change_to_prior` (default: -1): If >0, matches to this ratio (overrides `price_ratio`).
- `--price_ratio` (default: 0): If 0, no matching. If <0, assigns weights. Otherwise, performs matching.
- `--nfolds` (default: 6): Number of folds for splitting training data.
- `--split_sel` (default: 0): Number of splits to use for model selection. 0 means all.
- `--train_weights_method_file`: If set, trains with all weight options listed in this file (one per line).
- `--ms_predictor_name` (default: xgb): Predictor name for model selection.
- `--ms_configs_file`: Model selection file. Each parameter is assigned with =. Use commas to specify multiple options for a parameter (see example below).
- `--generelization_error_factor` (default: 5): Penalty factor for generalization error (overfitting) between train and test. Should be >1.
- `--result_folder`: Output folder for results.
- `--config_folder`: Output folder for configuration files.
- `--min_age_filter` (default: 0): Minimum age filter.
- `--max_age_filter` (default: 120): Maximum age filter.
- `--min_year_filter` (default: 0): Minimum year filter for sample time.
- `--max_year_filter` (default: 3000): Maximum year filter for sample time.
- `--use_same_splits` (default: 1): If true, uses the same splits for different training samples (assumes all have the same samples).
- `--bt_json`: JSON file for creating features for bootstrap cohort filtering.
- `--bt_cohort`: Cohort line for filtering (no support for Multi or name, only filter definition).
- `--bootstrap_args`: Bootstrap parameters.
- `--bootstrap_measure` (default: AUC_Obs): Measure for bootstrap.


## Example: `lightgbm_model.options` File

```ini
verbose=0
silent=2
num_threads=15
num_trees=200
metric=auc
objective=binary
learning_rate=0.01,0.03,0.05
lambda_l2=0
metric_freq=1000
min_data_in_leaf=100,500,1000,2000
feature_fraction=0.8,1
bagging_fraction=0.8
bagging_freq=5
max_bin=250
boosting_type=gbdt
max_depth=0,5,6,7
min_data_in_bin=50
```



## Output

The Optimizer creates two output folders, set by `--result_folder` and `--config_folder`:

- **config_folder**: Stores the final model, cross-validation results, and a text file with the selected parameters.
- **result_folder**: Contains detailed results for each cross-validation split and a summary file for hyperparameter tuning. For each configuration, it reports performance on both the test and training splits (to assess overfitting).