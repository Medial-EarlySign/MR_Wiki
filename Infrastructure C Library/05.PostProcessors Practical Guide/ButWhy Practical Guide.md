
# ButWhy Practical Guide

## Global Feature Importance

You can compute global feature importance for each model (tree-based predictors like XGBoost, LightGBM, QRF) directly, without extra preparation. Importance can also be calculated for groups of features (e.g., signals).

### Option 1 - Simple (but redundant)
Use Flow's `print_model_info` to get feature importance using SHAP values:

```bash
Flow --print_model_info --f_model $MODEL_PATH --rep $REPOSITORY --f_samples $SAMPLES_TO_ANALYSE_SHAPLEY --max_samples $DOWN_SAMPLE_SAMPLES_TO_THIS_COUNT_OPTIONAL_TO_SPEEDUP --importance_param "importance_type=shap"
```
This command reports SHAP-based feature importance for each feature in tree models.

### Option 2 - Detailed Report
Use Flow's `shap_val_request` to generate a report with average outcome/score/SHAP values across different feature value groups:

```bash
Flow --shap_val_request --f_model $MODEL_PATH --rep $REPOSITORY --f_samples $SAMPLES_TO_ANALYSE_SHAPLEY --max_samples $DOWN_SAMPLE_SAMPLES_TO_THIS_COUNT_OPTIONAL_TO_SPEEDUP --group_signals "" --bin_method "split_method=iterative_merge;binCnt=50;min_bin_count=100;min_res_value=0.1" --f_output $REPORT_STORE_PATH
```
This creates a report at the path specified by `--f_output`. Key arguments:

- **group_signals**: Leave empty to report for each feature. Use:
  - `BY_SIGNAL_CATEG_TREND`: group by signals, separating value and trend features
  - `BY_SIGNAL_CATEG`: group by signals, combining value and trend features
  - Or provide a tab-delimited file mapping features to groups
- **bin_method**: Controls how features are binned. The recommended value is `split_method=iterative_merge;binCnt=50;min_bin_count=100;min_res_value=0.1`, which creates up to 50 bins with at least 100 samples per bin and a minimum value resolution of 0.1. Bins are merged greedily to ensure minimum counts in each bin.
- **cohort_filter**: Optionally filter samples using a bootstrap cohort file or a cohort string (e.g., `Age:40,60;Time-Window:0,365`). For filters beyond Age, Gender, or Time-window, specify `f_json` to define filter features.
- **keep_imputers**: If true, model imputers are used to fill missing values during SHAP analysis. By default, imputers are skipped and missing values are binned separately.
- **max_samples**: controls maximal samples count and randomly subsample the row to the number if the file is larger. If 0, will do nothing (default: 0) 
- **f_model**, **rep**, **f_samples**: needed inputs for calculation. We need data repository, full model with predictor and samples files to calcualte the feature importance for


**Advanced flags (usually not needed):**
- `normalize`: Normalize SHAP values to percentages (default: 1)
- `normalize_after`: If 1, normalizes after summing global importance; if 0, normalizes per prediction (default: 1; only applies if `normalize` is on)
- `remove_b0`: Remove the baseline/prior score (default: 1). If 0, keeps and prints the baseline (b0), which is the constant added to all predictions.

#### Inspecting the Raw Output

To inspect the first few rows of the output file (`shap_val_output.tsv`) and transpose them for easier reading:

```bash
cat shap_val_output.tsv | head -n 4 | awk ' { for (i=1;i<=NF;i++) a[i]=a[i]"\t"$i; } END { for (i in a) {printf("%d%s\n", i, a[i])} }' | sort -g -k1
```

This produces a table like:

|   | **Feature** | **Age** | **ADMISSION.category_dep_set_Hospital_Emergency_Department.win_0_3650** | **DIAGNOSIS.category_dep_set_ICD10_CODE:J00-J99.win_0_1825** |
|---|:-----------|:--------|:------------------------------------------------------|:---------------------------------------------------|
| 1 | Importance | 5.3 | 4.9 | 4.15 |
| 2 | SHAP::Low_Mean | 15.4 | -4.3 | -5.1 |
| 3 | SHAP::Low_Std | 8.6 | 1.0 | 1.4 |
| 4 | SHAP::Low_Prctile10 | 4.5 | -5.6 | -6.8 |
| 5 | SHAP::Low_Prctile50 | 15.0 | -4.3 | -5.2 |
| 6 | SHAP::Low_Prctile90 | 27.2 | -3.1 | -3.3 |
| 7 | FEAT_VAL::Low_Mean | 5.27 | 0 | 0 |
| 9 | FEAT_VAL::Low_Prctile0 | 0 | 0 | 0 |
| 10 | FEAT_VAL::Low_Prctile10 | 2 | 0 | 0 |
| 11 | FEAT_VAL::Low_Prctile50 | 6 | 0 | 0 |
| 12 | FEAT_VAL::Low_Prctile90 | 9 | 0 | 0 |
| 13 | FEAT_VAL::Low_Prctile100 | 9 | 0 | 0 |                               |
| 14 | SHAP::Medium_Mean | -4.9 | -1.2 | -1.0 |
| ... | ... | ... | ... | ... |
| 19 | FEAT_VAL::Medium_Mean | 44.96 | 0.3 | 0.5 |
| 21 | FEAT_VAL::Medium_Prctile0 | 40 | 0 | 0 |
| 25 | FEAT_VAL::Medium_Prctile100 | 50 | 1 | 1 |
| 26 | SHAP::High_Mean | 10.3 | 6.1 | 3.2 |
| ... | ... | ... | ... | ... |
| 31 | FEAT_VAL::High_Mean | 84.57 | 1 | 1 |
| 33 | FEAT_VAL::High_Prctile0 | 81 | 1 | 1 |
| 37 | FEAT_VAL::High_Prctile100 | 90 | 1 | 1 |
| ... | ... | ... | ... | ... |

