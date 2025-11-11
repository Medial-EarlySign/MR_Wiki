# Medial Tools

This page describes the command-line tools and Python helpers that interact with the MES infrastructure. It explains how to prepare data, train and evaluate models, and how to use the available tools for common workflows.

## Overview

Medial EarlySign (MES) provides two main ways to work with EMR data and models:

1. A Python API that exposes many infrastructure capabilities for loading data, creating sample files, training, and inference.
2. Standalone applications (executables) that implement infrastructure workflows; these are useful when the Python API does not yet cover a specific feature.

When a model is deployed via AlgoMarker, only a small runtime API and shared library are required to produce predictions. Deployment does not require the full training API or a training data repository. Deployed models accepts JSON-formatted patient records. See [AlgoMarker](../Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md) for details.

## Setup requirements

1. Use the Python integration where possible - see the [Python](Python) section. Note that the Python package does not expose every feature. Some capabilities are still only available as executables, but [extension](Python/Extend%20and%20Develop.md) of the python library is possible. Follow the Python setup instructions: [Python API for MES Infrastructure](../Installation/Python%20API%20for%20MES%20Infrastructure.md).

2. If you need the command-line tools, follow the installation guide: [MES Tools to Train and Test Models](../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md). Each tool includes a `--help` flag that lists its arguments and options. Common tools are covered also within this Wiki.

3. To develop your own applications against the infrastructure, see the examples in the [Examples of Simple Applications](#examples-of-simple-applications) section below.

In most cases, Python plus a few tools will be sufficient - it is uncommon need to write new C++ code.

## Tutorial

### Step 1 - Create a data repository

First convert your EMR data to the MES repository format. Follow the ETL instructions: [ETL tutorial](../Infrastructure%20Library/DataRepository/ETL%20Tutorial).

Note: Use the `Flow` application to perform the actual loading into a repository. The loading API has not been ported to Python yet, so installing the MES Tools may be necessary. See [Flow loading](Using%20the%20Flow%20App/index.md#creating-repositories).

### Step 2 - Access repository data

You can access repository data in two ways:

1. Python API
    * Fetch signals as a Pandas DataFrame — [Load Signals in python](Python/Examples.md#load-some-signals)

2. Tools and UI
    * Use `Flow` to print signal summaries or export data — [Flow view signals](Using%20the%20Flow%20App/index.md#printing-pids-and-signals)
    * Open a single patient with the repository viewers UI — [Repository viewers](../Infrastructure%20Library/DataRepository/Repository%20Viewers.md)

### Step 3 - Create MedSamples

Create a tab-separated MedSamples file describing prediction times and outcomes for each patient: [MedSamples format](../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md).

Use the Python API when possible to generate MedSamples. Each row typically contains a patient identifier, prediction time, outcome (0/1 or numeric for regression), outcome time, and optional split/metadata fields.

Suggested process:

1. Generate candidate samples (patient id + date) without labels.
2. Label and exclude ineligible samples, documenting exclusions for cohort diagrams and validation.

Example (creating samples for date `20251011`):

```python
import med
rep = med.PidRepository()

rep.read_all("/path/to/repository", [], ["BDATE"])
bdate_sig = rep.get_sig("BDATE").rename(columns={"pid": "id"})

bdate_sig["EVENT_FIELDS"] = "SAMPLE"
bdate_sig["time"] = 20251011
bdate_sig["outcome"] = 0
bdate_sig["split"] = -1
bdate_sig["outcomeTime"] = 20500101

# Keep fields in the MedSamples order
bdate_sig = bdate_sig[["EVENT_FIELDS", "id", "time", "outcome", "outcomeTime", "split"]]

bdate_sig.to_csv("/path/to/samples", index=False, sep="\t")
```

> [!NOTE] 
> Keep in mind that training and test sample sets are often processed differently. For example, training sets may be rebalanced by year to avoid the model learning calendar trends. Those filtering and subsampling choices are part of study design and are under the responsibility of the data scientist to mitigate biases and potential information leakage in training.

## Training a model

1. Define the model pipeline and components in a MedModel JSON file: [MedModel JSON format](../Infrastructure%20Library/MedModel%20json%20format.md).
2. Train the model using either:
    * Python: [Train Model Using Python API](Python/Examples.md#learn-model-from-json-to-generate-matrix)
    * Tools:
        * [Training with Flow](Using%20the%20Flow%20App/index.md#training-a-model) - simple training run without hyperparameter search
        * [Optimizer](Optimizer.md) - grid-search-style training with penalties to balance generalization (note: Optuna can be used externally for more flexible tuning)

## Applying a model

You can generate predictions or extract the feature matrix produced by a model pipeline.

- [Apply a model using Python](Python/Examples.md#load-medmodel-and-apply-predict-on-sample)
- [Apply a model with Flow](Using%20the%20Flow%20App/index.md#predictingapplying-a-model)

## Model evaluation

Please refer to our suggested [Checklist](Model%20Checklist) for model evaluation
Common evaluation tools and workflows used in MES:

1. [bootstrap_app](bootstrap_app) - bootstrap-based performance analysis with cohort and subgroup filtering. For example, we might want to test performance in different sub-cohorts: time window, age range, etc.
2. Feature importance and post-processing - see [Flow post-processors](../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md).
3. Explainability - add model explainers as post-processors. See the [Explainers Guide](../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md#adding-an-explainer-to-an-existing-model) and our patent [US20240161005A1](https://patents.google.com/patent/US20240161005A1) for the MES-specific approach. Recognizing that standard Shapley values struggle with high-dimensional, correlated medical data, we developed a specialized extension. This new method was validated by our clinicians in a blinded study against other explainability techniques and was a key component of our award-winning submission to the [CMS Health AI Outcome Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge). The results are published, but some of the process can be seen in the Research tab of this wiki.
4. Covariate-shift / simulation tools - [Simulator](Simulator.md).
5. Automated checks - [AutoTest](Model%20Checklist/AutoTest), a pipeline of tests derived from the Model Checklist.

## Other tools and utilities

* [Add calibration and calibration tests](Calibrate%20model,%20and%20calibration%20test.md)
* [Fairness extraction](Fairness%20extraction.md): Calculates fairness metrics.
* [Adjust Model](adjust_model.md): Adds components like rep_processors or post_processors to an existing model. Usefull for example, if we want to noise the input, drop values or other manipulations that we don't want to store in the model pipeline during training.
* [Model Signals Importance](model_signals_importance.md): Evaluates the importance of signals in an existing model and measures the impact of including or excluding them on performance.
* [Iterative Feature Selector](Iterative%20Feature%20Selector.md): Iteratively selects features or groups of features in a top-down or bottom-up manner and generates a report.
* [Change Model](change_model): Modifies a model settings that don't requires retraining, such as enabling verbose mode for outliers or limiting memory batch size.
    - [How to Limit Memory Usage in Predict](change_model/How%20to%20limit%20memory%20usage%20in%20predict.md).
* [TestModelExternal](TestModelExternal.md): Compares repositories or samples by building a propensity model to identify differences.

## Examples of Simple Applications

To learn how to create your own applications, clone the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository. Navigate to the `MedProcessUtils` directory and explore the following examples:

* `learn` - Application.
* `getMatrix` - Application.
* `predict` - Application.
