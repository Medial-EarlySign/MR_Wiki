
# LGI/Colon-Flag

## Overview

The LGI/Colon-Flag model was developed to detect colon and rectal cancer using data from Maccabi Healthcare Services (MHS), the second largest HMO in Israel. First version published in 2015, with the final version completed in 2018. The model is currently deployed in:

The model has undergone external validation at numerous sites across various regions. A partial list of related publications is provided [below](#list-of-publications).

This model is effective at detecting gastric cancer, although our specialized [GastroFlag](GastroFlag.md) model offers superior performance in this area. It also performs well in identifying lower gastrointestinal (GI) disorders and pre-cancerous conditions.

## Model Inputs

The model uses the following signals:

* Birth year (for age calculation)
* Sex
* CBC panel: Hemoglobin, Hematocrit, RBC, MCH, MCV, MCHC, Platelets, RDW, WBC, MPV, Lymphocytes (absolute and %), Monocytes (absolute and %), Eosinophils (absolute and %), Basophils (absolute and %), Neutrophils (absolute and %)

## Deployments

* partial list - there are more deployments

- Maccabi Healthcare Services (since 2015)
- Geisinger Health System (since 2018)

## Intended Usage

- **Not for screening exclusion:** This tool is not intended to rule out patients from screening. Its sensitivity is insufficient for use as a primary screening tool.
- **Purpose:** The model is designed to help increase compliance and improve the yield of colonoscopies among patients who are non-adherent to screening recommendations.
- **Professional use only:** The tool is intended for interpretation and use by healthcare professionals, not patients.

The model is designed to calculate a score when new CBC data is available. Requests to calculate a score without CBC data will be rejected. A score can still be generated even if some other input signals are missing.

For further information, please see the "Contact Details for Usage" section and request the User Guide.

## List of Publications

* Partial list of publications.

| Manuscript | Population | Year| 
|------------|------------|-----|
| [Development and validation of a predictive model for detection of colorectal cancer in primary care by analysis of complete blood counts: a binational retrospective study](https://pubmed.ncbi.nlm.nih.gov/26911814/) | MHS Israel, THIN - UK | 2016 |
| [Evaluation of a prediction model for colorectal cancer: retrospective analysis of 2.5 million patient records](https://pubmed.ncbi.nlm.nih.gov/28941187/) | UK - CPRD | 2017 |
| [Early Colorectal Cancer Detected by Machine Learning Model Using Gender, Age, and Complete Blood Count Data](https://link.springer.com/article/10.1007/s10620-017-4722-8) | US - Kaiser Permanente North West | 2017 |
|[Computer-Assisted Flagging of Individuals at High Risk of Colorectal Cancer in a Large Health Maintenance Organization Using the ColonFlag Test](https://ascopubs.org/doi/full/10.1200/CCI.17.00130)| MHS Israel, prospective use | 2018 |
| [Prediction of findings at screening colonoscopy using a machine learning algorithm based on complete blood counts (ColonFlag)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0207848) | Canada | 2018 |
| [Validation of an Algorithm to Identify Patients at Risk for Colorectal Cancer Based on Laboratory Test and Demographic Data in Diverse, Community-Based Population](https://pubmed.ncbi.nlm.nih.gov/32360824/) | US - Kaiser Permanente North West | 2020 |
| [Collaboration to Improve Colorectal Cancer Screening Using Machine Learning](https://catalyst.nejm.org/doi/full/10.1056/CAT.21.0170) | US - Geisinger Health System | 2022 |
| [Diagnostic application of the ColonFlag AI tool in combination with faecal immunochemical test in patients on an urgent lower gastrointestinal cancer pathway](https://bmjopengastro.bmj.com/content/11/1/e001372) | UK | 2024


## Contact Details for Usage

Roche Navify Algosuit - Details to be announced.