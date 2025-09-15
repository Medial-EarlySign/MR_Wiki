
# LGI/Colon-Flag

## Overview

The LGI/Colon-Flag model was developed to detect colon and rectal cancer using data from Maccabi Healthcare Services (MHS), the second largest HMO in Israel. First version published in 2015, with the final version completed in 2018.

The model has undergone external validation at numerous sites across various regions. A partial list of related publications is provided [below](#list-of-publications).

This model is effective at detecting gastric cancer, although our specialized [GastroFlag](GastroFlag.md) model offers superior performance in this area. It also performs well in identifying lower gastrointestinal (GI) disorders and pre-cancerous conditions.

## Model Inputs

The model uses the following signals:

* Birth year (for age calculation)
* Sex
* CBC panel: Hemoglobin, Hematocrit, RBC, MCH, MCV, MCHC, Platelets, RDW, WBC, MPV, Lymphocytes (absolute and %), Monocytes (absolute and %), Eosinophils (absolute and %), Basophils (absolute and %), Neutrophils (absolute and %)

## Deployments

- Maccabi Healthcare Services - Israel (since 2015)
- Geisinger Health System - US (since 2018)
- List of more sites...

> **Note:** partial list - there are more deployments

## Intended Usage

- **Not for screening exclusion:** This tool is not intended to rule out patients from screening. Its sensitivity is insufficient for use as a primary screening tool.
- **Purpose:** The model is designed to help increase compliance and improve the yield of colonoscopies among patients who are non-adherent to screening recommendations.
- **Professional use only:** The tool is intended for interpretation and use by healthcare professionals, not patients.

The model is designed to calculate a score when new CBC data is available. Requests to calculate a score without CBC data will be rejected. A score can still be generated even if some other input signals are missing.

For further information, please see the "Contact Details for Usage" section and request the User Guide.

## List of Publications

* Partial list of publications.

| Manuscript | Population | Year | Model | Study Type | Research Organization |
| ---------- | ---------- | ---- | ----- | ---------- | --------------------- |
| [Development and validation of a predictive model for detection of colorectal cancer in primary care by analysis of complete blood counts: a binational retrospective study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4997037/) | MHS Israel, THIN - UK | 2016 | Old ColonFlag | Retrospective, Outcomes were retrieved after scoring + External validation | MES |
| [Performance analysis of a machine learning flagging system used to identify a group of individuals at a high risk for colorectal cancer](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0171759) | MHS Israel | 2017 | Old ColonFlag | Prospective Observational | MES |
| [Evaluation of a prediction model for colorectal cancer: retrospective analysis of 2.5 million patient records](https://pmc.ncbi.nlm.nih.gov/articles/PMC5633543/) | UK - CPRD | 2017 | Old ColonFlag | Retrospective, External Validation | Oxford |
| [Early Colorectal Cancer Detected by Machine Learning Model Using Gender, Age, and Complete Blood Count Data](https://link.springer.com/article/10.1007/s10620-017-4722-8) | US - Kaiser Permanente North West | 2017 | ColonFlag ??? | Retrospective, External Validation | MES |
|[Computer-Assisted Flagging of Individuals at High Risk of Colorectal Cancer in a Large Health Maintenance Organization Using the ColonFlag Test](https://ascopubs.org/doi/full/10.1200/CCI.17.00130)| MHS Israel | 2018 | Old ColonFlag | Prospective Interventional | MHS |
| [Prediction of findings at screening colonoscopy using a machine learning algorithm based on complete blood counts (ColonFlag)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0207848) | Canada | 2018 | ColonFlag | Retrospective, External Validation | MES |
| [Potential roles of artificial intelligence learning and faecal immunochemical testing for prioritisation of colonoscopy in anaemia](https://onlinelibrary.wiley.com/doi/10.1111/bjh.15776) | UK - gastroenterology clinic in Plymouth, Royal London Hospital | 2019 | ColonFlag | Prospective Observational | Barts | 
| [Validation of an Algorithm to Identify Patients at Risk for Colorectal Cancer Based on Laboratory Test and Demographic Data in Diverse, Community-Based Population](https://www.sciencedirect.com/science/article/pii/S1542356520305991) | US - Kaiser Permanente North West | 2020 | ColonFlag | Retrospective, External Validation | University of Washington + KP |
| [Collaboration to Improve Colorectal Cancer Screening Using Machine Learning](https://catalyst.nejm.org/doi/full/10.1056/CAT.21.0170) | US - Geisinger Health System | 2022 | ColonFlag | Prospective Interventional | Geisinger |
| [Diagnostic application of the ColonFlag AI tool in combination with faecal immunochemical test in patients on an urgent lower gastrointestinal cancer pathway](https://bmjopengastro.bmj.com/content/11/1/e001372) | UK - Barts Health - Urgency pathway | 2024 | ColonFlag | Prospective Interventional | Barts |
| [Machine Learning-Guided Cancer Screening: The Benefits of Proactive Care](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4959547) | Geisinger | 2024 | ColonFlag | Prospective Interventional | Geisinger |


Less important publication:

| Manuscript | Population | Year | Model | Study Type | Research Organization | Comment |
| ---------- | ---------- | ---- | ----- | ---------- | --------------------- | ------- |
| [Use of ColonFlag score for prioritisation of endoscopy in colorectal cancer](https://pmc.ncbi.nlm.nih.gov/articles/PMC8183282/) | UK - Barts Health - Urgency pathway | 2021 | ColonFlag | Prospective Interventional | Barts | There is a new publication from 2024 with more data |
| [Predicting the presence of colon cancer in members of a health maintenance organisation by evaluating analytes from standard laboratory records](https://pmc.ncbi.nlm.nih.gov/articles/PMC5379154/) | MHS Israel | 2017 | ColonFlag variations with all labs | Retrospective | MES | Different model |
| [Development and Validation of a Colorectal Cancer Prediction Model: A Nationwide Cohort-Based Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11258054/) | Clalit - Israel | 2024 | Clalit Model | Retrospective, Developent and internal validation | Clalit | Not our model and no comparison to ColonFlag |


## Contact Details for Usage

Roche Navify Algosuit - Details to be announced.