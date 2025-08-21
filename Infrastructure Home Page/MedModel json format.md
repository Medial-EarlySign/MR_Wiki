# MedModel JSON Format

Refer to `MedModel::init_from_json_file` for implementation details.

## General Fields

Use only the first field, `"model_json_version"`, the rest have default values so change them only if needed:

- `"model_json_version"`: Specify `2`.
- `"serialize_learning_set"`: Boolean (`0` or `1`). If enabled, stores learning samples in the model. Default: `0`.
- `"generate_masks_for_features"`: Boolean (`0` or `1`). If enabled, stores for each feature whether the value was imputed (important for explainers and MASK predictor during calibration). Default: `0`.
- `"max_data_in_mem"`: Maximum size of a vector the machine can hold (default: `MAX_INT`). Limits number of rows × number of features. Larger values split model apply into batches.
- `"take_mean_pred"`: Boolean (`0` or `1`). If enabled, averages predictions; otherwise, uses median. Default: `1`. Currenly relevant only for [Multiple Imputations](05.PostProcessors%20Practical%20Guide/MultipleImputations.md) mode

You can use these prefixes for referencing files relative to the JSON:

- `path_rel:`: References a file with a relative path, resolves to absolute path from JSON location.
- `file_rel:`: References a file, extracts content line by line into a list of actions (`["line1", "line2", ...]`).
- `comma_rel:`: References a file, extracts content line by line into a comma-separated string (`"line1,line2,..."`).
- `json:`: References another file, adds its content to this JSON as-is.

The parameters in the model can be later changed using [adjust_model](/Medial%20Tools/adjust_model.html)or [change_model](/Medial%20Tools/change_model).
For example, if you are implementing running an existing model in lower memory computer, you might want to lower down `max_data_in_mem`.
[Howto limit memory](/Medial%20Tools/change_model/How%20to%20limit%20memory%20usage%20in%20predict.html)

## Main Model Pipeline

Model pipeline instructions are listed under `"model_actions"` (an array of model components):

```json
{
  "model_json_version": "2",
  "model_actions": [
    // List model components here, each as an object {}
  ]
}
```

### List Expansion

When specifying a list of values for a field, the element is duplicated for each value:

```json
{
  "field_1": "A",
  "field_2": ["val_1", "val_2", "val_3"]
}
```

Is equivalent to:

```json
{ "field_1": "A", "field_2": "val_1" },
{ "field_1": "A", "field_2": "val_2" },
{ "field_1": "A", "field_2": "val_3" }
```

Multiple lists create a cartesian product of all options.

## Model Components

Components inside `"model_actions"` are executed in order. Blocks can be executed in parallel; feature generators are always parallel.

Each component has an `"action_type"` field (default: `"feat_generator"`). Place it first for readability.

Available `action_type` options:

