# Available Models

The **Models** section describes predictive models developed and deployed using the Medial Research Framework. These models are designed to identify patients at elevated risk for a range of clinical outcomes, supporting earlier interventions and improved healthcare decision-making.

Each model in this repository is built on standardized EMR data processed through the Medial Infrastructure - ensuring reproducibility, scalability, and compliance across diverse healthcare systems. The framework supports modular data pipelines, feature generation, and evaluation workflows, enabling seamless deployment of models across sites.

Most models presented here have been validated across multiple real-world datasets and healthcare partners.

## What You’ll Find Here

* **Model Overviews** - Brief summaries describing the clinical motivation, prediction targets, and input features.
* **Evidence** - List of publication, deployments
* **Implementation Details** - Intended usage and contact details

Each model page provides both conceptual and technical details, helping users understand why it was developed and in which contexts it performs best.

| Model Name |  Model description | Contact Details for Usage |
|------------|--------------------|-----------|
| [LGI/Colon-Flag](ColonFlag.md) | Detects colon cancer using age, sex, and CBCs | [Roche](https://navify.roche.com/marketplace/products/algorithms/navify-algorithms-colonflag-by-medial-earlysign) | 
| [LungFlag](LungFlag.md) | Detects lung cancer using age, sex, smoking information, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [GastroFlag](GastroFlag.md) | Detects gastric cancer using age, sex, and common blood tests | [Roche](https://navifyportal.roche.com/us/en-us/about) |
| [AAA](AAA.md) | Predicts AAA events | Geisinger/TBD |
| [FluComplications](FluComplications.md) | Predicts flu followed by complications such as pneumonia, hospitalization, or death | TBD |
| [Pred2D](Pred2D.md) | Predicts progression from prediabetes to diabetes | Planned to be open source |
| [FastProgressors](FastProgressors.md) | Predicts rapid decline in eGFR	 | Planned to be open source |
| [Mortality](MortalityCMS.md) | Predicts mortality using CMS claims data | TBD |
| [Unplanned COPD Admission Prediction Model](COPDCMS.md) | Predicts COPD hospitalization using CMS claims data | TBD |

Instructions for using an existing model can be found [here](../Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-use-the-deployed-algomarker)