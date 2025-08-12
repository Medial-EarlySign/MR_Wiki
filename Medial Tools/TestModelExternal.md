# TestModelExternal
 A tool to test difference between repositories when applying a model.
It builds a propensity model to discriminate between repositories to reveal differences and do simplr compare of the feature matrices.
The goal is to discover that the model is transferable and can well behave on the second repository.
 
Uses example:

- Estimate model performance/transferability on different repository
- Test model on different years and the differences in different year. You can pass train_rep==test_rep and just change the samples to test for differences

Part of Tools git repository. Can be found under AllTools solution.

## **Mode 1 - Comparing the model when the 2 repositories are available in the same network:**

- model_path - Must be given in any mode. The path to the binary MedModel that we want to test for.
- rep_test - repository for testing and comparing with. In the propensity model it will be labeled as 1.
- samples_test - path to MedSamples to be applied in the test repository
- output - direcotry to output files
- rep_trained - repository path of the trained model (or just the reference repository to test with)
- samples_train - path to similar way (same logic of creation as test_samples) created MedSample on the training repository
- predictor_type, predictor_args - parameters for the propensity model to discriminate difference of repositories by the model view
- calibration_init_str - calibration args. Will be used in the propensity model as Post Processor
 
Less important (optional)

- smaller_model_feat_size  - if given > 0, will create additional smaller propensity model based on top X group of features. X=smaller_model_feat_size. 
- additional_importance_to_rank - path fo shaply report created by "Flow --shap_val_request" to rank the difference combained with the importance of each feature to the model
- features_subset_file - file to filter features from the MedModel
- fix_train_res - if >0, will also set the feature resulotion in the train to match the test.
- sub_sample_train - sub sampling on train samples. Integer number to limit the maximal number of samples to sub sample to. 0 -no subsampling.
- sub_sample_test - sub sampling on test samples. Integer number to limit the maximal number of samples to sub sample to.0 -no subsampling.
- train_ratio - the train/test ratio - the test are used to report propensity model performance
- bt_params - bootstrap parameters for the propensity model
- binning_shap_params - for the shapley report analysis on the propensity model
- group_shap_params - grouping args for the shapley on the propensity model
- shap_auc_threshold - if the AUC is smaller than that, will skip shapley analysis to save time
- print_mat - if > 0 will print propensity matrix. 0 - labels are for train samples, 1 - labels are for test samples,

## **Mode 2 - Compare when the repositories are in different networks**
To use this mode, rep_trained and/or samples_train should be empty.

- model_path - Must be given in any mode. The path to the binary MedModel that we want to test for.
- rep_test - repository for testing and comparing with. In the propensity model it will be labeled as 1.
- samples_test - path to MedSamples to be applied in the test repository
- output - direcotry to output files
- strata_json_model - json to be used for creating strats and collecting stats
- strata_settings - the strata setting for collecting stats
When comparing to different repository.
Add this argument:
- strata_train_features_moments - will create the file for the current test_samples and compare it to the file path in this path
Less important (optional):
- features_subset_file - file to filter features from the MedModel
- sub_sample_test - sub sampling on test samples. Integer number to limit the maximal number of samples to sub sample to.0 -no subsampling.