- `rp_set`: Set of [rep_processors](01.Rep%20Processors%20Practical%20Guide) executed in parallel. Contains `"members"` (array of rep_processors, each with `"rp_type"` and parameters).
- `fp_set`: Set of [feature_processors](03.FeatureProcessor%20practical%20guide) executed in parallel. Contains `"members"` (array of feature_processors).
- `rep_processor`: Single rep_processor. See [Rep Processors Practical Guide](01.Rep%20Processors%20Practical%20Guide) or [RepProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/RepProcess_8h.html#a2772b5cb2b32efafbbd8ba9440b9576a).
- `feat_generator`: Feature generator. See [Feature Generator Practical Guide](03.FeatureProcessor%20practical%20guide) or [FeatureGeneratorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureGenerator_8h.html#a109794c7f375415720a0af5dd3132023).
- `feat_processor`: Feature processor. See [Feature Processor Practical Guide](03.FeatureProcessor%20practical%20guide) or [FeatureProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureProcess_8h.html#ae648a97312d7df5b3f5cf01b19887334). To apply on multiple features, add `"tag"` (value to search for features) and `"duplicate": "1"`. This creates a MultiFeatureProcessor that scans all features, generating child processors after filtering by tag.
- `post_processor`: Feature processor. See [PostProcessors Practical Guide](05.PostProcessors%20Practical%20Guide) or [PostProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/PostProcessor_8h.html#a1dab070b8206be89206ff19f321a1cfc).

Example of `"rp_set"` block (similar for `"fp_set"`):

```json
{
  "action_type": "rp_set",
  "members": [
    // List rep processor components here, each as an object with "rp_type" field...
  ]
}
```

## Predictor

In the last part of the JSON, after `"model_actions"`:

- `"predictor"`: Selects MedPredictor to train on the generated matrix. See [MedPredictor practical guide](04.MedAlgo%20Library/MedPredictor%20practical%20guide) and [List of options](https://Medial-EarlySign.github.io/MR_LIBS/MedAlgoh.html#ab3f9aacffd8e29e833677299133ac4f0). Examples: `"xgb"` for xgboost, `"lightgbm"` for LightGBM, `"lm"` for linear model, etc.
- `"predictor_params"`: Arguments to initialize the predictor, depending on the chosen predictor.

## Reference Lists

- You can add lists of values at the end for reference in the model_actions. For example, `"diabetes_drugs": "ATC_A______,ATC_...."` can be referenced using `"ref:diabetes_drugs"` in the model_actions.


## Full example

<details>
       <summary>Click to expend example json</summary>


```json title="example json"
   {
	"model_json_version": "2",
	"serialize_learning_set": "0",
	"model_actions": [
		"json:full_rep_processors.json", // Import a json from current folder with other componenets - in this case, outlier cleaners, signal panel completers, etc.
    // Features
		{
			"action_type": "feat_generator",
			"fg_type": "age"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "gender"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "unified_smoking",
			"tags": "smoking",
			"smoking_features": "Current_Smoker, Ex_Smoker, Unknown_Smoker, Never_Smoker, Passive_Smoker, Smok_Days_Since_Quitting , Smok_Pack_Years_Max, Smok_Pack_Years_Last,Smoking_Years,Smoking_Intensity"
		},
		// Cancers in Dx
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=10950"
			],
			"time_unit": "Days",
			"sets": [
				"ICD9_CODE:140-149,ICD9_CODE:150-159,ICD9_CODE:160-165,ICD9_CODE:170,ICD9_CODE:171,ICD9_CODE:172,ICD9_CODE:174,ICD9_CODE:175,ICD9_CODE:176,ICD9_CODE:179-189,ICD9_CODE:200-208,ICD9_CODE:209.0,ICD9_CODE:209.1,ICD9_CODE:209.2,ICD9_CODE:290.3,ICD9_CODE:230-234"
			],
			"signal": "ICD9_Diagnosis",
			"in_set_name": "Cancers"
		},
    // Statistical features - will take: last, average, min, max, etc. for each time window: 0-180, 0-365. 365-730, 0-1095 prior prediction day in days and for each signal: Hemoglobin, WBC...
    // In total will create: 8*4*4 = 128 features
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": [
				"last",
				"last_delta",
				"avg",
				"max",
				"min",
				"std",
				"slope",
				"range_width"
			],
			"window": [
				"win_from=0;win_to=180",
				"win_from=0;win_to=365",
				"win_from=365;win_to=730",
				"win_from=0;win_to=1095"
			],
			"time_unit": "Days",
			"tags": "labs_and_measurements,need_imputer,need_norm",
			"signal": [
				"Hemoglobin",
				"WBC",
				"Platelets",
				"Albumin"
			]
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": [
				"last_time"
			],
			"window": [
				"win_from=0;win_to=180",
				"win_from=0;win_to=365",
				"win_from=365;win_to=730",
				"win_from=0;win_to=1095"
			],
			"time_unit": "Days",
			"tags": "labs_and_measurements,need_imputer,need_norm",
			//Take only panels - to remove repititions:
			"signal": [
				"BMI",
				"Creatinine",
				"WBC",
				"Cholesterol",
				"Glucose",
				"Hemoglobin",
				"Albumin"
			]
		},
		{
			"action_type": "feat_generator",
			"fg_type": "category_depend",
			"signal": "DIAGNOSIS",
			"window": [
				"win_from=0;win_to=10950;tags=numeric.win_0_10950",
				"win_from=0;win_to=365;tags=numeric.win_0_365"
			],
			"time_unit_win": "Days",
			"regex_filter": "ICD10_CODE:.*",
			"min_age": "40",
			"max_age": "90",
			"age_bin": "5",
			"min_code_cnt": "200",
			"fdr": "0.01",
			"lift_below": "0.7",
			"lift_above": "1.3",
			"stat_metric": "mcnemar",
			"max_depth": "50",
			"max_parents": "100",
			"use_fixed_lift": "1",
			"sort_by_chi": "1",
			"verbose": "1",
			"take_top": "50"
		},
		// Feature selector to remove features with 99.9% same value, there are other options, like lasso, by model importance, etc.
		{
			"action_type": "fp_set",
			"members": [
				{
					"fp_type": "remove_deg",
					"percentage": "0.999"
				}
			]
		},
		// Imputer - simple choise of choosing median value by stratifying to age, gender and smoking status - will commit for all features with "need_imputer" tag
		{
			"action_type": "fp_set",
			"members": [
				{
					"fp_type": "imputer",
					"strata": "Age,40,100,5:Gender,1,2,1:Current_Smoker,0,1,1:Ex_Smoker,0,1,1",
					"moment_type": "median",
					"tag": "need_imputer",
					"duplicate": "1"
				}
			]
		},
		// Normalizer - will commit for all features with "need_imputer" tag
		{
			"action_type": "fp_set",
			"members": [
				{
					"fp_type": "normalizer",
					"resolution_only": "0",
					"resolution": "5",
					"tag": "need_norm",
					"duplicate": "1"
				}
			]
		}
	],
	"predictor": "xgb",
	"predictor_params": "tree_method=auto;booster=gbtree;objective=binary:logistic;eta=0.050;alpha=0.000;lambda=0.010;gamma=0.010;max_depth=6;colsample_bytree=0.800;colsample_bylevel=1.000;min_child_weight=10;num_round=200;subsample=0.800" }
```

</details>


This example uses an additional file "full_rep_processors.json" next to it with this content:

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

full_rep_processors.json also uses reference files which makes the management of the json easier:

<details>
       <summary>all_rules_sigs.list - list with all supported signals, each signal name spears in a different line, easier to define all known signals once in a separate file</summary> 

```text title="all_rules_sigs.list"
Albumin
ALKP
ALT
Amylase
AST
B12
Basophils#
Basophils%
Bicarbonate
Bilirubin
BMI
Ca
CA125
Cholesterol
Cholesterol_over_HDL
CK
Cl
CO2
CorrectedCa
Creatinine
CRP
Digoxin
eGFR
Eosinophils#
Eosinophils%
Erythrocyte
Ferritin
Fibrinogen
Follic_Acid
FreeT3
FreeT4
FSH
GFR
GGT
Globulin
Glucose
HbA1C
HDL
HDL_over_Cholesterol
HDL_over_LDL
HDL_over_nonHDL
Height
Hematocrit
Hemoglobin
INR
Iron_Fe
K+
LDH
LDL
LDL_over_HDL
Lithium
LUC
LuteinisingHormone
Lymphocytes#
Lymphocytes%
MCH
MCHC-M
MCV
Mg
Monocytes#
Monocytes%
MPV
Na
Neutrophils#
Neutrophils%
NonHDLCholesterol
NRBC
PDW
PFR
Phosphore
PlasmaAnionGap
PlasmaViscosity
Platelets
Platelets_Hematocrit
Progesterone
Prolactin
Protein_Total
PSA
PULSE
RandomGlucose
RBC
RDW
Reticulocyte
Rheumatoid_Factor
Serum_Oestradiol
SerumAnionGap
Sex_Hormone_Binding_Globulin
T4
Testosterone
TIBC
Transferrin
Transferrin_Saturation_Index
Triglycerides
TSH
Urea
Uric_Acid
Urine_Dipstick_pH
Urine_Epithelial_Cell
Urine_Microalbumin
Urine_Protein_Creatinine
UrineAlbumin
UrineAlbumin_over_Creatinine
UrineCreatinine
UrineTotalProtein
VitaminD_25
WBC
Weight
Band%
Blast%
Gleason_1
Gleason_2
Gleason_Total
PSA_Ratio
PT_Seconds
PTP
PTT
TEMP
Urine_Bilirubin
Urine_Erythrocytes
Urine_Glucose
Urine_Ketone
Urine_Leukocytes
Urine_Nitrite
Urine_PH
Urine_Protein
Urine_Urubilinogen
Fev1
Smoking_Duration
Smoking_Intensity
Pack_Years
```
</details>


<details>
       <summary>cleanDictionary.csv - file with definition of all outliers for each signal</summary>

```text title="cleanDictionary.csv"
name,logicalN,logicalH,low bound,low dist,high bound,high dist,val_channel
Albumin,1,1.00E+99,none,none,7.2,norm,0
ALKP,0.1,1.00E+99,none,none,5000,lognorm,0
ALT,0.1,1.00E+99,none,none,6500,lognorm,0
Amylase,0.1,1.00E+99,none,none,6000,lognorm,0
AST,0.1,1.00E+99,none,none,6000,lognorm,0
B12,1,1.00E+99,none,none,2500,lognorm,0
Basophils#,0,1.00E+99,none,none,18,lognorm,0
Basophils%,0,100,none,none,25,lognorm,0
Bicarbonate,0.1,1.00E+99,5.048214541,norm,48.02457951,norm,0
Bilirubin,0,1.00E+99,none,none,50,lognorm,0
BMI,5,1.00E+99,none,none,70,norm,0
Ca,0.1,1.00E+99,0.1,lognorm,20,lognorm,0
CA125,0,1.00E+99,none,none,10000,lognorm,0
Cholesterol,1,1.00E+99,none,none,1200,lognorm,0
Cholesterol_over_HDL,1,1.00E+99,none,none,36.09669438,lognorm,0
CK,0,1.00E+99,none,none,3000,lognorm,0
Cl,0.1,1.00E+99,0.1,lognorm,140,lognorm,0
CO2,1,1.00E+99,none,none,52.46921412,norm,0
CorrectedCa,0.1,1.00E+99,0.1,lognorm,20,lognorm,0
Creatinine,0,1.00E+99,none,none,20,lognorm,0
CRP,0,1.00E+99,none,none,300,lognorm,0
Digoxin,0,1.00E+99,none,none,88.49217997,lognorm,0
eGFR,0,1.00E+99,none,none,160,lognorm,0
Eosinophils#,0,1.00E+99,none,none,50,lognorm,0
Eosinophils%,0,100,none,none,100,none,0
Erythrocyte,0,1.00E+99,none,none,13772.43655,lognorm,0
Ferritin,0,1.00E+99,none,none,20000,lognorm,0
Fibrinogen,0,1.00E+99,none,none,3500,lognorm,0
Follic_Acid,0,1.00E+99,none,none,30,lognorm,0
FreeT3,0.001,1.00E+99,none,none,46.79056395,lognorm,0
FreeT4,0.001,1.00E+99,none,none,64.27336088,lognorm,0
FSH,0,1.00E+99,none,none,45399.78,lognorm,0
GFR,0,1.00E+99,none,none,146,lognorm,0
GGT,0,1.00E+99,none,none,8000,lognorm,0
Globulin,0,1.00E+99,none,none,87.00820496,lognorm,0
Glucose,10,1.00E+99,none,none,5000,lognorm,0
HbA1C,0.1,100,none,none,50,lognorm,0
HDL,0,1.00E+99,none,none,420,lognorm,0
HDL_over_Cholesterol,0,1.00E+99,none,none,1,lognorm,0
HDL_over_LDL,0,1.00E+99,none,none,12.19513883,lognorm,0
HDL_over_nonHDL,0,1.00E+99,none,none,2.029837851,norm,0
Height,20,1.00E+99,none,none,300,norm,0
Hematocrit,0.1,100,none,none,75,norm,0
Hemoglobin,2,100,none,none,25,norm,0
INR,0.01,1.00E+99,none,none,11,manual,0
Iron_Fe,1,1.00E+99,none,none,700,norm,0
K+,1.5,1.00E+99,1.5,lognorm,11,lognorm,0
LDH,1,1.00E+99,none,none,12000,lognorm,0
LDL,1,1.00E+99,none,none,2000,lognorm,0
LDL_over_HDL,0,1.00E+99,none,none,51.72779688,lognorm,0
Lithium,0,1.00E+99,none,none,150,lognorm,0
LUC,0,1.00E+99,none,none,2.817745324,lognorm,0
LuteinisingHormone,0,1.00E+99,none,none,12098.73012,lognorm,0
Lymphocytes#,0,1.00E+99,none,none,500,lognorm,0
Lymphocytes%,0,100,none,none,100,none,0
MCH,0.01,1.00E+99,none,none,500,norm,0
MCHC-M,0.1,1.00E+99,none,none,200,norm,0
MCV,1,1.00E+99,none,none,150,norm,0
Mg,0.01,1.00E+99,none,none,2.113294532,lognorm,0
Monocytes#,0,1.00E+99,none,none,40,lognorm,0
Monocytes%,0,100,none,none,100,none,0
MPV,0.1,1.00E+99,none,none,27,lognorm,0
Na,100,1.00E+99,100,lognorm,200,lognorm,0
Neutrophils#,0,1.00E+99,none,none,150,lognorm,0
Neutrophils%,0,100,none,none,100,none,0
NonHDLCholesterol,0,1.00E+99,none,none,1401.434359,lognorm,0
NRBC,0,1.00E+99,none,none,3476.436337,lognorm,0
PDW,0,100,none,none,39.42776545,lognorm,0
PFR,0,1.00E+99,none,none,1328.242946,norm,0
Phosphore,0.1,1.00E+99,none,none,20,norm,0
PlasmaAnionGap,-1.00E+99,1.00E+99,-4.790862408,norm,38.30832862,norm,0
PlasmaViscosity,0.1,1.00E+99,none,none,5.093440521,lognorm,0
Platelets,0.1,1.00E+99,none,none,3000,lognorm,0
Platelets_Hematocrit,0.01,100,none,none,none,none,0
Progesterone,0,1.00E+99,none,none,724363.8626,lognorm,0
Prolactin,0,1.00E+99,none,none,16288.44876,lognorm,0
Protein_Total,0.1,1.00E+99,none,none,15,lognorm,0
PSA,0,1.00E+99,none,none,5000,lognorm,0
PULSE,1,300,none,none,285.3549087,lognorm,0
RandomGlucose,1,1.00E+99,none,none,1136.372137,lognorm,0
RBC,0,1.00E+99,none,none,10,norm,0
RDW,0,100,none,none,100,lognorm,0
Reticulocyte,0,1.00E+99,none,none,17270.35704,lognorm,0
Rheumatoid_Factor,0,1.00E+99,none,none,3021.474146,lognorm,0
Serum_Oestradiol,0,1.00E+99,none,none,188460.5286,lognorm,0
SerumAnionGap,-1.00E+99,1.00E+99,-7.763505351,norm,34.21884248,norm,0
Sex_Hormone_Binding_Globulin,0,1.00E+99,none,none,3209.154851,lognorm,0
T4,0.001,1.00E+99,none,none,40.14304291,norm,0
Testosterone,0,1.00E+99,none,none,572.4061104,lognorm,0
TIBC,0,1.00E+99,none,none,146.4669744,norm,0
Transferrin,10,1.00E+99,none,none,1250,lognorm,0
Transferrin_Saturation_Index,0,100,none,none,none,none,0
Triglycerides,5,1.00E+99,none,none,10000,lognorm,0
TSH,0,1.00E+99,none,none,302.8916089,lognorm,0
Urea,0,1.00E+99,none,none,600,lognorm,0
Uric_Acid,0,1.00E+99,none,none,50,lognorm,0
Urine_Dipstick_pH,0,14,none,none,12.65839393,lognorm,0
Urine_Epithelial_Cell,0,1.00E+99,none,none,464267.9586,lognorm,0
Urine_Microalbumin,0,1.00E+99,none,none,99771.15903,lognorm,0
Urine_Protein_Creatinine,0,1.00E+99,none,none,29928.16788,lognorm,0
UrineAlbumin,0,1.00E+99,none,none,113282.8368,lognorm,0
UrineAlbumin_over_Creatinine,0,1.00E+99,none,none,20116.5322,lognorm,0
UrineCreatinine,0,1.00E+99,none,none,3007.223193,lognorm,0
UrineTotalProtein,0,1.00E+99,none,none,159.820147,lognorm,0
VitaminD_25,0,1.00E+99,none,none,500,lognorm,0
WBC,0.01,1.00E+99,none,none,150,manual,0
Weight,1,1.00E+99,none,none,300,norm,0
Band%,0,100,none,none,100,none,0
Blast%,0,100,none,none,100,none,0
Gleason_1,0.9,5.1,none,none,5.1,none,0
Gleason_2,0.9,5.1,none,none,5.1,none,0
Gleason_Total,1.9,10.1,none,none,10.1,none,0
PSA_Ratio,0,50,none,none,50,none,0
PT_Seconds,8,180,none,none,180,none,0
PTP,3.9,140,none,none,140,none,0
PTT,16,150,none,none,150,none,0
TEMP,31.9,45,none,none,45,none,0
Urine_Bilirubin,0,50,none,none,50,none,0
Urine_Erythrocytes,0,1000,none,none,1000,none,0
Urine_Glucose,0,1500,none,none,1500,none,0
Urine_Ketone,0,200,none,none,200,none,0
Urine_Leukocytes,0,1000,none,none,1000,none,0
Urine_Nitrite,0,1.1,none,none,1.1,none,0
Urine_PH,0,10,none,none,10,none,0
Urine_Protein,0,2000,none,none,2000,none,0
Urine_Urubilinogen,0,20,none,none,20,none,0
BP,20,200,none,none,200,none,0
BP,50,300,none,none,300,none,1
Fev1,0,1000,none,none,500,none,0
Smoking_Duration,0,120,none,none,120,none,0
Smoking_Intensity,0,200,none,none,200,none,0
Pack_Years,0,300,none,none,300,none,0
```
</details>

<details>
       <summary>ruls2Signals.tsv - definition of panel outlier cleaning</summary>
    
```text title="ruls2Signals.tsv"
1	BMI,Weight,Height	BMI
2	MCH,Hemoglobin,RBC
3	MCV,Hematocrit,RBC
4	MCHC-M,MCH,MCV
5	Eosinophils#,Monocytes#,Basophils#,Lymphocytes#,Neutrophils#,WBC
6	MPV,Platelets_Hematocrit,Platelets
7	UrineAlbumin,UrineTotalProtein
8	UrineAlbumin_over_Creatinine,UrineAlbumin,UrineCreatinine
9	LDL,HDL,Cholesterol
10	NonHDLCholesterol,HDL,Cholesterol
11	HDL_over_nonHDL,HDL,NonHDLCholesterol	HDL_over_nonHDL
12	HDL_over_Cholesterol,HDL,Cholesterol	HDL_over_Cholesterol
13	HDL_over_LDL,HDL,LDL	HDL_over_LDL
14	HDL_over_LDL,LDL_over_HDL	HDL_over_LDL
15	Cholesterol_over_HDL,Cholesterol,HDL	Cholesterol_over_HDL
17	Cholesterol_over_HDL,HDL_over_Cholesterol
18	LDL_over_HDL,LDL,HDL	LDL_over_HDL
19	Albumin,Protein_Total
20	FreeT4,T4
21	NRBC,RBC
22	CHADS2,CHADS2_VASC
#the rest - use default names
```
</details>

<details>
       <summary>completion_metadata - Definition of signals and resolutions after completion of data using panels</summary>

```text title="completion_metadata"
Name,FinalFactor,OrigResolution,FinalResolution
ALT,1,1.0,1.0
AST,1,1.0,1.0
Albumin,1,0.1,0.1
Amylase,1,1.0,1.0
B12,1,1.0,1.0
Basophils#,1,0.1,0.1
Basophils%,1,0.1,0.1
Bilirubin,1,0.01,0.01
CO2,1,0.1,0.1
Cholesterol,1,1.0,1.0
Creatinine,1,0.01,0.01
Eosinophils#,1,0.1,0.1
Eosinophils%,1,0.1,0.1
Ferritin,1,0.1,0.1
GFR,1,1.0,1.0
GGT,1,1.0,1.0
Globulin,1,0.1,0.1
Glucose,1,1.0,1.0
HbA1C,1,0.1,0.1
HDL,1,1.0,1.0
Hematocrit,1,0.1,0.1
Hemoglobin,1,0.1,0.1
INR,1,0.01,0.01
LDH,1,1.0,1.0
LDL,1,1.0,1.0
Lymphocytes#,1,0.1,0.1
Lymphocytes%,1,0.1,0.1
MCH,1,0.1,0.1
MCHC-M,1,0.1,0.1
MCV,1,0.1,0.1
Monocytes#,1,0.1,0.1
Monocytes%,1,0.1,0.1
MPV,1,0.1,0.1
Neutrophils#,1,0.01,0.01
Neutrophils%,1,0.1,0.1
NonHDLCholesterol,1,1.0,1.0
Platelets,1,1.0,1.0
RandomGlucose,1,1.0,1.0
RBC,1,0.01,0.01
Na,1,0.1,0.1
Triglycerides,1,1.0,1.0
Urea,1,1.0,1.0
WBC,1,0.1,0.1
RDW,1,0.1,0.1
BMI,1,0.01,0.01
Weight,1,1,1
Height,1,1,1
```
</details>