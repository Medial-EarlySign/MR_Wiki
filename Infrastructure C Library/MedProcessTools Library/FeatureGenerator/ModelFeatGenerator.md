# ModelFeatGenerator
The input model should have been trained on a set of samples different from the samples it is ran on at generation time, it is then used to generate predictions on the current samples at the given time points.
The input model can also be used to impute a feature  - this functionality is suppose to be moved to a separate feature processor.
fg_type -  "model". (required)
name - the name to be used in the feature name. Will default to the model file name and then to "ModelPred" if not given.
modelFile - model file, will be used as the feature name if name is not given.
impute_existing_feature - use the model to impute a feature in the matrix. Will not work if more than 1 time is given since it is  a separate functionality. defaults to 0.
n_preds - the number of prediction per sample per time - 1 for binary classification which is the default.
time_unit_sig - the signal time unit - defaults to the global_default_windows_time_unit.
time_unit_win - the times vector time unit - defaults to the global_default_windows_time_unit.
times - a vector of times before the sample for which the prediction should be given. Defaults to 0 if no values are given.
```json
{
	"feat_generator": "model",
	"name": "$NAME_OF_FEATURE",
	//Optional for manipulating prediction time:
	"time_unit_win": "Hours", "times": "30, 100, 200",
	//Option 1 - using trained model. path to binary MedModel
	"file": "/nas1/Work/Users/ReutF/model_feature/pre2d_light_S0.model"
 	//Option 2 - json for learning the model, path to samples if they are different from outer model training. There is a flag to filter and ensure we are using the same patient ids (no leakage from other splits)
	"model_json": "$PATH_TO_JSON",
	"model_train_samples": "$PATH_TO_TRAIN_SAMPLES_IF_DIFFERENT_FROM_CURRENT"
}
```
<img src="/attachments/9765619/9765623.png"/>
 
 
override_predictions cane be used to copy predictions into our feature matrix without running the model (if we have the predictions from a previous run). There is no way to do this using the json file
The feature id nember in the feature matrix is constant for all features resulting from running this generator once (FTR_000001.regression_pred_t_100.1, FTR_000001.regression_pred_t_200.1,  FTR_000001.regression_pred_t_30.1)
 
