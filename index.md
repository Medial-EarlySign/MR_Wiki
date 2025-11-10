
# Wikimedial 

## Overview

This is an infrastructure developed by Medial EarlySign to streamline the creation of predictive models using EMR data for clinical applications. Existing tools often fall short for clinical use many Python libraries are not optimized for sparse time series analysis, leading to high memory consumption and, in some cases, performance that is 10-100 times slower than necessary.

Medial Infrastructure is designed to turn the Electronic Medical Record (EMR)-a complex, semi-structured time-series dataset, into a machine-learning-ready resource. Unlike images or free text, EMR data can be stored in countless formats, and its "labels" (the outcomes or targets you want to predict) aren’t always obvious. We address this by standardizing both the storage and the processing of time-series signals. We can think about this infrastructure as "TensorFlow" of medical data machine learning.

This award-winning framework used in production across multiple sites and recognized in the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge) offers an end-to-end solution for high-stakes medical AI.

## What is this?
An infrastrucutre library with tools and extention in python to access the library. 
The library has internal data format repository for storing the EMR in efficeint format for fast and low memory access. 
We used this infrastructure to process millions of patients with dozens of signals with low memory footprint of 10-20GB of RAM, VS pandas that loading a single diagnosis signal resulted in out of memory on 256GB RAM machine. 
The Infrastrucutre is build upon:

* Data Repository Layer - [MedRepository](Infrastructure%20C%20Library/00.InfraMed%20Library%20page)
* MedModel - A pipeline for a full machine learning model to handle data from MedRepository or json input files of EMR to generate prediction/explainability output. It has the ability to train a new model or use an existing one
* Tools to evaluate MedModel performance using bootstrap analysis, fairness, explainability results. A script for testing utilizing most of those evaluations is accessible in [AutoTest](Medial%20Tools/Model%20Checklist/AutoTest)

## Using a Prebuilt Model
Available models:

| Model Name |  Model description | Contact Details for Usage |
|------------|--------------------|-----------|
| [LGI/Colon-Flag](Models/ColonFlag.md) | Detects colon cancer using age, sex, and CBCs | [Roche](https://navify.roche.com/marketplace/products/algorithms/navify-algorithms-colonflag-by-medial-earlysign) | 
| [LungFlag](Models/LungFlag.md) | Detects lung cancer using age, sex, smoking infromation, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [GastroFlag](Models/GastroFlag.md) | Detects gastric cancer using age, sex, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [AAA](Models/AAA.md) | Predicts AAA events | Geisinger/TBD |
| [FluComplications](Models/FluComplications.md) | Predicts flu followed by complications such as pneumonia, hospitalization, or death | TBD |
| [Pred2D](Models/Pred2D.md) | Predicts progression from prediabetes to diabetes | Planned to be open source |
| [FastProgressors](Models/FastProgressors.md) | Predicts rapid decline in eGFR	 | Planned to be open source |
| [MortatlityCMS](Models/MortatlityCMS.md) | Predicts mortality using CMS claims data | TBD |
| [Unplanned COPD Admission Prediction Model](Models/COPDCMS.md) | Predicts COPD hospitalization using CMS claims data | TBD |

There are two options for using a model:

* The model is already depolyed and you just want to access it. What is the API? - please refer [How To Use Deployed AlgoMarker](Infrastructure%20C%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-use-the-deployed-algomarker)
* The model is available for download, but you need to deploy it first. Please refer to [AlgoMarker Deployment](Infrastructure%20C%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-deploy-algomarker)


## Creating a new model

If you want to create a new model, please follow those steps:

1. Set up your environment: Compile and clone the necessary tools
    * Follow: [Infrastructure Installation](Installation/index.md#setup)
2. Create a data repository: Follow the [ETL guide](Repositories/Load%20new%20repository.md)
3. Define your cohort: Prepare a list of patient IDs, prediction times, and outcome. See [MedSamples](Infrastructure%20C%20Library/MedProcessTools%20Library/MedSamples.md) for details on labeling. In this step you will create a file where each patient has a timestamp for prediction and a label in a CSV format. 
4. Specify the model architecture in JSON. Refer to: [Model Json Format](Infrastructure%20C%20Library/MedModel%20json%20format.md), [infrastucture explaination](Infrastructure%20C%20Library/index.md) 
5. Run our tools to train the model with the model architecture, samples and data repository - python or [Flow](Medial%20Tools/Using%20the%20Flow%20App/index.md#training-a-model), [Optimizer](Medial%20Tools/Optimizer.md) to train the model, or [python code](Python/Examples.md#learn-model-from-json-to-generate-matrix)
6. Apply and test the model using [Flow](Medial%20Tools/Using%20the%20Flow%20App/index.md#predictingapplying-a-model) or [python code](Python/Examples.md#load-medmodel-and-apply-predict-on-sample)
7. Analyze model performance using [bootstrap](Medial%20Tools/bootstrap_app/) and [test kit/AutoTest](Medial%20Tools/Model%20Checklist/AutoTest/) or write your own tests
8. Wrap the model for deployment - follow - [AlgoMarker Deployment](Infrastructure%20C%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md)

## Other Documentation Pages

* [Infrastructure Home Page](Infrastructure%20C%20Library/index.md) - Information about the Infrastructure
    - [Howto use AlgoMarker](Infrastructure%20C%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md)
* [Repositories](Repositories/index.md) - Information on how to Load data into Data Repository
* [Medial Tools](Medial%20Tools/index.md) - A documentation of our tools used to create the models, test the models, etc.
* [Python](Python/index.md) - A documentation of python wrapper of our infrastructure
* [Research](Research/index.md) - A documentation of some research topics
* [Installation](Installation/index.md) - Other documentation
* [MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs) - Github page to Medial EarlySign infrastructure libraries
* [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) - Github page to Medial EarlySign tools that uses MR_LIBS
* [MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts) - Github page to Medial EarlySign complementry scripts and tools

