# MedModel json format
To see the code, please refer to MedModel::init_from_json_file
The json have several general fields, you should used only the first "model_json_version":
 
- "model_json_version" - you should specify 2
- "serialize_learning_set" - boolen 0/1 - if turned on will store learning samples in the model. (default is 0)
- "generate_masks_for_features" - boolean 0/1 - if turned on, will store for each feature if the value was imputed or not (important for the explainers, and [MASK predictor](MedPredictor%20practical%20guide/MASK%20predictor%20-%20predict%20by_missing_value_subset) when using calibration, doesn't important for other things). Can be also changed later with [adjust_model ](/Medial%20Tools/adjust_model)or [change_model](/Medial%20Tools/change_model). Default if not specified is "0"
- "max_data_in_mem" - the maximal size of a vector that the machine can hold (default is MAX_INT to avoid integer overflow, since we aren't sure all the code is safe). This is the limit for number of rows * number if features. A bigger number of elements will split the model apply into batches to fir memory. Can be also changed later with [adjust_model ](/Medial%20Tools/adjust_model)or [change_model](/Medial%20Tools/change_model).
- "take_mean_pred" - boolean 0/1 - if turned on will average predictions, when false will use median. Useful when using multiple imputations (not used anywhere till now, so it doesn't effect anything important). Default is 1.  Can be also changed later with [adjust_model ](/Medial%20Tools/adjust_model)or [change_model](/Medial%20Tools/change_model)
You can use:
- path_rel: prefix - to reference file with relative path to the json - will translate file name to absolute file path from current json path
- file_rel: prefix to reference file with relative path to the json and extracts file content line by line into list of actions. Translate into [ "line1", "line2", ...] from the file. Useful to create multiple items where each line constructs a new item
- comma_rel: prefix to reference file with relative path to the json and extracts file content line by line into string list. Translate into "line1,line2, ..."  from the file. Useful to create a single set
- json: - reference to another file relative path to this json - add file content to this json as is...
 
The main model pipeline instructions are listed under "model_actions" which is an array of model components. An example template:
```
{
  "model_json_version":"2",
  "model_actions" : [
     ... LIST HERE MODEL COMPONENTS, EACH ONE IN {} ...
  ]
}
```
In the next section we will describe the elements. 
Another trick we have in the model_actions is that when you specify a list of values for some element, the element is duplicated for all the values in the list.
For example
 
```
{
 "model_component_field_value_1": "Value_A",
 "model_component_field_value_2": [ "val_1", "val_2", "val_3" ... ]
}
```
This block is equivelent for writing:
```
{
 "model_component_field_value_1": "Value_A",
 "model_component_field_value_2": "val_1"
},
{
 "model_component_field_value_1": "Value_A",
 "model_component_field_value_2": "val_2"
},
{
 "model_component_field_value_1": "Value_A",
 "model_component_field_value_2": "val_3"
}
... And all the rest values
```
When we have multiple lists in the same block - all the options are created like cartesian product. 
## Model components:
This section will describe model components that can be placed inside "model_actions" list. The order iof the components is important and the actions are performed by the order they are written.
You can specify blocks of components that can be excuted in parallel (used many times), but each block is excuted one of the other.
All feature_genertors are excuted in parallel so you don't need to arrange them in blocks.
- Each component has a field called "action_type". If not provided, it is assumed to be "feat_generator" - feature generator. Please place it as the first field in the block for readability. Available options:
  - rp_set - set of rep_processors that can be excuted in parallel. Many times we used this template even for 1 component for easier editing. The block contains another element called "members" which is an array of "rep_processors" that can be execute in parallel. Please specify "rp_type" to choose type and then use initialize the type using the rest of the parameters in the json elemtn block
  - fp_set - set of feature_processors that can be excuted in parallel. Many times we used this template even for 1 component for easier editing. The block contains another element called "members" which is an array of "feature_processors" that can be excute in parallel.
  - rep_processor - to specify a single rep_processor. Please choose on from [Rep Processors Practical Guide](../Rep%20Processors%20Practical%20Guide). Or you can refer the full list of options in the doxygen: [ RepProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/RepProcess_8h.html#a2772b5cb2b32efafbbd8ba9440b9576a)
  - feat_generator - to specify feature generator. Please choose on from [Feature Generator Practical Guide](../Feature%20Generator%20Practical%20Guide). Or you can refer the full list of options in the doxygen: [FeatureGeneratorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureGenerator_8h.html#a109794c7f375415720a0af5dd3132023)
  - feat_processor - to specify feature processor. Please choose on from . Or you can refer the full list of options in the doxygen: [FeatureProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureProcess_8h.html#ae648a97312d7df5b3f5cf01b19887334). If you want to apply the processor on multiple features, please add: "tag" and give it value to search for features with the relevant tag. Please also include "duplicate":"1" in the phrase. What happens, is that MultiFeatureProcessor is created and given duplicate=1, and tag. The multi feature processors scans all features and generates child feature processoer after filtering the features by tag.
  - post_processor to specify feature processor. Please choose on from [PostProcessors Practical Guide](../PostProcessors%20Practical%20Guide). Or you can refer the full list of options in the doxygen: [PostProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/PostProcessor_8h.html#a1dab070b8206be89206ff19f321a1cfc)
Example of "rp_set" block, "fp_set" is similar
```
{
  "action_type":"rp_set",
  "members": [
    ... LIST HERE REP PROCESSOR COMPONENTS, EACH ONE IN {} AND EACH CONTAIN "rp_type" FIELD...
  ]
}
```
 
## predictor
in the last part of the json, after "model_actions".
- "predictor" to select MedPredictor to train on the generated matrix - [MedPredictor practical guide](../MedPredictor%20practical%20guide) - doxygen full [List of options](https://Medial-EarlySign.github.io/MR_LIBS/MedAlgoh.html#ab3f9aacffd8e29e833677299133ac4f0). For example "xgb" for xgboost or "lightgbm" for LightGBM, "lm" for linear model, etc.
- "predictor_params" - arguments to initialize the predictor. Depends on the chossen predictor.
- You can put in the end lists of values that you can reference to in the model_actions. For example, "diabetes_drugs": "ATC_A______,ATC_...." and in the model_actions you can refer to this list by using "ref:diabetes_drugs"