**Example (Age column):**
- *Importance*: About 5.3% of the average XGBoost raw score (before sigmoid/calibration)
- *SHAP::Low_Mean*: 15.4 - average contribution for the "Low" age group (positive)
- *FEAT_VAL::Low_Prctile0*: 0 - lowest value in "Low" bin; *FEAT_VAL::Low_Prctile100*: 9 - highest value (so "Low" = 0-9 years, average 5.27)
- *SHAP::Medium_Mean*: -4.9% - negative contribution for 40–50 year olds, average 44.96 (Protective)
- *SHAP::High_Mean*: 10.3% - positive contribution for 81–90 year olds, average 84.57

## Generating Graphs from the Report

Use the script `feature_importance_printer.py` (should be under [MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts) `Python-scripts/feature_importance_printer.py`).

- To output a single HTML file with the top 30 features/groups:
  ```bash
  feature_importance_printer.py --report_path $REPORT_STORE_PATH --output_path $OUTPUT_PATH --num_format "%2.3f" --feature_name "" --max_count 30 --print_multiple_graphs 0
  ```
- To output multiple HTML files (one per feature/group, up to 30):
  ```bash
  feature_importance_printer.py --report_path $REPORT_STORE_PATH --output_path $OUTPUT_PATH --num_format "%2.3f" --feature_name "" --max_count 30 --print_multiple_graphs 1
  ```
    - `force_many_graph`: Forces scatter (not bar) chart if set
    - `use_median`: Use median instead of mean for feature bins
    - `contrib_format`: Controls SHAP value precision; `num_format`: feature value precision
    - `feature_name`: If set, outputs only that feature to a single HTML file

## Local Feature Importance – Explaining a Single Prediction

To use ButWhy for explaining individual predictions, follow these steps:

1. **Add an Explainer PostProcessor to the Model** (can be done later with `adjust_model`)
2. **Apply the Model** - Use Flow or `CreateExplainReport` to generate report

### Adding an Explainer to an Existing Model

For training with an explainer, see the [PostProcessors Practical Guide](../05.PostProcessors%20Practical%20Guide). To add an explainer to an existing model, create a post_processor JSON like:

```json
{
  "post_processors": [
    {
      "action_type": "post_processor",
      "pp_type": "tree_shap",
      "attr_name": "Tree_iterative_cov",
      "filters": "{max_count=0;sort_mode=0}",
      "processing": "{grouping=BY_SIGNAL_CATEG_TREND;iterative=1;group_by_sum=0;learn_cov_matrix=1;zero_missing=0;use_mutual_information=0;mutual_inf_bin_setting={split_method=iterative_merge;min_bin_count=100;binCnt=50;min_res_value=0}}"
    }
  ]
}
```

Add this post processor using `adjust_model`:

```bash
adjust_model --rep $REPOSITORY --inModel $F_MODEL_PATH --out $F_MODEL_OUTPUT_PATH_WITH_EXPLANIER --postProcessors $FILE_PATH_TO_POST_PROCESSOR_DEF --samples $SAMPLES_PATH
```

### Creating a Report for Each Prediction

`CreateExplainReport` is part of [AllTools](../../Installation/index.md#3-mes-tools-to-train-and-test-models):

```bash
CreateExplainReport --rep $REPOSITORY --samples_path $PATH_TO_SAMPLES_TO_EXPLAIN --model_path $PATH_TO_MODEL --output_path $OUTPUT_PATH_REPORT --take_max 10
# viewer_url_base: Controls the viewer link (should contain two "%d" for pid and prediction time)
# rep_settings: Controls features shown per group, e.g., rep_settings="min_count=2;sum_ratio=0.5" shows at least 2 features/group and at least 50% total weight
```

### Generating HTML Reports

Use `explainer_printer.py` (in MR_Scripts under `Python-scripts/explainer_printer.py`):

```bash
explainer_printer.py --report_path $OUTPUT_PATH_REPORT --predictor_name "pre2d - optional argument to control graph title" --filter_pid -1 --max_count 10 --output_path $FOLDER_OUTPUT_PATH_TO_HTMLS
# This creates an HTML file for each sample. Use --filter_pid to select specific pids. max_count limits the number of HTMLs generated.
```
 
 
 
 
