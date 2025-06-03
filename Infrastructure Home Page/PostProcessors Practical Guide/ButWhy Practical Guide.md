# ButWhy Practical Guide
# Global Feature Importance for a model
This can be done for each model (Tree based predictor - xgboost,lightGBM,QRF) directly without preparation. Can also calculate the importance in group of features like signals.
### Option 1 - redundant, but a little simpler
Using Flow print_model_info
```bash
Flow --print_model_info --f_model $MODEL_PATH --rep $REPOSITORY --f_samples $SAMPLES_TO_ANALYSE_SHAPLEY --max_samples $DOWN_SAMPLE_SAMPLES_TO_THIS_COUNT_OPTIONAL_TO_SPEEDUP --importance_param "importance_type=shap"
```
Which reports the feature importance using shapley on trees for each feature
### Option 2
Using Flow shap_val_request - which create a report and shows average outcome/score/Shapley values in different feature value groups.
```bash
Flow --shap_val_request --f_model $MODEL_PATH --rep $REPOSITORY --f_samples $SAMPLES_TO_ANALYSE_SHAPLEY --max_samples $DOWN_SAMPLE_SAMPLES_TO_THIS_COUNT_OPTIONAL_TO_SPEEDUP --group_signals "" --bin_method "split_method=iterative_merge;binCnt=50;min_bin_count=100;min_res_value=0.1" --f_output $REPORT_STORE_PATH
```
Which creates report and stores it in f_output paramter. There are two additional arguments:
- group_signals - keep empty to report for each feature.
  - BY_SIGNAL_CATEG_TREND - to report by signals, using **different** group for values and trends features
  - BY_SIGNAL_CATEG - to report by signals, using **the same **group for values and trends features
  - Can also specify "$FILE_PATH" where FILE_PATH is tab delimeted file with 2 tokens. The first is the name of the feature and the later is the name of the group to map into.

- bin_method - The report also contains information on how the model behaves in different feature values. This parameter controls how we "bin" the features. 
Use this argument: "split_method=iterative_merge;binCnt=50;min_bin_count=100;min_res_value=0.1". Which means to bin into 50 bins with at least 100 observations in bin and use resolution for feature value of 0.1.
Iteratively merges the adjacent bins that sums together with the smallest observation count (greedy). Has more methods and simpler methods, but this is good method to ensure minimal observations in bin.
- cohort_filter - might be a bootstrap cohort file to filter the samples - same format as bootstrap cohort file. It can also be just the cohort string. for example "Age:40,60;Time-Window:0,365". You should specify "f_json" if you want to use filters that are not Age,Gender,Time-window in order to define the features that will be used to filter the samples
- keep_imputers - If true will use the model imputers to complete missing values in the shapley values analysis. By default it is off - imputers are skipped in the analysis of feature values and kept in a separate bin of missing values.
Print graphs from report:
 
```bash
#Full path of scripts (should already be in system path) $MR_ROOT/Projects/Scripts/Python-scripts/feature_importance_printer.py
 
#command to output single html file with global feature\group importance (feature is the report was created without group_signals and group if Flow ran with some argument in group_signals). output of top 30 (max_count argument)
feature_importance_printer.py --report_path $REPORT_STORE_PATH  --output_path $OUTPUT_PATH --num_format "%2.3f" --feature_name "" --max_count 30 --print_multiple_graphs 0
 
#command to output multiple html file based on global feature\group importance. output_path is directory, create 30(max_count argument) graphs, 1 for each important feature based on global feature important. 
feature_importance_printer.py --report_path $REPORT_STORE_PATH  --output_path $OUTPUT_PATH --num_format "%2.3f" --feature_name "" --max_count 30 --print_multiple_graphs 1
# force_many_graph arguments - forces the graph to be scatter and not bar chart (bar chart is choosen, when less than 5 bins exists for the feature value)
# use_median - if true will use median instead if average values for each feature bin
# contrib_format - controls the Shapleyt values precision, num_format - controls the feature value precision. 
# feature_name - used to print single feature. When not empty will only output this feature and output_path is path to single html file
```
# Local Feature importnace  - Explain single prediction
Two steps are needed in order to use ButWhy for single prediction.
1. Add PostProcessor with explainer to the model. Can be done later with adjust_model
2. Apply the model - Use Flow or special program to reformat the output called CreateExplainReport
### Add Explainer into a model:
Example of how to train a model with explainer can be found here [PostProcessors Practical Guide](/Infrastructure%20Home%20Page/PostProcessors%20Practical%20Guide).
Here I'll show how to **add **explainer into existing model.
Create post_processor for the json:
```json
{ 
  "post_processors": [
    {
      "action_type":"post_processor",
      "pp_type":"tree_shap",
      "attr_name":"Tree_iterative_cov",
      "filters":"{max_count=0;sort_mode=0}",
	  "processing":"{grouping=BY_SIGNAL_CATEG_TREND;iterative=1;group_by_sum=0;learn_cov_matrix=1;zero_missing=0;use_mutual_information=0;mutual_inf_bin_setting={split_method=iterative_merge;min_bin_count=100;binCnt=50;min_res_value=0}}"
    }
  ]
}
```
Use adjust_model:
 
```bash
adjust_model --rep $REPOSITORY --inModel $F_MODEL_PATH --out $F_MODEL_OUTPUT_PATH_WITH_EXPLANIER --postProcessors $FILE_PATH_TO_POST_PROCESSOR_DEF --samples $SAMPLES_PATH 
```
### Create Report for each pred
```bash
 CreateExplainReport --rep $REPOSITORY --samples_path $PATH_TO_SAMPLES_TO_EXPLAIN --model_path $PATH_TO_MODEL  --output_path $OUTPUT_PATH_REPORT --take_max 10
# viewer_url_base - can control the link for the viewer. the string should contain 2 "%d" for pid, prediction time to open the viewer on each patient
# rep_settings - controls how many features to show in each group. Example rep_settings="min_count=2;sum_ratio=0.5" - means that it will show at least 2 features per group and the features together will have at least 50% weight
```
Print html for the report:
```bash
explainer_printer.py --report_path $OUTPUT_PATH_REPORT --predictor_name "pre2d - optional argument to control graph title" --filter_pid -1 --max_count 10 --output_path $FOLDER_OUTPUT_PATH_TO_HTMLS
#will create html for each sample - you can filter and to create htmls only for certain pid by using filter pid. max_count is parameter to controls the maximal amount of html graphs to create, will create only the first ones. 
```
 
 
 
 
