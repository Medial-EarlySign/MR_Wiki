# Infrastructure Home Page

## Overview of Medial Infrastructure
Medial Infrastructure is designed to turn the Electronic Medical Record (EMR)—a complex, semi-structured time-series dataset—into a machine-learning-ready resource. Unlike images or free text, EMR data can be stored in countless formats, and its “labels” (the outcomes or targets you want to predict) aren’t always obvious. We address this by standardizing both the storage and the processing of time-series signals.

## Goals
1. **MedRepository: a high-performance EMR time-series store**
    * Fast retrieval of any patient’s full record or a specific signal across all patients.
    * [Unified representation](Generic%20(Universal)%20Signal%20Vectors): each signal consists of zero or more time channels plus zero or more value channels, all tied to a patient ID.
      - Static example: “Birth year” → no time channels, one value channel.
      - Single-time example: “Hemoglobin” → one time channel (test date), one value channel (numeric result).
      - Interval example: “Hospitalization” → two time channels (admission and discharge dates).
    * **Hierarchical support for categorical medical ontologies** 
      - Enables seamless integration and translation between different systems when working with a frozen model or algorithm. 
      - Example: A query for ICD-10 codes starting with "J" (respiratory diseases) will also automatically map to corresponding categories in systems like Epic. When dictionary of mapping between ICD and Epic is added, no need to change the model. 
      - Ontology mappings are managed by [MedDictionary](InfraMed%20Library%20page/MedDictionary), which supports many-to-many hierarchical relationships across coding systems.
2. **Modular processing pipeline (sklearn-style)**
    * **[Rep Processors](Rep%20Processors%20Practical%20Guide/)**: Clean or derive “raw” virtual signals, while preventing leakage of future data
      - Example: Outlier cleaner that omits values only when abnormality is detected by future readings (e.g., a hemoglobin value on 2023-Feb-04 flagged only by a 2023-May-21 test remains until after May 21).
      - Example: Virtual BMI signal computed from weight/height, or imputed when only two of three inputs exist
    * **[Feature Generators](MedProcessTools%20Library/FeatureGenerator/)**: Convert cleaned signals into predictive features.
      - Examples:
        * “Last hemoglobin in past 365 days”
        * “Hemoglobin slope over three years”
        * “COPD diagnosis code during any emergency admission in last three years”
    * **[Feature Processors](Feature%20Generator%20Practical%20Guide/)**: Operate on the feature matrix—imputation, selection, PCA, etc. 
    * **[Predictors/Classifiers](MedAlgo%20Library/)**: LightGBM, XGBoost, or custom algorithms.
    * **[Post-processing](PostProcessors%20Practical%20Guide/)**: Score calibration, explainability layers, fairness adjustments, etc.
3. **JSON-driven pipeline configuration** - Define every processor, feature generator, and model step in a single JSON file. [Json Format](MedModel%20json%20format)
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
  - [RepProcessors Practical Page](Rep%20Processors%20Practical%20Guide)
- FeatureGenerators:
  - [Feature Generator Practical Guide](Feature%20Generator%20Practical%20Guide)
- FeatureProcessors:
  - [FeatureProcessor practical guide](FeatureProcessor%20practical%20guide)
- MedPredictors
  - [MedPredictors practical guide](MedPredictor%20practical%20guide)
- PostProcessors:
  - [PostProcessors Practical Guide](PostProcessors%20Practical%20Guide)

## Other links
Home page for in depth pages explaining several different aspects in the infrastructure
Some interesting pages:

- How to Serialize : learn the [SerializableObject](MedProcessTools%20Library/SerializableObject) libarary secrets.
- [PidDynamicRecs and versions](InfraMed%20Library%20page/PidDynamicRec)
- [Virtual Signals](Virtual%20Signals)
