# Infrastructure Home Page

## Overview of Medial Infrastructure
Medial Infrastructure is designed to turn the Electronic Medical Record (EMR)-a complex, semi-structured time-series dataset, into a machine-learning-ready resource. Unlike images or free text, EMR data can be stored in countless formats, and its "labels" (the outcomes or targets you want to predict) aren’t always obvious. We address this by standardizing both the storage and the processing of time-series signals.
We can think about this infrastructure as "TensorFlow" of medical data machine learning. 

### Howto Use this
Suppose you're a potential user or client interested in using a specific model.
You're not concerned with how the model was built or which tools were used, you simply want to deploy and use it.
Please refer to this page: [Howto use AlgoMarker](AlgoMarkers/Howto%20Use%20AlgoMarker.md)

### Main contributers from recent years:
- [Avi Shoshan](https://www.linkedin.com/in/avi-shoshan-a684933b/)
- [Yaron Kinar](https://www.linkedin.com/in/yaron-kinar-il/)
- [Alon Lanyado](https://www.linkedin.com/in/lanyado/)

### Challenges
- **Variety of Questions**: Risk prediction (e.g., cancer, CKD), compliance, diagnostics, treatment recommendations
- **Medical Data Complexity**: Temporal irregularity, high dimensionality (>100k categories), sparse signals, multiple data types
- **Retrospective Data Issues**: Noise, bias, spurious patterns, policy sensitivity

### Goals
- Avoid reinventing common methodologies each project. Sometimes complicated code/logic with debugging
- Maintain shareable, versioned, regulatory‑compliant pipelines
- Facilitate reproducible transfer from research to product
- Provide end-to-end support: data import → analysis → productization

### Platform Requirements
- **Performance**: Ultra-efficient in memory & time (>100x compare to native python pandas in some cases, mainly in preprocessing)
- **Extensibility**: Rich APIs, configurable pipelines, support new data types
- **Minimal Rewriting & Ease Of Usage**: JSON‑driven configs, unified codebase, python API to the C library
- **Comprehensive**: From "raw" data to model deployment
- **Reproducible & Versioned**: Track data, code, models, and parameters

## Infrastructure Components
1. **MedRepository: a high-performance EMR time-series store**
    * Fast retrieval of any patient’s full record or a specific signal across all patients.
    * [Unified representation](00.InfraMed%20Library%20page/Generic%20(Universal)%20Signal%20Vectors.md): each signal consists of zero or more time channels plus zero or more value channels, all tied to a patient ID.
        - Static example: "Birth year" → no time channels, one value channel.
        - Single-time example: "Hemoglobin" → one time channel (test date), one value channel (numeric result).
        - Interval example: "Hospitalization" → two time channels (admission and discharge dates).
    * **Hierarchical support for categorical medical ontologies** 
        - Enables seamless integration and translation between different systems when working with a frozen model or algorithm. 
        - Example: A query for ICD-10 codes starting with "J" (respiratory diseases) will also automatically map to corresponding categories in systems like Epic. When dictionary of mapping between ICD and Epic is added, no need to change the model. 
        - Ontology mappings are managed by [MedDictionary](00.InfraMed%20Library%20page/MedDictionary.md), which supports many-to-many hierarchical relationships across coding systems.
2. **Modular processing pipeline (sklearn-style)**
    * **[Rep Processors](01.Rep%20Processors%20Practical%20Guide/)**: Clean or derive "raw" virtual signals, while preventing leakage of future data
        - Example: Outlier cleaner that omits values only when abnormality is detected by future readings (e.g., a hemoglobin value on 2023-Feb-04 flagged only by a 2023-May-21 test remains until after May 21).
        - Example: Virtual BMI signal computed from weight/height, or imputed when only two of three inputs exist
    * **[Feature Generators](MedProcessTools%20Library/FeatureGenerator/)**: Convert cleaned signals into predictive features.
        - Examples:
            * "Last hemoglobin in past 365 days"
            * "Hemoglobin slope over three years"
            * "COPD diagnosis code during any emergency admission in last three years"
    * **[Feature Processors](02.Feature%20Generator%20Practical%20Guide/)**: Operate on the feature matrix—imputation, selection, PCA, etc. 
    * **[Predictors/Classifiers](04.MedAlgo%20Library/)**: LightGBM, XGBoost, or custom algorithms.
    * **[Post-processing](05.PostProcessors%20Practical%20Guide/)**: Score calibration, explainability layers, fairness adjustments, etc.
3. **JSON-driven pipeline configuration** - Define every processor, feature generator, and model step in a single JSON file. [Json Format](MedModel%20json%20format.md)
    Example json for training a model:

<details>
       <summary>Click to expend</summary>


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



4. Comprehensive evaluation toolkit
    * [Bootstrap-based](/Medial%20Tools/bootstrap_app/) cohort analysis allows batch testing across thousands of user-defined subgroups (e.g., age 50–80, males only, prediction window of 365 days, COPD patients).
    * Automatically extracts AUC, ROC points at each 1% FPR increment, odds ratios, PPV/NPV, and applies incidence-rate adjustments or KPI weights
    * Includes explainability and fairness audits
5. **Unified API wrapper for production deployment**
    * Ready for productization out of the box, no need to reinvent integration or design a new interface each time. See [AlgoMarker](AlgoMarkers/)
    * Packages the entire end-to-end pipeline (raw time-series ingestion through inference) into a single, stable SDK.
    * Core infrastructure implemented in C++ for performance and portability, with a lightweight [Python wrapper](/Python) for seamless integration.
    * Although powered by C++, the team mainly uses and maintains workflows via the Python SDK, ensuring rapid development and minimal friction. Experienced user might use the C++ API more often, since the python interface is more limited. 


## Basic Pages

- MedModel learn and apply 
- RepProcessors:
    - [RepProcessors Practical Page](01.Rep%20Processors%20Practical%20Guide)
- FeatureGenerators:
    - [Feature Generator Practical Guide](02.Feature%20Generator%20Practical%20Guide)
- FeatureProcessors:
    - [FeatureProcessor practical guide](03.FeatureProcessor%20practical%20guide)
- MedPredictors
    - [MedPredictors practical guide](04.MedAlgo%20Library/MedPredictor%20practical%20guide)
- PostProcessors:
    - [PostProcessors Practical Guide](05.PostProcessors%20Practical%20Guide)

## Other links
Home page for in depth pages explaining several different aspects in the infrastructure
Some interesting pages:

- [Setup Environment](../New%20employee%20landing%20page/index.md#setup)
- How to Serialize : learn the [SerializableObject](MedProcessTools%20Library/SerializableObject.md) libarary secrets.
- [PidDynamicRecs and versions](00.InfraMed%20Library%20page/PidDynamicRec.md)
- [Virtual Signals](01.Rep%20Processors%20Practical%20Guide/Virtual%20Signals.md)
