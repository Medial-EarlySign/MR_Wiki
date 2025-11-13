
# model_signals_importance

## Overview

The `model_signals_importance` tool systematically evaluates how specific groups of signals contribute to your model’s performance. It does this by comparing the model’s results with and without selected signals, without retraining the model. The model remains fixed; the tool simply tests the effect of removing signals from the input.

This analysis is useful for:

- **Model Interpretability**: Quantifies the impact of each signal or group.
- **Feature Selection**: Identifies redundant or low-impact signals that can be removed, simplifying the model and reducing data requirements.
- **Performance Benchmarking**: Shows the expected performance drop if a signal becomes unavailable.

---

## Command Line Parameters

- `--rep`: Path to the data repository.
- `--samples`: Path to the raw data samples.
- `--model_path`: Path to the pre-trained model.
- `--output`: Path to save the output report.
- `--skip_list <comma-delimited list>`: A comma-separated list of signals to exclude from the analysis, such as Age,Gender. These are typically signals that are always present and not under evaluation.
- `--no_filtering_of_existence`: Disables the default behavior of filtering the test cohort to include only samples where the signal exists. When this flag is used, performance is measured on all samples, regardless of the signal's presence.
- `--features_groups <path>`: A file mapping features to logical group names (e.g., all CBC features to the CBC group). This can be a tab-delimited file or a keyword like BY_SIGNAL_CATEG to group features by their originating source.
- `--group2signal <path>`: (Optional) Path to a tab-delimited file with two columns: group name (from `features_groups`) and a comma-separated list of signals. This remaps groups to the actual signals to exclude during testing. Can help when the "features_groups" defined for ButWhy are not input signals and you want to map them to input signals.
- `--measure_regex <string>`: A regular expression string (e.g., `"AUC|SENS@FPR_03"`) that specifies which performance metrics to include in the output report.

You can also specify filtering arguments with `--bt_filter` arguments like we do in [FilterSamples](FilterSamples.md)

## How It Works

The tool uses a flexible two-step process to define which signals to test for importance:

1. **Feature-to-Group Mapping**: Reads the `--features_groups` file to map each feature to a group. Like happens in ButWhy analysis
2. **Group-to-Signal Mapping**: Uses the `--group2signal` file to determine the final signals to exclude for each test. If a group name from the `features_groups` file is found in `group2signal`, the listed signals are used; otherwise, the group name itself is treated as the signal to test.

This process allows for testing the importance of either individual groups or multiple combined groups at once.

For each group defined by this process, the tool performs the following steps:

1. **Cohort Identification**: Determines the cohort of samples where the input signal is present within the specified time window. When `--no_filtering_of_existence` it will just calculate the cohort size and will not filter the samples to that cohort.
2. **Performance with Signals**: Measures the model's performance on this cohort with all signals included. The result is labeled with a `:with_signals` suffix.
3. **Performance Without Signals**: Measures the model's performance on the same cohort after omitting the input signal. This result is labeled with a `:no_signals` suffix.
4. **Difference Calculation**: Calculates the performance difference, labeled with a `:difference` suffix, which quantifies the signal's impact.

All results are stored in a final output table.

## Example Usage

```bash
model_signals_importance --model_path my_model.bin --features_groups feature_groups.tsv --group2signal group_mapping.tsv --skip_list Age,Gender --no_filtering_of_existence --time_windows 0,365
```

In this example:

- The base model is `my_model.bin`.
- `feature_groups.tsv` maps features to groups.
- `group_mapping.tsv` defines which signals to test for each group.
- `Age` and `Gender` are skipped.
- Signals are tested without filtering for their existence in the `0,365` day window. The report will show how many samples have each signal, but performance is measured on all data, not just those with the signal present. If `--no_filtering_of_existence` was not given, the performance was assess only with the cohort where the signal presents.

## Output

The tool outputs a report comparing model performance on the full dataset versus performance with each signal group removed. The report typically includes a metric (e.g., AUC) and the performance drop, giving a clear, quantitative measure of each signal’s importance.

### Example output

| Test Description | #samples| #Unique_patients | #controls | #cases | AUC_Mean | AUC_Lower | ACU_Upper | SENS@FPR_03_Mean | SENS@FPR_03_lower | SENS@FPR_03_upper |
| ---------------- | ------- | ---------------- | --------- | ------ | -------- | --------- | --------- | ---------------- | ----------------- | ----------------- |
| Group:CBC:time_window:365:with_signals | 1000000 |	710053 |	997015 |	2985 | 0.824535 |	0.817392 |	0.832693 |	36.8828 |	34.9927 |	38.8223 |
| Group:CBC:time_window:365:no_signals |	1000000 |	710053 |	997015 |	2985 |	0.743143 |	0.735234 |	0.751862 |	14.5724 |	13.219 |	15.9436 |
| Group:CBC:time_window:365:difference |	1000000 |	710053 |	997015 |	2985 |	0.0813916 |	EMPTY |	EMPTY |	22.3104 |	EMPTY |	EMPTY |

For instance, in the example table, removing the CBC signal group resulted in a **0.08 point drop in AUC**, highlighting its importance.