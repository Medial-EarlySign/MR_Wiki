

# bootstrap_app

`bootstrap_app` is a powerful and highly efficient command-line tool designed for **evaluating model performance using bootstrap analysis**. It provides key statistical metrics such as confidence intervals and standard deviations for a wide range of performance measures.

The tool uses a patient-level bootstrap sampling method. It first randomly selects a patient from the dataset, then either a random sample or all samples associated with that patient. This ensures that the analysis properly accounts for patients with multiple data points, which is a best practice in medical model assessment.

The source code can be found in the `bootstrap_app` folder of the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository.
It is compiled as part of [AllTools](../../../Installation/index.md#3-mes-tools-to-train-and-test-models).

## Getting Started: Your First Run

The easiest way to use `bootstrap_app` is from command line:

```bash
bootstrap_app --input /path/to/my_data.tsv --output /tmp/bootstrap_results
```

**Mandatory Parameters**
Only two parameters are mandatory for any run:

* `--input`: The file containing your model's predictions and the true outcomes. It must be a tab-separated TSV with a header row, including the columns `pid` (patient ID), `outcome`, and `pred_0` (the prediction score). Full File Format [MedSamples](../../../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md)
* `--output`: The path to the output file where `bootstrap_app` will write the results of the analysis.

## Core Features at a Glance

- **Highly efficient**: Quickly computes performance metrics on millions of predictions, making it suitable for large-scale datasets result files.
- **Flexible Inputs**: Supports various input types and allows for sample weighting.
- **Comprehensive Metrics**: Handles regression, categorical, and custom performance measures, including specialized metrics for binary classification.
- **Powerful Cohort Analysis**: Easily assesses model performance across thousands of defined cohorts (e.g., age groups, sex, time windows) using a simple configuration file.
- **Standalone & Integrated**: Available as a standalone executable built on a fast C++ library, with a [Python API](../../../Infrastructure%20Library/Medial%20Tools/Python/Examples.md#bootstrap-analysis-on-samples) available for integration into dataframe-based workflows.


## How it Works: Program Overview

The primary use case for `bootstrap_app` is to analyze a `MedSamples` TSV file containing patient id, outcome and prediction data. However, its main strength lies in its ability to analyze complex cohorts.

The workflow for cohort analysis involves:

1. **Defining Cohorts**: You define cohorts using a plain-text file where each filter is a simple `FEATURE_NAME:MIN_VALUE,MAX_VALUE` pair. Multiple conditions on the same line are combined with `AND` logic.
2. **Generating a Feature Matrix**: The tool can generate a feature matrix from a [MedModel JSON](../../../Infrastructure%20Library/MedModel%20json%20format.md) file and a data repository or given a matrix CSV directly in the input
3. **Applying Filters**: The tool then uses simple filtering rules, similar to pandas (even though less expressive, it is suffecient for most usecases), to create and analyze performance for each defined cohort.

This approach keeps everything within the fast C++ ecosystem, providing an efficient way to analyze performance across many sub-populations.

A single line in the `cohorts_file` can generate multiple combinations of cohorts. For instance, this example will generate 6 distinct cohorts by combining every `Age` filter with every `Time-Window` filter:

```tsv
MULTI	Age:40,89;Age:50,75;Age:45,75	Time-Window:0,365;Time-Window:180,365
```

For more information on the `cohorts_file` format/bootstrap query language, refer to the [MedBootstrap](../../../Infrastructure%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format) wiki page.

## Command-Line Options

You can view all available options by running:

```bash
./bootstrap_app --help
```

The options are organized into several logical groups:

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
- `--cohorts_file arg`: Cohort definition file ([format details](../../../Infrastructure%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format))
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


## Example Usage

The easiest way to use `bootstrap_app` is with a configuration (`.cfg`) file, which is an INI-style plain-text file instead of supplying all arguments in command line.

```bash
bootstrap_app --base_config /path/to/bootstrap_example.cfg
```


Here's an example of what a `bootstrap_example.cfg` file might look like:

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

### Explanation

While `bootstrap_app` has many options, only two are mandatory for a basic run: `input` and `output`. The **input file** is a tab-separated TSV file that must contain columns for `pid` (patient ID), `outcome`, and `pred_0` (prediction score). For more details on this format, see the [MedSamples](../../../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md) documentation.

The other parameters you see in the example, such as `rep`, `json_model`, and `cohorts_file`, are **optional** and used for advanced cohort analysis/filtering of sub population. The tool can automatically generate a feature matrix from a `json_model` and a data repository. Alternatively, you can directly provide a feature matrix as a CSV file by setting `input_type` to `features_csv` in this case, you don't need to specify `rep` or `json_model`.


## Adjusting Incidence with an Incidence File

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

The `registry_path` is a text format of [MedRegistry](../../../Infrastructure%20Library/MedProcessTools%20Library/MedRegistry). See the code documentation for more details (e.g., `write_text_file` method).


## Understanding the Results Output

The output is a TSV file with three columns: `Cohort`, `Measurement`, and `Value`.

* **Cohort**: The name of the cohort being analyzed.
* **Measurement**: The performance metric (e.g., AUC_Mean, SENS@FPR_03).
* **Value**: The calculated value for that metric.

For each metric, the tool outputs several statistics:

* `_Mean`: The average value across all bootstrap iterations.
* `_Obs`: The value from the original, non-bootstrapped data.
* `_Std`: The standard deviation across iterations.
* `_CI.Lower.95` and `_CI.Upper.95`: The lower and upper bounds of the 95% confidence interval.

- See [Bootstrap legend](Bootstrap%20legend.md) for more details on output metrics.
- Use the [utility tool to process bootstrap result files](Utility%20tools%20to%20process%20bootstrap%20results.md) to generate tables or plots (e.g., ROC curves) from one or more bootstrap files.

### Example Result Format

```tsv
Cohort	Measurement	Value
Age:40-89,Time-Window:0,365	AUC_CI.Lower.95	0.555556
Age:40-89,Time-Window:0,365	AUC_CI.Upper.95	1
Age:40-89,Time-Window:0,365	AUC_Mean	0.867092
Age:40-89,Time-Window:0,365	AUC_Obs	0.875
Age:40-89,Time-Window:0,365	AUC_Std	0.129476
...
Age:40-89,Time-Window:0,365	SENS@FPR_03	10.34565
```

## Implementation and Advanced Library Usage

You can use `bootstrap` in C++ code at three levels (main code in [MR_Libs](https://github.com/Medial-EarlySign/MR_LIBS/)):

1. `bootstrap.cpp`, `bootstrap.h` (in `Internal/MedStat/MedStat`): Basic bootstrap analysis API using standard C++ objects (e.g., vector, map). Main function: `booststrap_analyze`.
2. `MedBootstrap.cpp`, `MedBootstrap.h` (in `Internal/MedStat/MedStat`): Builds on the base API, providing a friendlier interface using MES C++ objects like `MedSamples` and `MedFeatures`.
3. `bootstrap_app`: The application itself, which receives arguments and uses the API from the [MedBootstrap](../../../Infrastructure%20Library/MedProcessTools%20Library/MedBootstrap.md) library.

For details on implementing custom metrics and extending bootstrap, see [Extending bootstrap](Extending%20bootstrap/).