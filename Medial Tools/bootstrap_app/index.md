

# bootstrap_app

`bootstrap_app` is a high-performance tool for evaluating model performance using bootstrap analysis. It outputs confidence intervals, standard deviations, and other statistics for each metric.

The tool operates by first randomly selecting a patient from the dataset, then either randomly choosing a prediction date/sample for that patient or selecting all their samples. This method ensures that patients with more samples have a proportionate impact on performance metrics. In medical model assessment, it is best practice to randomize by patient ID first, then select all or a random subset of their prediction dates.



## Key Features

- Highly efficient: computes performance metrics on millions of predictions in seconds.
- Supports sample weights for metric calculation.
- Handles regression, categorical, and custom performance measures.
- Easily assesses performance across multiple cohorts (e.g., age, sex, time windows, disease stage) using a simple API or config file scalable to thousands of cohort definitions.

The application is a standalone executable built on a fast C++ library. You can also use the [Python API](../../Python/Examples.md#bootstrap-analysis-on-samples) for dataframe-based workflows that uses the same library.

Source code is available in the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository (`bootstrap_app` folder), and it is compiled as part of [AllTools](../../Installation/index.md#3-mes-tools-to-train-and-test-models).



## Program Overview

The simplest use case is to read a `MedSamples` TSV file containing outcome and prediction columns (e.g., `outcome`, `pred_0`) and assess model performance. However, the main strength of `bootstrap_app` is its ability to define and analyze complex cohorts.

You can generate a feature matrix using a [MedModel JSON](../../Infrastructure%20C%20Library/MedModel%20json%20format.md) and a repository. Once you have a feature matrix, you can filter rows using simple rules, similar to pandas filtering in Python.

Cohorts are defined in a plain-text file, where each filter is written as `FEATURE_NAME:MIN_VALUE,MAX_VALUE`. Multiple conditions are combined with AND logic. This format is easy to read and sufficient for most use cases, even if less expressive than pandas, and keeps everything within the C++ ecosystem.


## Program Options

To see all available options, run:

```bash
./bootstrap_app --help
```



### General Options
- `--sample_seed arg (=0)`: Seed for bootstrap sampling
- `--use_splits`: Perform split-wise analysis in addition to full data
- `--run_id arg (=run_id_not_set)`: Run ID to store in the result file
- `--debug`: Enable verbose debugging
- `--output_raw`: Output bootstrap filtering of label and prediction (for inspection)




### Input/Output Options
- `--rep arg`: Repository path (for cohort filtering, if needed)
- `--input_type arg (=samples)`: Input type (`samples`, `samples_bin`, `features`, `medmat_csv`, `features_csv`)
- `--input arg`: Input file location
- `--weights_file arg`: File with sample weights (same order as input), or use `attr:` prefix to extract attribute from samples
- `--control_weight arg (=-1)`: If >0, use this value to weight controls (simple alternative to `weights_file`)
- `--cohorts_file arg`: Cohort definition file ([format details](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format))
- `--cohort arg`: Analyze a single cohort by providing a string (e.g., `Time-Window:0,365;Age:40,80`); overrides `--cohorts_file`
- `--json_model arg`: JSON model for creating features for cohort filtering (input for `cohorts_file`)
- `--output arg`: Output file location for bootstrap results



### Bootstrap Metrics/Measurement Options
- `--measurement_type arg`: Which measures to perform. Options: `calc_regression`, `calc_kandel_tau`, `calc_harrell_c_statistic`, `calc_multi_class`, `calc_roc_measures_with_inc`, `calc_only_auc`, `calc_npos_nneg`. Default: `calc_roc_measures_with_inc` (recommended for binary classification).
- `--general_measurements_args arg`: Arguments for the measurement init function (as `key=value;` string)



### Binary Classification Metrics Options
For binary classification, you can specify many arguments directly (instead of using `general_measurements_args`):
- `--max_diff_working_point arg (=0.05)`: Maximum allowed difference between calculated and requested working point (otherwise, returns missing value)
- `--force_score_working_points`: Force using scores as working points (reports results as a function of score cutoff only)
- `--min_score_quants_to_force_score_wp arg (=10)`: If the prediction file has fewer than this number of score bins, performance is reported only by score cutoffs
- `--working_points_sens arg`: Sensitivity working points (comma-separated, 0-100%)
- `--working_points_fpr arg`: FPR working points (comma-separated, 0-100%)
- `--working_points_pr arg`: Precision-recall working points (comma-separated, 0-100%)
- `--part_auc_params arg`: Partial AUC points (comma-separated, 0-1)

**Explanation:** Performance metrics are reported as "Metric @ Other Metric Cutoff". There are two main ways to define cutoffs:

1. By score threshold: reported as `@SCORE_X` (e.g., `SENS@SCORE_0.5`). If the score has few bins (e.g., binary), results are reported only this way. The parameters `min_score_quants_to_force_score_wp` and `force_score_working_points` control this behavior.
2. By another metric: e.g., sensitivity at a fixed FPR (e.g., `SENS@FPR_03`). See the [metrics legend](Bootstrap%20legend.md) for details. You can also extract the score cutoff at a given FPR (e.g., `SCORE@FPR_03`). This is useful for extracting KPIs by controlling FPR, PR, or sensitivity directly.


### Multi-Class Metrics Options
- `--multiclass_top_n arg (=1,5)`: In multiclass mode, top N predictions to consider (comma-separated)
- `--multiclass_dist_name arg`: Name of distance function (e.g., Jaccard, Uniform)
- `--multiclass_dist_file arg`: File with distance metric
- `--multiclass_auc arg (=0)`: Perform class-wise AUC in multi-class analysis



### Bootstrapping Parameters
- `--score_resolution arg (=0.0001)`: Score bin resolution for speed (set to 0 for no rounding)
- `--score_bins arg (=0)`: Number of score bins for speed (set to 0 to disable)
- `--nbootstrap arg (=500)`: Number of bootstrap iterations
- `--fix_label_to_binary arg (=1)`: If set, treats labels as `label = outcome > 0` (enforces binary labels)



### Bootstrap Sampling Options
- `--sample_per_pid arg (=1)`: Number of samples to take per patient (0 = take all samples for a randomized patient)
- `--sample_pid_label`: If true, randomization is based on patient and label (default: false)
- `--do_autosim`: Perform auto simulation (requires `min_time` and `max_time`)
- `--min_time arg`: Minimum time for auto simulation
- `--max_time arg`: Maximum time for auto simulation
- `--sim_time_window`: Treat cases as controls if not in time window (do not censor)
- `--censor_time_factor arg (=2)`: When `sim_time_window` is on, factor for censoring cases (1 = all cases beyond window become controls without censoring)



### Bootstrap Filtering Options
- `--whitelist_ids_file arg`: File with whitelist of IDs to include
- `--blacklist_ids_file arg`: File with blacklist of IDs to exclude
- `--sample_min_year arg (=-1)`: Filter out samples before this year (no filtering if < 0)
- `--sample_max_year arg (=-1)`: Filter out samples after this year (no filtering if < 0)
- `--use_censor arg (=1)`: Use repository censor signal (deprecated)

you may not provide this file or override all parameter with command arguments.

### Incidence Adjustments (Advanced)
See [Fixing incidence](#fixing-incidence-with-incidence-file) for more details.
- `--incidence_file arg`: Path to incidence file (age/sex stratified, e.g., from SEER) to adjust incidence for metrics sensitive to incidence rate
- `--registry_path arg`: Registry path for calculating incidence by sampling in the current repository (use only for non-case-control data)
- `--labeling_params arg (=conflict_method=max;label_interaction_mode=0:within,all|1:before_start,after_start;censor_interaction_mode=all:within,all)`: How to label from registry (see `LabelParams` type)
- `--incidence_sampling_args arg (=start_time=20070101;end_time=20140101;time_jump=1;time_jump_unit=Year;time_range_unit=Date)`: Initialization string for `MedSamplingYearly`
- `--do_kaplan_meir arg (=1)`: Use Kaplan-Meier calculation for incidence by registry (recommended, especially for large time windows)


## Example Run

```bash
bootstrap_app --base_config /nas1/Work/Users/Alon/UnitTesting/examples/bootstrap_app/bootstrap_example.cfg
```

The `bootstrap_example.cfg` file contains all program arguments in INI format (`parameter_name = parameter_value`). You can use this file or override parameters with command-line arguments.

Example `bootstrap_example.cfg`:

```ini
# Repository path:
rep = /home/Repositories/THIN/thin_jun2017/thin.repository
# MedSamples input (or use `input_type` for other types)
input = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/validation_samples.preds
# Output path:
output = /tmp/bootstrap_test
# JSON model for additional features for cohort filtering
json_model = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/model_stats.json
# Cohorts definition file:
cohorts_file = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/bootstrap_new.params
```

For the exact format of `cohorts_file`, see the [MedBootstrap](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format) wiki page or the [doxygen documentation](https://Medial-EarlySign.github.io/MR_LIBS/classMedBootstrap.html#a719ddf45e236146cd0020b0f587b78a1).


## Fixing Incidence with an Incidence File

The tool estimates average incidence in your cohort based on sex, age group, and patient counts. For positive predictive value (PPV), it multiplies sensitivity by incidence, then divides by `sensitivity * incidence + FPR * (1 - incidence)`. This is equivalent to weighting cases as `average incidence * total cohort / total cases` and controls as `(1 - average incidence) * total cohort / total controls`.

If the model is random (sensitivity = FPR), then PPV equals incidence. The bootstrap program also evaluates how additional cohort filters (beyond sex and age) affect incidence. For example, selecting anemic patients may bias toward cases and increase incidence compared to the global population (e.g., SEER data). The tool assumes the effect on stratified outcome, age, and sex is similar between your input samples and the reference population, and measures the lift in odds ratio before and after applying bootstrap filters. This is an adjustment for incidence-sensitive metrics, not an exact calculation.

Example incidence file (can be created via Flow App):

```bash
head /nas1/Work/Users/Alon/UnitTesting/examples/bootstrap_app/pre2d_incidence_thin.new_format
```
```
AGE_BIN 3
AGE_MIN 21
AGE_MAX 90
OUTCOME_VALUE   0.0
OUTCOME_VALUE   1.0
STATS_ROW       MALE    21      1.0     5242
STATS_ROW       MALE    21      0.0     94758
STATS_ROW       FEMALE  21      1.0     5242
STATS_ROW       FEMALE  21      0.0     94758
STATS_ROW       MALE    24      1.0     5338
```

The `registry_path` is a text format of [MedRegistry](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry). See the code documentation for more details (e.g., `write_text_file` method).


## Results Output File

- See [Bootstrap legend](Bootstrap%20legend.md) for details on output metrics.
- Use the [utility tool to process bootstrap result files](Utility%20tools%20to%20process%20bootstrap%20results.md) to generate tables or plots (e.g., ROC curves) from one or more bootstrap files.


## Implementation and Advanced Library Usage

You can use `bootstrap` in C++ code at three levels (main code in [MR_Libs](https://github.com/Medial-EarlySign/MR_LIBS/)):

1. `bootstrap.cpp`, `bootstrap.h` (in `Internal/MedStat/MedStat`): Basic bootstrap analysis API using standard C++ objects (e.g., vector, map). Main function: `booststrap_analyze`.
2. `MedBootstrap.cpp`, `MedBootstrap.h` (in `Internal/MedStat/MedStat`): Builds on the base API, providing a friendlier interface using MES C++ objects like `MedSamples` and `MedFeatures`.
3. `bootstrap_app`: The application itself, which receives arguments and uses the API from the [MedBootstrap](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedBootstrap.md) library.

For details on implementing custom metrics and extending bootstrap, see [Extending bootstrap](Extending%20bootstrap/).