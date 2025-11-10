
# Home

## Medial EarlySign Documentation - Overview

This is an infrastructure developed by Medial EarlySign to streamline the creation of predictive models using EMR data for clinical applications. Existing tools often fall short for clinical use. Many Python libraries are not optimized for sparse time series analysis, leading to **high memory consumption** and, in some cases, performance that is **10-100 times slower** than possible. We used this infrastructure to process millions of patients with dozens of signals with low memory footprint of 10-20GB of RAM, VS pandas, where loading a single diagnosis signal resulted in out of memory on 256GB RAM machine. 

Medial Infrastructure is designed to turn the Electronic Medical Record (EMR)-a complex, semi-structured time-series dataset, into a **machine-learning-ready** resource. Unlike images or free text, EMR data can be stored in countless formats, and its "labels" (the outcomes or targets you want to predict) aren’t always obvious. We address this by standardizing both the storage and the processing of time-series signals. We can think about this infrastructure as "**TensorFlow**" of medical data machine learning.

This is an infrastructure library provided with tools and a Python extension library to access the library. 

This **award-winning framework** used in production across multiple sites and recognized in the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge) offers an end-to-end solution for high-stakes medical AI.


### Core Components
The library has internal data format repository for storing the EMR in efficient format for fast and low memory access. 
The infrastructure is built upon:

* **Data Repository Layer** - [MedRepository](Infrastructure%20Library/00.InfraMed%20Library%20page)
* **MedModel** - A pipeline for a full machine learning model to handle data from MedRepository or json input files of EMR to generate prediction/explainability output. It has the ability to train a new model or use an existing one
* **Tools** to evaluate MedModel performance using bootstrap analysis, fairness, explainability results. A script for testing utilizing most of those evaluations is accessible in [AutoTest](Medial%20Tools/Model%20Checklist/AutoTest). Reference to [Tools Page](Medial%20Tools)

## Why use this?
* **Fast and efficient** library to process EMRs and common methods are implemented. Processing time series might be less efficient for vector libraries like pandas/polars and a specific library with efficient algorithm is a better fit
* Avoid reinventing common methodologies each project. Some logic is complicated and rewriting them/testing them will take a lot of time and effort.
* Maintain shareable, versioned, pipelines 
* Provides built-in safeguards to help mitigate common data leakage and overfitting pitfalls common in time-series EMR data.
* Production ready - can be easily deployed in a docker image, native server with minimal dependencies. Can be also deployed in distro-less linux docker image

## Getting started
* You want to use an existing model
    - The model is deployed already? - [How To Use Deployed AlgoMarker](Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-use-the-deployed-algomarker)
    - The model is available, but you need to deploy it first. Please refer to [AlgoMarker Deployment](Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-deploy-algomarker)
    - List of [Models](Models)
* You want to build a new model please follow [Creating a new model](#creating-a-new-model)


## Creating a new model

If you want to create a new model, please follow those steps:

1. Set up your environment: Compile and clone the necessary tools
    * Follow: [Installation](Installation/index.md#setup)
2. Create a data repository with your EMR data: Follow the [ETL guide](Infrastructure%20Library/DataRepository/Load%20new%20repository.md)
3. Define your cohort: Prepare a list of patient IDs, prediction times, and outcome. See [MedSamples](Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md) for details on labeling. In this step you will create a file where each patient has a timestamp for prediction and a label in a CSV format. 
4. Specify the model architecture in JSON. Refer to: [Model Json Format](Infrastructure%20Library/MedModel%20json%20format.md), [infrastucture explanation](Infrastructure%20Library/index.md) 
5. Run our tools to train the model with the model architecture, samples and data repository - python or [Flow](Medial%20Tools/Using%20the%20Flow%20App/index.md#training-a-model), [Optimizer](Medial%20Tools/Optimizer.md) to train the model, or [python code](Medial%20Tools/Python/Examples.md#learn-model-from-json-to-generate-matrix)
6. Apply and test the model using [Flow](Medial%20Tools/Using%20the%20Flow%20App/index.md#predictingapplying-a-model) or [python code](Medial%20Tools/Python/Examples.md#load-medmodel-and-apply-predict-on-sample)
7. Analyze model performance using [bootstrap](Medial%20Tools/bootstrap_app/) and [test kit/AutoTest](Medial%20Tools/Model%20Checklist/AutoTest/) or write your own tests
8. Wrap the model for deployment - follow - [AlgoMarker Deployment](Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md)

## Github pages

* [MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs) - Github repository for Medial EarlySign infrastructure libraries
* [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) - Github repository for Medial EarlySign tools that uses MR_LIBS
* [MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts) - Github repository for Medial EarlySign complementary scripts and tools
