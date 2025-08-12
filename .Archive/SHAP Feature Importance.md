# SHAP Feature Importance
SHAP Feature Importance tool caluclates the SHAP values for XGboost or LightGBM models, and generate a pdf document with feature importance information.
the tool can be found in  **$MR_ROOT/Tools/ShapFeatureImportance/.**
The tool receives a model file and a samples file (an additional model for filtering the samples is optional). 
**Important:**

- Should run in **python 3** (use the command: source /opt/medial/python36/enable)
- it is not recommended to work on more than 20,000 samples. Usually 10,000 can give a clear enough graphs (use num_samples parameter)
 
The final document consists 4 plots:

1. **Importance of single features:**<img src="/attachments/11207150/11207121.png"/>****
2. **Mean of absolute SHAP values for most important ******<img src="/attachments/11207150/11207122.png"/>
3. ****<img src="/attachments/11207150/11207123.png"/>
4. **Importance of signals - grouped by type******In this figure, signals are aggregated together (SHAP values are summed) with their feature type - for numerical features, feaures are aggregated according to the following feature groups:'value' ('last','avg',',min','max'), 'trend' ('slope', 'win_delta','last_delta','max_diff'), 'time' : 'last_time', 'std': 'std'} .  ********
 
 
 
**Parameters:**

- samples_file::  Input samples file
- rep_file:: Repository file
- model_file_json_filter::  Model to use for generating filters. (optional)
- model_file:: Model:: main model
- output_file:: Ouput file name
- filter_params:: Parameters for filtering (optional - "bootstrap fomatting". Example: "Time-Window:30,180;Age:65,75;Gender:2,2")
- sig_rename_dict:: Renaming dictionary - renaming the signal name for the last graph (optional. Example: "LDL_over_HDL:LDL over HDL,category_set_ATC_C10A____:Drug-LIPID MODIFYING AGENTS")
- num_samples :: default= inf  :: Bound the number of samples - for faster running
**Workflow:**

1. If **filter_params** exists, a model is applied (if available, according to the "**model_file_json_filter**", otherwise only a model with age and gender is applied).
2. The samples are than filtered according to the **filter_params**
3. After filtering, a unique random sample is chosen per id.
4. The main model (**model_file**) is applied for features matrix generation
5. SHAP values are calculated
6. features are aggregated to groups.

**Example:**
```bash title="Running Example"
python shap_feature_importance_tool.py --num_samples 10000 --sig_rename_dict "LDL_over_HDL:LDL over HDL,category_set_ATC_C10A____:Drug-LIPIDMODIFYING AGENTS" --samples_file /server/Work/AlgoMarkers/AAA/aaa_1.0.0.2/RegistryAndSamples/aaa_train_age_matched_matched.samples --rep_file /home/Repositories/THIN/thin_2018/thin.repository --model_file_json_filter /server/UsersData/ron-internal/MR/Projects/Shared/AlgoMarkers/aaa/configs/analysis/ever_smokers_json.json --model_file /server/Work/AlgoMarkers/AAA/aaa_1.0.0.2/Performance/model_6_S4.model --output_file /server/Work/Users/Ron/tmp/shap_5.pdf --filter_params "Time-Window:30,180;Age:65,75;Gender:2,2;Ex_or_Current_Smoker:0.5,1.5"
```


