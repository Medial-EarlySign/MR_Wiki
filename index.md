
# Wikimedial 

## Overview

This is an infrastructure developed by Medial EarlySign to streamline the creation of predictive models using EMR data for clinical applications. Existing tools often fall short for clinical use many Python libraries are not optimized for sparse time series analysis, leading to high memory consumption and, in some cases, performance that is 10–100 times slower than necessary.

## Using a Prebuilt Model
Available models:

| Model Name |  Model description | Contact Details for Usage |
|------------|--------------------|-----------|
| [LGI/Colon-Flag](Models/ColonFlag.md) | Detects colon cancer using age, sex, and CBCs | [Roche](https://navify.roche.com/marketplace/products/algorithms/navify-algorithms-colonflag-by-medial-earlysign) | 
| [LungFlag](Models/LungFlag.md) | Detects lung cancer using age, sex, smoking infromation, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [GastroFlag](Models/GastroFlag.md) | Detects gastric cancer using age, sex, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [AAA](Models/AAA.md) | Predicts AAA events | Geisinger/TBD |
| [FluComplications](Models/FluComplications.md) | Predicts flu followed by complications such as pneumonia, hospitalization, or death | TBD |
| [Pred2D](Models/Pred2D.md) | Predicts progression from prediabetes to diabetes | Planned to be open sources |
| [FastProgressors](Models/FastProgressors.md) | Predicts rapid decline in eGFR	 | Planned to be open sources |
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
5. Run our tools to train the model with the model architecture, samples and data repository - python or [Flow](Medial%20Tools/Guide%20for%20common%20actions#2-train-a-model-from-json), [Optimizer](Medial%20Tools/Optimizer.md) to train the model, or [python code](Python/Medial's%20C++%20API%20in%20Python/Examples.md#learn-model-from-json-to-generate-matrix)
6. Apply and test the model using [Flow](Medial%20Tools/Guide%20for%20common%20actions#3-calculate-model-score-on-samples) or [python code](Python/Medial's%20C++%20API%20in%20Python/Examples.md#load-medmodel-and-apply-predict-on-sample)
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
