# TestGibbs
There is utility to test the gibbs imputations method - it has several options for controlling gibbs parameters for training, testing it.
The default test is to impute all values (harder) - generate a full example and compare it to the original population. You can also contol to test only "earsing" randomly masks of values and imputing them (easier for gibbs).
Please git pull [http://bitbucket:7990/scm/med/but_why.git](http://bitbucket:7990/scm/med/but_why.git) and compile TestGibbs, then run with TestGibbs --base_config $CONFIG_FILE  or just specify all parameters in the command.
 
Gibbs config examples with all params:
```ini
save_gibbs=/nas1/Temp/Test_gibbs/gibbs_model #Binary model of gibbs object. Will start from if exists
save_gibbs_cmp_log=/nas1/Temp/Test_gibbs/compare_gibbs_log
save_graphs_dir=/nas1/Temp/Test_gibbs/gibbs_graphs
missing_value=-65336
test_random_masks=0
down_sample=0
#When learn_to_impute_missing_value is 1, the imputer will also take missing value imputation as legal value to impute. Useful for simple compare to test matrix that has missing values VS generated data using gibbs
learn_to_impute_missing_value=1
#optional file path with name of features to filter from matrix and keep only those
#Flow --print_model_info --f_model /nas1/Work/Users/Eitan/Lung/outputs/models/model_10.base/results/CV_MODEL_0.medmdl 2>&1 | grep FEAT | awk -F" " '{print $3}' | sort > /nas1/Temp/Test_gibbs/feats_list
#Removed Smoking_Status features - they are strongly connected and it causes problems in gibbs
sel_features=/nas1/Temp/Test_gibbs/feats_list 
#Input option 1 - directly provide train/test matrices
#load_matrix_path= #Provide specific matrix for train
#test_gibbs_mat= #Provide specific matrix for test
#Input option 2 - Provide rep and samples and model to generate matrix
run_feat_processors=0
rep=/home/Repositories/KP/kp.repository
model_path=/nas1/Work/Users/Eitan/Lung/outputs/models/model_10.base/results/CV_MODEL_0.medmdl
train_samples=/nas1/Work/Users/Eitan/Lung/outputs/models/model_10.base/results/CV_MODEL_0.medmdl.train_samples
test_samples=/nas1/Work/Users/Eitan/Lung/outputs/models/model_10.base/results/CV_MODEL_0.medmdl.test_samples
max_loops=1 #Rerrun multiple times to take only "good" samples each time. If bigger than 1
gibbs_random_range=1 #Only used if test_random_masks is on - erase mask and put those values in random range
stop_at_sens=0.95 #Rerrun multiple times to take only "good" samples each time. threshold for good samples
gibbs_params=predictor_type=lightgbm;predictor_args={objective=multiclass;metric=multi_logloss;verbose=0;num_threads=0;num_trees=100;learning_rate=0.05;lambda_l2=0;metric_freq=50;is_training_metric=false;max_bin=255;min_data_in_leaf=20;feature_fraction=0.8;bagging_fraction=1;bagging_freq=4;is_unbalance=true;num_leaves=80};calibration_save_ratio=0.2;calibration_string={calibration_type=isotonic_regression;verbose=0};num_class_setup=num_class;bin_settings={split_method=iterative_merge;min_bin_count=500;binCnt=100};selection_count=500000
gibbs_sampling_params=burn_in_count=1000;jump_between_samples=50;samples_count=10000;find_real_value_bin=1
#For testing the generated samples and compare to test samples
predictor_type=xgb
predictor_args=tree_method=auto;booster=gbtree;objective=binary:logistic;eta=0.1;alpha=0;lambda=0.1;gamma=0.1;max_depth=4;colsample_bytree=1;colsample_bylevel=0.8;min_child_weight=10;num_round=100;subsample=0.7
```
```bash
Linux/Release/TestGibbs --base_conf /server/UsersData/alon/MR/Projects/Shared/Projects/configs/UnitTesting/examples/MultipleImputations/TestGibbs_cfg.cfg
```
 
The result will appear in  /nas1/Temp/Test_gibbs
