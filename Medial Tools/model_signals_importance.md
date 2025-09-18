
# model_signals_importance

## Overview

The `model_signals_importance` tool systematically evaluates how specific groups of signals contribute to your model’s performance. It does this by comparing the model’s results with and without selected signals, without retraining the model. The model remains fixed; the tool simply tests the effect of removing signals from the input.

This analysis is useful for:

- **Model Interpretability**: Quantifies the impact of each signal or group.
- **Feature Selection**: Identifies redundant or low-impact signals that can be removed, simplifying the model and reducing data requirements.
- **Performance Benchmarking**: Shows the expected performance drop if a signal becomes unavailable.

---

## Command Line Parameters

- `--skip_list <comma-delimited list>`: Signals to exclude from the analysis (e.g., `Age,Gender`). Use for signals always present in the data and not under test.
- `--no_filtering_of_existence`: Disables the default filtering that ensures the signal under analysis exists in the time window. By default, the tool only compares samples where the signal is present; this flag tests the impact regardless of existence.
- `--features_groups <path>`: Path to a tab-delimited file (or "ButWhy" grouping file) mapping features to logical group names (e.g., all CBC-related features grouped as `CBC`). Can be also keyword like `BY_SIGNAL_CATEG` to group features by their originating source signal.
- `--group2signal <path>`: (Optional) Path to a tab-delimited file with two columns: group name (from `features_groups`) and a comma-separated list of signals. This remaps groups to the actual signals to exclude during testing.
- `--measure_regex <string>`: Controls the measurements we want to extract in the report. For example: "AUC|SENS@FPR_03"

You can also specify filtering arguments with `--bt_filter` arguments like we do in [FilterSamples](Guide%20for%20common%20actions/index.md#15-filter-samples-by-bt-cohort)

## How It Works

The tool uses a flexible two-step mapping to decide which signals to remove for each test:

1. **Feature-to-Group Mapping**: Reads the `--features_groups` file to map each feature to a group.
2. **Group-to-Signal Mapping**: Uses the `--group2signal` file to determine which signals to exclude for each group:
   - If a group name is found in `--group2signal`, the tool uses the listed signals.
   - If not, the group name itself is used as the signal for testing.

This lets you test individual groups or combine multiple groups into a single signal for analysis.

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