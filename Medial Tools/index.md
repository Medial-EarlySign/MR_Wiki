# Medial Tools

The Medial tools are list of executables based on the infrastrucutre to perform some actions and access the infrastrucutre API.

## What is this
Tutorial for usage with the infrastrucutre on an existing EMR dataset. Creating, testing, evaluating models with the infrastrucutre. 

This guide is different intended usage from deployment models.
When model is deployed using AlgoMarker, we are using a minimal API of the AlgoMarker to access the model outputs. For example no need for access for the train API of the infrasturcutre, so only a minimal sahred library is exposed for runtime.
There is also no need to generate a data repository for training testing on a large dataset. The API accepts JSONs with the EMR information for each patient. For more information on AlgoMarker deployments, please refere to [AlgoMarker](../Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md)

## Setup Requirements

1. I want to use the python library that uses teh infrastructure - [Python extension](Python). Please keep in mind that the python library does not fully exposes all the infrastracture APIs. We had also build in the past some tools/executables prior of having this python extension. Must of them can be rewritten with our python extension, but we haven't done this. Follow [python setup](../Installation/Python%20API%20for%20MES%20Infrastructure.md)
2. Application/Executables that uses the infrastructure - please refere to [installation guide](../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md). Documentation for each tool exists in this wiki and each tool has `--help` to list all his arguments with description.
3. I want to write my own applications using the infrastructure. Here are some [simple application examples](#examples-of-simple-applications)
    
Most of the time it will be sufficient to use python and some applications and there will be no need to write your own c++ code. For each use case I will describe all options.

## Tutorial

### Step 1 - Creating a Data Repository

The first step is to create a database/data repository with the data in MES infrastracture format.
In order to do that, please follow our [ETL guide](../Infrastructure%20Library/DataRepository/ETL%20Tutorial)

Please note that you will require to use `Flow` application in order to do the actual loading - [Flow loading](Using%20the%20Flow%20App/index.md#creating-repositories). Currently haven't ported the loading API code into python. It means you will need to install MES Tools.

### Step 2 - Accessing the Data Repository

There are 2 main options for accessing the raw data of the repository:

1. Using python API
    * Fetch signals as pandas DataFrame - [Load Signals in python](Python/Examples.md#load-some-signals)
2. Using Tools
    * Use Flow to output signal data/statistics - [Flow view signals](Using%20the%20Flow%20App/index.md#printing-pids-and-signals)
    * Use [Repository viewers](../Infrastructure%20Library/DataRepository/Repository%20Viewers.md) UI to fetch a specific patient and view it's data

### Step 3 - Creating a MedSamples

The next step it to create a TSV(Tab separated values) file called [MedSamples](../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md).
This file defines the ground truth outcome for each patient in each time point.

It is recommended to use the python API when applicable to generate the samples files, but in some cases we wrote C++ application to generate the sample file/s.
This file marks for each patient identifier a requested prediction time and an outcome `0` - control, healthy individual in that time point and `1` - a positive case of the medical condition we target for classification.
The outcome can also be numberic for regression.  There are other fields in the file for future processing's and filtering when applicable.

Suggested steps:

1. Generate all potential "samples" candidates of patient id and date for prediction without labeling them
2. Label and exlcude ineligibile "samples" and document the exclusion reason for cohort diagram and validation

Example code to create "samples" for all patients in the data repository within a specific date `20251011`
```python
import med
rep = med.PidRepository()

rep.read_all("/path/to/repository", [], ["BDATE"])
bdate_sig = rep.get_sig("BDATE").rename(columns = {"pid":"id"}) #All patients has BDATE signal and it is unique for each patient

bdate_sig["EVENT_FIELDS"] = "SAMPLE" # A dummy field, part for the MedSamples format. A legacy
bdate_sig["time"] = 20251011 # The requested prediction date for each patient. The infrastrucutre will constrain and remove future information beyond that date when doing inference.
bdate_sig["outcome"] = 0 # Currently no labeling, we will mark all as 0
bdate_sig["split"] = -1 # Mark of split information of that patient. Currently not using it and putting all patients at split -1
bdate_sig["outcomeTime"] = 20500101 # Marks the event date. When the target event happened. This will be used for filtering based on time windows analysis. For now, I'm just setting a valid date and in the labeling process, I might want to set this correctly if I want to do sub analysis by time windows

#Ordering the fields in the right order and removing unused fields
bdate_sig = bdate_sig[["EVENT_FIELDS", "id", "time", "outcome", "outcomeTime", "split"]]

bdate_sig.to_csv("/path/to/samples", index=False, sep="\t") # This is TAB separated
```


> [!NOTE] 
> Keep in mind that in most cases we process the training samples differently from test samples.
> The most common use case is to match and rebalance the incidence rate of the outcome over the years in the train, to avoid model learning the underlying year of the requested prediction. Those filtering/subsamping steps are being done in training to control for potential biases and information leakage and are highly important.
> This is up to the data science research to build an appropriate training samples and there is no magic/automatic solution for that.

### Training a Model

1. Create a model instruction/architecture file in [MedModel JSON](../Infrastructure%20Library/MedModel%20json%20format.md) format. This JSON file will configure the components in the [model pipeline](../Infrastructure%20Library) as described in the Infrastructure page.  
2. Train The model
    * Using python - [Train Model Using Python API](Python/Examples.md#learn-model-from-json-to-generate-matrix)
    * Using MES Tools
        - [Train using Flow](Using%20the%20Flow%20App/index.md#training-a-model) - Simplest, but without any Hyper parameters tuning
        - [Optimizer](Optimizer.md) - Training a model using grid search hyper parameter tuning. Uses build in penality for generalization error and gap between training/testing performance. Optuna is a better tools and can be easily adjust to do the same with more options, but currently that's what we have.

### Applying a Model
I have a model and I want to output scores from it or generate the feature matrix.
Since a model is a full pipeline to process the raw time series EMR, we can also access the feature matrix of the model.

* [Apply a model Using python](Python/Examples.md#load-medmodel-and-apply-predict-on-sample)
* [Apply a Model using Flow](Using%20the%20Flow%20App/index.md#predictingapplying-a-model)

### Model Evaluation
There are many many options to evalute the model results. 
You can see list of suggested test for model development - [Model Checklist](Model%20Checklist/).
You can also use external tools, but here is a brief intoduction to common and helpfull tools we used:

1. [bootstrap_app](bootstrap_app) - Analyze Model performance using bootstrap analysis to assess the confidence interval of the performace. Supports assessing model performance in multiple cohorts, sub population within a very simple query language. For example, we might want to test performance in different time window, age range, etc.
2. Model Feature importance - you can use [Flow](../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md)
3. [Adding Explainability](../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md#adding-an-explainer-to-an-existing-model) - as a post processor and additional output it is usefull to use our own explainability based on Shapley values, suited for medical data. This is described in the patent [US20240161005A1](https://patents.google.com/patent/US20240161005A1). The vanilla shapley values doesn't work well in medical data with many features and correlations, so we have developed an extenstion for that. It was tested based on ourt clinicians in a blinded validation of multiple explainability methods and it was also used in the [CMS Health AI outcome Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge), as we were award winners.
3. Estimating expected performance in different environments with covariance shift - [Simulator](Simulator.md)
4. [AutoTest](Model%20Checklist/AutoTest) - A pipeline of many tests, based on Model Checklist. It is divided into 3 main scenarions: Model development, Validation on external dataset without access to outcome, a complementry tests for external validation when we also have access to outcomes.



### Other Tools

* [Adding Calibration to a model and testing it](Calibrate%20model,%20and%20calibration%20test.md)
* [Fairness Extraction](Fairness%20extraction.md): Calculates fairness metrics.
- [Adjust Model](adjust_model.md): Adds components like rep_processors or post_processors to an existing model. Some components may require training with MedSamples and a repository. Usefull for example, if we want to test noising of the input, droping values and doing some manipulations that we don't want to store in the model.
* [Model Signals Importance](model_signals_importance.md): Evaluates the importance of signals in an existing model and measures the impact of including or excluding them on performance.
- [Iterative Feature Selector](Iterative%20Feature%20Selector.md): Iteratively selects features or groups of features in a top-down or bottom-up manner and generates a report.
- [Change Model](change_model): Modifies a model without retraining, such as enabling verbose mode for outliers or limiting memory batch size.
    - [How to Limit Memory Usage in Predict](change_model/How%20to%20limit%20memory%20usage%20in%20predict.md).
- [TestModelExternal](TestModelExternal.md): Compares repositories or samples by building a propensity model to identify differences.

## Examples of Simple Applications

To learn how to create your own applications, clone the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository. Navigate to the `MedProcessUtils` directory and explore the following examples:

* `learn` - Application.
* `getMatrix` - Application.
* `predict` - Application.
