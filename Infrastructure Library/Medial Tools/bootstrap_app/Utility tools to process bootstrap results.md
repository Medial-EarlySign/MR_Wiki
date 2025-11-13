
# Utility Tools for Processing Bootstrap Results

The bootstrap output file can contain **a lot of numbers** and be scatter across different files. 
We need a tool to visualize, compare and rearrange the results in a desired format. 
Sometimes we want to visulize it as a graph.

## Formatting Bootstrap Results as Tables

You can use the `bootstrap_format.py` script to convert bootstrap result files into well-formatted tables (Excel-like). This script is available in the [MR_SCRIPTS](https://github.com/Medial-EarlySign/MR_Scripts) repository and should be accessible in your `PATH` under the `Python-scripts` directory of MR_Scripts.

**Basic usage:**
```bash
bootstrap_format.py --report_path $BT_REPORT_PATH_1 $BT_REPORT_PATH_2 ... $BT_REPORT_PATH_N \
  --report_name $NAME_FOR_1 $NAME_FOR_2 ... $NAME_FOR_N \
  --cohorts_list $REGEX_TO_FILTER_COHORTS \
  --measure_regex $REGEX_TO_FILTER_MEASUREMENTS \
  --table_format $TABLE_FORMAT
# Example of processing 2 files for previous mode and a current model:
bootstrap_format.py --report_path /tmp/bt_previous.pivot_txt /tmp/bt_current.pivot_txt \
  --report_name OLD NEW \
  --cohorts_list . \
  --measure_regex "AUC|OR@PR" \
  --table_format "cm,r"
```

**Key options:**

- Specify one or more bootstrap result files and assign each a name.
- Filter cohorts using the `--cohorts_list` regex (use `.` to include all).
- Select which measurements to extract with `--measure_regex` (e.g., `AUC|SENS@FPR`).
- Control table layout with `--table_format`. There are three dimensions:
    - `r`: report (the result file, e.g., baseline or MES_Full)
    - `c`: cohort (multiple cohorts per file)
    - `m`: measurement (e.g., AUC, SENS@FPR_05)
    Specify the three characters, separated by a comma, to map dimensions to rows and columns. One token will have two characters, expanding all combinations (Cartesian product) and using `$` as a delimiter. For example, `cm,r` means rows are cohort × measurement, columns are reports.

**Additional arguments:**

- `--break_cols`: Splits cohort filters into separate columns (default behavior).
- `--break_mes`: Splits measurement values (e.g., `8.4[7.8 - 9.2]`) into three columns: Mean, Min, Max.
- `--output_path`: Save the results as a CSV file.

**Example output (without `--break_cols`):**
```
Cohort$Measurements     OLD        NEW
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$AUC        0.807[0.801 - 0.814]    0.816[0.809 - 0.822]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$OR@PR_3    8.4[7.8 - 9.2]  9.5[8.7 - 10.3]
... (truncated)
```

**With `--break_cols` (default):**
```
Cohort  Age     Ex_or_Current   Suspected       Time-Window     Measurements    OLD        NEW
Time-Window:90.000-360.000,Age:50.000-80.000,...   50-80   1   0   90-360  AUC     0.807[0.801 - 0.814]    0.816[0.809 - 0.822]
... (truncated)
```

## Plotting Graphs from Bootstrap Results

To generate graphs (such as ROC curves) from bootstrap result files, use the `plt_bt.py` script:

```bash
plt_bt.py --input $BT_REPORT_PATH_1 $BT_REPORT_PATH_2 ... $BT_REPORT_PATH_N \
  --names $NAME_FOR_1 $NAME_FOR_2 ... $NAME_FOR_N \
  --output $OUTPUT_PATH \
  --measure $MEASURE \
  --filter_cohorts $REGEX_TO_FILTER_COHORTS \
  --show_ci 1 \
  --add_y_eq_x 1  # Adds y=x reference line
```
For ROC, use `SENS@FPR` as the measure.
