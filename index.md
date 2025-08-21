
# Wikimedial 

## Overview

This is an infrastructure developed by Medial EarlySign to streamline the creation of predictive models using EMR data for clinical applications. Existing tools often fall short for clinical use many Python libraries are not optimized for sparse time series analysis, leading to high memory consumption and, in some cases, performance that is 10–100 times slower than necessary.

## Quick Start Guide

Choose one of the following options to get started:

### Using a Prebuilt Model
Available models:

| Model Name |  Model description | Contact Details for Usage |
|------------|--------------------|-----------|
| [LGI/Colon-Flag](Models/ColonFlag.md) | Detects colon cancer using age, sex, and CBCs | [Roche](https://navify.roche.com/marketplace/products/algorithms/navify-algorithms-colonflag-by-medial-earlysign) | 
| [LungFlag](Models/LungFlag.md) | Detects lung cancer using age, sex, smoking infromation, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [GastroFlag](Models/GastroFlag.md) | Detects gastric cancer using age, sex, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [AAA](Models/AAA.md) | Predicts AAA events | Geisinger/TBD |
| [FluComplications](Models/FluComplications.md) | Predicts flu followed by complications such as pneumonia, hospitalization, or death | TBD |
| [Pred2D](Models/Pred2D.md) | Predicts progression from prediabetes to diabetes | TBD |
| [FastProgressors](Models/FastProgressors.md) | Predicts rapid decline in eGFR	 | TBD |
| [MortatlityCMS](Models/MortatlityCMS.md) | Predicts mortality using CMS claims data | TBD |
| [COPDCMS](Models/COPDCMS.md) | Predicts COPD hospitalization using CMS claims data | TBD |

Instructions for using an existing model can be found [here](Infrastructure%20Home%20Page/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-use-the-deployed-algomarker)


### Creating a new model

If you want to create a new model, please follow those steps:

1. Set up your environment: Compile and clone the necessary tools - See the: [Infrastructure Installation](Infrastructure%20Home%20Page/index.md#installations)
2. Create a data repository: Follow the [ETL guide](Repositories/Load%20new%20repository.md)
3. Define your cohort: Prepare a list of patient IDs, prediction times, and outcome. See [MedSamples](Infrastructure%20Home%20Page/MedProcessTools%20Library/MedSamples.md) for details on labeling.
4. Specify the model architecture in JSON. Refer to: [Model Json Format](Infrastructure%20Home%20Page/MedModel%20json%20format.md), [infrastucture explaination](Infrastructure%20Home%20Page/index.md) and examples (TODO: reference to full example) 
5. Run our tools - python or `Flow`, `Optimizer` to train the model
6. Apply and test the model using `Flow`

### Other Documentation Pages

* [Infrastructure Home Page](Infrastructure%20Home%20Page/index.md) - Information about the Infrastructure
    - [Howto use AlgoMarker](Infrastructure%20Home%20Page/AlgoMarkers/Howto%20Use%20AlgoMarker.md)
* [Repositories](Repositories/index.md) - Information on how to Load data into Data Repository
* [Medial Tools](Medial%20Tools/index.md) - A documentation of our tools used to create the models, test the models, etc.
* [Python](Python/index.md) - A documentation of python wrapper of our infrastructure
* [Research](Research/index.md) - A documentation of some research topics
* [New employee landing page](New%20employee%20landing%20page/index.md) - Other documentation
