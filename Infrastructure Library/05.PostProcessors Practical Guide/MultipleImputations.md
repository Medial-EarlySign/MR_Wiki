# MultipleImputations
The main idea is to do multiple imputations for missing value as post processor on existing model. 
The steps are:

- Apply model till feature processor imputers (if model has one). If model doesn't have imputer complete apply till the end before predictor. The main idea is that we can't just use the model imputer (it's not stochastic and we need to replace it) so the postprocessor locate the imputer if exists and "replaces" with stochastic one. 
- Duplicate each row 100 times (parameter) for different imputation in each line. There is also additional parameter "batch" to control the maximal memory needed for Apply the post processor - mainly set to 10K, so we will end up with 1M rows in each batch that each 100 rows are duplicates of the same row and will be aggregated later. 
- Apply the stochastic imputer given in the post processor argument on all rows - so each row out of the 100 duplication will get different imputations
- Aggregations, each 100 rows are aggregated - Mean,Median, STD, CI_lower, CI_Upper are extract as attributes in model apply. We can later test if the model original score (that is not impacted) is even inside the confidence interval. You can also control the post processor to override the prediction with mean value/median value of this multiple imputations
 
Example config:
```json
{ 
  "post_processors": [
    {
      "action_type":"post_processor",
      "pp_type":"aggregate_preds",
      "force_cancel_imputations":"1",
	  "use_median":"0",
	  "resample_cnt":"100",
	  "batch_size":"10000",
	  "feature_processor_type":"predictor_imputer",
	  //"feature_processor_args":"{gen_type=UNIVARIATE_DIST;generator_args={strata=Age,0,100,5;min_samples=50};tag=labs_numeric}"
	  "feature_processor_args":"{gen_type=GIBBS;generator_args={kmeans=0;select_with_repeats=0;max_iters=0;predictor_type=lightgbm;predictor_args={objective=multiclass;metric=multi_logloss;verbose=0;num_threads=0;num_trees=100;learning_rate=0.05;lambda_l2=0;metric_freq=50;is_training_metric=false;max_bin=255;min_data_in_leaf=50;feature_fraction=0.8;bagging_fraction=0.25;bagging_freq=4;is_unbalance=true;num_leaves=80;silent=2};num_class_setup=num_class;calibration_string={calibration_type=isotonic_regression;verbose=0};calibration_save_ratio=0.2;bin_settings={split_method=iterative_merge;min_bin_count=200;binCnt=100};selection_ratio=1.0;selection_count=500000};sampling_args={burn_in_count=5;jump_between_samples=10;samples_count=1;find_real_value_bin=1};verbose_learn=1;tag=labs_numeric}"
    }
  ]
}
```

- resample_cnt - how many times we duplicate each row
- force_cancel_imputations - flag to indicate we need to find model original imputer and replace it (otherwise there will be no missing values, the imputer will impute them).
- batch_size - how many samples in each batch before duplications
- use_median - if true will replace pred_0 with median
- feature_processor_type - the feature processor init type - pay attention to use something with stochastic properties, for example "predictor_imputer" - you can see more imputer options in [FeatureProcessor practical guide](../03.FeatureProcessor%20practical%20guide)
- feature_processor_args - arguments for the feature processors. You can see some explanations in the FeatureProcessor practical guide
Run adjust model with this post processor to generate gibbs sampling on missing values in features tagged "labs_numeric":
```bash
adjust_model --rep /home/Repositories/THIN/thin_jun2017/thin.repository --samples /server/Work/Users/Alon/But_Why/outputs/explainers_samples/diabetes/train.samples --inModel /server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/diabetes/base_model.bin --out /server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/diabetes/test_imputer.2.mdl --postProcessors $MR_ROOT/Projects/Shared/Projects/configs/UnitTesting/examples/MultipleImputations/post_processors.multipleimputations.json
```
Apply with Flow and store attributes:
```bash
Flow --get_model_preds --print_attr 1 --rep /home/Repositories/THIN/thin_jun2017/thin.repository --f_samples /server/Work/Users/Alon/But_Why/outputs/explainers_samples/diabetes/test.samples --f_preds /server/Linux/alon/pre2d_test.tsv --f_model /server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/diabetes/test_imputer.2.mdl
```
 

Example output for pred2d model output:
[Excel Results](../../attachments/13402388/13402394.xlsx)
There are additional columns: attr_pred.ci_lower,attr_pred.ci_upper,attr_pred.mean,attr_pred.median,attr_pred.std
 
