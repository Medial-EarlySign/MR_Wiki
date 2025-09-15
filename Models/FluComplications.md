# FluComplications

## Overview
This model was developed using data from Kaiser Permanente Northwest. Its primary goal is to identify unvaccinated patients who would most benefit from receiving a flu shot by predicting those at higher risk for influenza or influenza-like illness followed within three months by a complication. Complications may include pneumonia (the most common), hospitalization, or death.

The model is especially sensitive to severe complications such as hospitalization and death, but also performs well in predicting all types of complications. In the related publication, we also analyzed the additional complications observed after flu compared to patients who did not contract the flu. Since the model's risk factors often identify frail patients who may experience complications regardless of flu, we specifically examined the "additional" complications following influenza.

The model was compared to a linear model based on the World Health Organization (WHO) list of approximately 10 risk factors (e.g., asthma, immunosuppression, pregnancy, age, etc.). Our model outperforms the WHO-based model and also incorporates hospitalization/admission history, medications, and other diagnosis codes. Some variants included blood and spirometry tests, but these were ultimately excluded from the final public model for simplicity, as they are less common or less impactful.

The model assumes good vaccine efficacy. While ideally the model would target "who will benefit most from a flu shot," this is difficult to determine due to varying vaccine efficacy from year to year. Instead, the model focuses on predicting who is likely to get sick and experience complications, highlighting those for whom vaccination would be especially important.

## Model Inputs

Inputs are listed in the "/discovery" API, including signal names and required units.

## Deployments

- MHS (Maccabi Health Services), 2019
- Kaiser Permanente Northwest, 2019
- Geisinger, 2019 and 2021–2025

## Intended Usage

The model is intended to increase flu shot adherence among populations at higher risk for flu complications.

## Publications

*Partial list:*

| Manuscript | Population | Year |
|------------|------------|------|
| [Prediction of Influenza Complications: Development and Validation of a Machine Learning Prediction Model to Improve and Expand the Identification of Vaccine-Hesitant Patients at Risk of Severe Influenza Complications](https://pubmed.ncbi.nlm.nih.gov/35893436/) | Geisinger - US | 2022 |

## Contact Details for Usage

please contact : alon (dot) medial at gmail (dot) com for more details