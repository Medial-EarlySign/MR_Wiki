# MedModel JSON Format

This guide explains the structure and usage of the MedModel JSON format for defining machine learning pipelines within the Medial infrastructure. The JSON file orchestrates all model steps, from raw data processing to prediction and post-processing, making your workflow modular, reproducible, and easy to configure.

## What is a MedModel JSON?

A MedModel JSON file describes:

- The pipeline of data processing and machine learning components (like data cleaning, feature generation, modeling, etc.)
- The order and configuration of each processing step
- The parameters for each component (as key-value pairs). This will call the component ["init" function](MedProcessTools%20Library/SerializableObject.md#init-from-string) with the key value pairs to initialize the component. This allows a simpler way to add components and pass arguments to them from the json.
- How to reference additional configuration files or value lists

This enables flexible, versioned, and shareable model definitions-ideal for both research and production.

## How to Write a MedModel JSON: Step-by-Step

Let’s walk through building a JSON model file, explaining each section.

### 1. General Fields

These fields configure the overall behavior of the pipeline. Most are optional and have sensible defaults.

```json
{
  "$schema": "https://raw.githubusercontent.com/Medial-EarlySign/MR_Tools/refs/heads/main/medmodel_schema.json",
  "model_json_version": "2",                // Required: version of the format (always use "2")
  "serialize_learning_set": "0",            // Optional: whether to save training samples in the model (default "0")
  "generate_masks_for_features": "0",       // Optional: track which features were imputed (default "0")
  "max_data_in_mem": 100000,                // Optional: controls batch size for large data (default is unlimited)
  "take_mean_pred": "1"                     // Optional: use mean for prediction (default "1")
}
```

**Tip:** Only `model_json_version` is required for most users. The rest can typically be left out.
**Tip2:** Use The $schema for autocomplete and validation, even though it is incomplete.

### 2. The Pipeline: `model_actions`

This is the heart of the model definition-a list of components executed in order. Each component is an object specifying:

- `action_type`: What kind of step this is (data cleaning, feature generation, etc.)
- Other keys: Parameters specific to the step

**Component types:**

- `rep_processor` or `rp_set`: Process raw signals
    * List of available rep_processor: [Rep Processors Practical Guide](01.Rep%20Processors%20Practical%20Guide). You should select and sepecify a the type name in `rp_type` field. For example:
    ```json
    {
      "rp_type": "$SELECT_TYPE",
      ... Specific Component arguments that will be passed as dictionary key and value to "init" function of the component
    }
    ```
- `feat_generator`: Creates features from cleaned signals
    * List of available feat_generator: [Feature Generator Practical Guide](02.Feature%20Generator%20Practical%20Guide). You should select and sepecify a the type name in `fg_type` field. For example:
    ```json
    {
      "fg_type": "$SELECT_TYPE",
      ... Specific Component arguments that will be passed as dictionary key and value to "init" function of the component
    }
    ```
- `fp_set`: Post-processes the feature matrix (imputation, selection, normalization)
    * List of available feature processors: [FeatureProcessor practical guide](03.FeatureProcessor%20practical%20guide). You should select and sepecify a the type name in `fp_type` field. For example:
    ```json
    {
      "fp_type": "$SELECT_TYPE",
      ... Specific Component arguments that will be passed as dictionary key and value to "init" function of the component
    }
    ```
- `predictor`: The machine learning algorithm. List of available predictors: [MedPredictor practical guide](04.MedAlgo%20Library/MedPredictor%20practical%20guide). you should specify the selected predictor as `predictor` and it parameters as `predictor_params`
- `post_processor`: Final calibration or adjustment.
    * List of available post processors: [PostProcessors Practical Guide](05.PostProcessors%20Practical%20Guide) and specify the type in `post_processor`. Example:
    ```json
    {
      "fp_post_processortype": "$SELECT_TYPE",
      ... Specific Component arguments that will be passed as dictionary key and value to "init" function of the component
    }
    ```

#### Example Walkthrough

Let’s walk through an example and explain each major step:

```json
{
  "$schema": "https://raw.githubusercontent.com/Medial-EarlySign/MR_Tools/refs/heads/main/medmodel_schema.json",
  "model_json_version": "2",
  "serialize_learning_set": "0",
  "model_actions": [
    // Step 1: Load additional rep_processors from another file for modularity
    "json:full_rep_processors.json",

    // Step 2: Generate simple features for age, gender, and smoking status
    { "action_type": "feat_generator", "fg_type": "age" },
    { "action_type": "feat_generator", "fg_type": "gender" },
    { "action_type": "feat_generator", "fg_type": "unified_smoking", "tags": "smoking", "smoking_features": "Current_Smoker,Ex_Smoker,..." },

    // Step 3: Generate categorical features (e.g., cancer diagnosis in the last 30 years)
    {
      "action_type": "feat_generator",
      "fg_type": "basic",
      "type": "category_set",
      "window": ["win_from=0;win_to=10950"], // Days
      "sets": ["ICD9_CODE:140-149,ICD9_CODE:150-159,..."],
      "signal": "ICD9_Diagnosis",
      "in_set_name": "Cancers"
    },

    // Step 4: Generate statistical features (last, avg, min, max, etc.) for signals and time windows
    {
      "action_type": "feat_generator",
      "fg_type": "basic",
      "type": ["last", "avg", "max", "min"],
      "window": [
        "win_from=0;win_to=180",
        "win_from=0;win_to=365"
      ],
      "signal": ["Hemoglobin", "WBC", "Platelets"]
    },

    // Step 5: Feature selection (remove features with near-constant values)
    {
      "action_type": "fp_set",
      "members": [
        { "fp_type": "remove_deg", "percentage": "0.999" }
      ]
    },

    // Step 6: Imputation (fill missing values using the median stratified by age, gender, smoking)
    {
      "action_type": "fp_set",
      "members": [
        { "fp_type": "imputer", "strata": "Age,40,100,5:Gender,1,2,1", "moment_type": "median", "tag": "need_imputer", "duplicate": "1" }
      ]
    },

    // Step 7: Normalization (for features needing normalization)
    {
      "action_type": "fp_set",
      "members": [
        { "fp_type": "normalizer", "resolution_only": "0", "resolution": "5", "tag": "need_norm", "duplicate": "1" }
      ]
    }
  ],

  // Step 8: Specify the predictor and its parameters
  "predictor": "xgb", // e.g., XGBoost
  "predictor_params": "tree_method=auto;booster=gbtree;objective=binary:logistic;..."
}
```

**How it works:**

1. The pipeline loads additional processors from a separate JSON file (for modularity).
2. It generates demographic and behavioral features.
3. It creates diagnosis-based categorical features.
4. It computes statistical features over defined time windows.
5. It removes features with little variation.
6. It imputes missing values using well-defined rules.
7. It normalizes certain features.
8. It trains the model using XGBoost, with custom parameters.


This example uses an additional file "full_rep_processors.json" next to it. Here is the content inside

<details>
       <summary>full_rep_processors.json</summary>

```json title="full_rep_processors.json"
{
  "action_type": "rp_set",
  "members": [
	{
	  "rp_type":"conf_cln",
	  "conf_file":"path_rel:cleanDictionary.csv",
	  "time_channel":"0",
	  "clean_method":"confirmed",
	  "signal":"file_rel:all_rules_sigs.list",
	  "print_summary" : "1",
	  "nrem_suff":"nRem"
	  //,"verbose_file":"/tmp/cleaning.log"
	},
	{
	  "rp_type":"conf_cln",
	  "conf_file":"path_rel:cleanDictionary.csv",
	  "val_channel":["0", "1"],
	  "clean_method":"confirmed",
	  "signal": ["BP"],
	  "print_summary" : "1",
	  "nrem_suff":"nRem"
	  //,"verbose_file":"/tmp/cleaning.log"
	}
  ]
},
{
  "action_type": "rp_set",
  "members": [
	{
	  "rp_type":"sim_val",
	  "signal":"file_rel:all_rules_sigs.list",
	  "type":"remove_diff",
	  "debug":"0"
	}
	
  ]
},
{
  "action_type": "rp_set",
  "members": [
	{
	  "rp_type":"rule_cln",
	  "addRequiredSignals":"1",
	  "time_window":"0",
	  "tolerance":"0.1",
	  "calc_res":"0.1",
	  "rules2Signals":"path_rel:ruls2Signals.tsv",
	  "consideredRules":[ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22" ] 
	  
	  //,"verbose_file":"/tmp/panel_cleaning.log"
	}
  ]
},
{
  "action_type": "rp_set",
  "members": [
	{
	  "rp_type":"complete",
	  "sim_val":"remove_diff",
	  "config":"path_rel:completion_metadata",
	  "panels":["red_line", "white_line", "gcs", "bmi"]
	},
	{
	  "rp_type":"calc_signals",
	  "calculator":"eGFR",
	  "missing_value":"-65336",
	  "work_channel":"0",
	  "names":"eGFR_CKD_EPI",
	  "signals_time_unit":"Date",
	  "max_time_search_range":"0",
	  "signals":"Creatinine,GENDER,BDATE",
	  "calculator_init_params":"{mdrd=0;ethnicity=0}"
	},
	{
	  "rp_type":"calc_signals",
	  "calculator":"eGFR",
	  "missing_value":"-65336",
	  "work_channel":"0",
	  "names":"eGFR_MDRD",
	  "signals_time_unit":"Date",
	  "max_time_search_range":"0",
	  "signals":"Creatinine,GENDER,BDATE",
	  "calculator_init_params":"{mdrd=1;ethnicity=0}"
	}
  ]
}  
```
</details>

* It uses `conf_cln` for configuring simple and fixed outliers by valid range and configuration file `cleanDictionary.csv` with those ranges.
* It uses `all_rules_sigs.list` to list down all the avaible signals are create cleaner for each of those signals. See [List Expension](#4-advanced-list-expansion) fo mkore details
* It uses `sim_val` to remove inputs on the same date with contradicting values and remove duplicate rows if the values are the sames
* It uses `rule_cln` to clear outliers based on equations and relations between signals. Gor example: BMI=Weight/Height^2, if a difference of more than tolerance (default is 10%) observed the values will be dropped. We can configure using `ruls2Signals.tsv` what happens if contradiction observed, whather to drop all signals in the relation, or just one specific - for example drop only the BMI. 
* It uses `complete` - to complete missing values in panels from other relational signals. For example BMI is missing and we have Weight, Height. It uses `completion_metadata` to control the resulted signals resolution. 
* It uses `calc_signals` to generate virtual signals for eGFR.

### 3. Referencing Other Files

To keep your pipeline modular and maintainable, you can reference external files directly in your JSON configuration. Here are the supported reference types:

- `"json:somefile.json"`: Imports another JSON file containing additional pipeline components.
- `"file_rel:signals.list"`: Loads a list of values from a file and expands them as a JSON array. Useful for features or signals lists. For details on how lists are expanded, see [List Expansion](#4-advanced-list-expansion).
- `"path_rel:config.csv"`: Uses a relative path to point to configuration files, resolved relative to the current JSON file's location.
- `"comma_rel:somefile.txt"`: Reads a file line by line and produces a single comma-separated string of values (`"line1,line2,..."`). Unlike `"file_rel"`, this will not create a JSON list, but rather a flat, comma-delimited string.

These options allow you to keep configuration modular, re-use existing resources, and simplify large or complex pipelines.

### 4. Advanced: List Expansion

If you use lists for fields (e.g., multiple signals or time windows), the pipeline automatically expands to cover all combinations (Cartesian product).

```json
{
  "type": ["last", "avg"],
  "window": ["win_from=0;win_to=180", "win_from=0;win_to=365"]
}
```
This generates steps for each type × window combination.

### 5. Reference Lists

At the end of your JSON, you can define reusable value lists, such as drug codes or signals:

```json
"diabetes_drugs": "ATC_A10,ATC_A11,ATC_A12"
```
Reference these in your pipeline using `"ref:diabetes_drugs"`.

---

## Ready to Write Your Own?

By following this walkthrough, you can confidently define new model JSON files:

- Start with the general fields
- List your pipeline steps in `model_actions`
- Modularize and reuse with references
- Expand lists for coverage
- Define your predictor and parameters

**Tip:** For a new project, copy and adapt the example above to fit your own signals, features, and model goals.

## Further Reading

- [Rep Processors Practical Guide](01.Rep%20Processors%20Practical%20Guide)
- [Feature Generator Practical Guide](02.Feature%20Generator%20Practical%20Guide)
- [FeatureProcessor practical guide](03.FeatureProcessor%20practical%20guide)
- [MedPredictor practical guide](04.MedAlgo%20Library/MedPredictor%20practical%20guide)
- [PostProcessors Practical Guide](05.PostProcessors%20Practical%20Guide)

