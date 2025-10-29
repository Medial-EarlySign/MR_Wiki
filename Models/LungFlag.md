
# LungFlag

## Overview

The LungFlag model was developed at Kaiser Permanente Southern California (KPSC) to identify all types of lung cancer, including Squamous, Adenocarcinoma, Small Cell, and Non-Small Cell variants.

It has been validated at approximately 10 different sites.

## Model Inputs

Inputs are listed in the `/discovery` API, including signal names and required units.

* Birth year (for age calculation)
* Sex
* Measurements: BMI, Weight, Height
* Smoking Information: Smoking Status (mandatory), Smoking duration (years), smoking intensity (ciggarets per day), Pack years, Smoking quit date (if applicable)
* Diagnosis signal: ICD10/ICD9
* Spirometry test: Fev1
* CBC panel: Hemoglobin, Hematocrit, RBC, MCH, MCV, MCHC, Platelets, RDW, WBC, Lymphocytes (absolute and %), Monocytes (absolute and %), Eosinophils (absolute and %), Basophils (absolute and %), Neutrophils (absolute and %)
* Lipid panel: Cholesterol, Triglycerides, LDL, HDL, NonHDLCholesterol
* Basic Metabolic Panel (BMP): Glucose, Creatinine, Urea
* Comprehensive Metabolic Panel (CMP) additions: Albumin, Protein_Total, ALT, ALKP

## Deployments

- Geisinger Health System (since 2022)

## Intended Usage

For further information, please see the "Contact Details for Usage" section and request the User Guide.

## List of Publications

* Partial list of publications.

| Manuscript | Population | Year| 
|------------|------------|-----|
| [Machine Learning for Early Lung Cancer Identification Using Routine Clinical and Laboratory Data](https://pubmed.ncbi.nlm.nih.gov/33823116/) | KPSC - US | 2021 |
| [Flagging High-Risk Individuals with a ML Model Improves NSCLC Early Detection in a USPSTF-Eligible Population](https://doi.org/10.1016/j.jtho.2022.09.029) | KPSC - US | 2023 |
| [Improved Efficiency with Lungflag vs Opportunistic Selection in a Theoretical East Asian Lung Cancer Screening Program](https://doi.org/10.1016/j.jtho.2023.09.860) | Budget impact | 2023 |
| [Use of the predictive risk model LungFlagTM for lung cancer screening in screening in a Spanish reference center: A cost-effectiveness analysis](https://doi.org/10.1016/j.annonc.2023.09.2691) | Spain - Budget Impact | 2023 |
| [LungFlag, a machine-learning (ML) personalized tool for assessing lung cancer risk in a community setting, to evaluate performance in flagging non-small cell lung cancer (NSCLC) regardless of sex or race](https://www.asco.org/abstracts-presentations/ABSTRACT412750) | KPSC - US | 2023 |
| [1561P Targeted screening methodologies to select high risk individuals: LungFlag performance in Estonia Lung Cancer Screening Pilot](https://www.annalsofoncology.org/article/S0923-7534(24)03142-9/fulltext) | Estonia | 2024 |
| [Validation of LungFlag™ Prediction Model Using Electronic Medical Records (EMR) On Taiwan Data](https://www.jto.org/article/S1556-0864(24)01541-7/fulltext) | National Taiwan University Hospital - Taiwan | 2024 |
| [Artificial intelligence–aided lung cancer screening in routine clinical practice: A pilot of LungFlag at Geisinger](https://doi.org/10.1200/JCO.2024.42.16_suppl.e13604) | Geisinger - US | 2024 |
| [Budget impact model of LungFlag, a predictive risk model for lung cancer screening](https://doi.org/10.1200/JCO.2024.42.16_suppl.10534) | US - Budget Impact | 2024 |
| [Validation of LungFlag Lean machine-learning model to identify individuals with lung cancer using multinational data](https://ascopubs.org/doi/10.1200/JCO.2025.43.16_suppl.e13649) | KPSC - US, Geisinger - US, THIN - UK, additional site in US | 2025 |
| [Cost-effectiveness of a machine learning risk prediction model (LungFlag) in the selection of high-risk individuals for non-small cell lung cancer screening in Spain](https://doi.org/10.1080/13696998.2024.2444781) | Spain - Budget Impact | 2025 |
| [Maximizing Lung Cancer Screening in High-Risk Population Leveraging ML-Developed Risk-Prediction Algorithms: Danish Retrospective Validation of LungFlag](https://pubmed.ncbi.nlm.nih.gov/40592640/) | Southern Denmark | 2025 | 

### Posters

| Poster | Population | Year| 
|------------|------------|-----|
| [Flagging high-risk individuals with a ML model improves NSCLC early detection in a USPSTF-eligible population](../SharePoint_Documents/LungFlag/Posters/20220827%20NA%20IASLC%20Final%20Poster.pdf) | KPSC - US | 2022 |
| [Computer-assisted Flagging of Never Smokers at High Risk of NSCLC in a Large US-based HMO using the LungFlag Model](../SharePoint_Documents/LungFlag/Posters/20220913%20IASLC%20AP%20Final%20Poster.pdf) | KPSC - US | 2022 |
| [Cost-effectiveness of a machine learning risk prediction model (LungFlag ) in the selection of high-risk individuals for non-small cell lung cancer screening in Spain](../SharePoint_Documents/LungFlag/Posters/ISPOREurope23_Heuser_EE74_POSTER.pdf) | Budget impact | 2023 |
| [Internal Poster - Real-World Evidence as the centerpiece for the evaluation of LungFlag pre-screening digital algorithm](../SharePoint_Documents/LungFlag/Posters/2023%20RWD%20Forum%20LungFlag%20poster.pdf) | Budget Impact | 2023 |
| [LungFlag, a Machine-Learning (ML) Personalized Tool for Assessing Pulmonary Complications a Community Setting, Demonstrates Comparable Performance in Flagging Non-Small Cell Lung Cancer (NSCLC) Regardless of Sex or Race](../SharePoint_Documents/LungFlag/Posters/20230510%20ASCO%20Final%20Poster.pdf) | KPSC - US | 2023 |
| [Improved Efficiency with LungFlag vs. Opportunistic Selection in a Theoretical East Asian Lung Cancer Screening Program](../SharePoint_Documents/LungFlag/Posters/20230831%20WCLC%20Final%20Poster.pdf) | Budget Impact | 2023 |
| [Use of the predictive risk model LungFlag for lung cancer screening in a Spanish reference center: A cost-effectiveness analysis](../SharePoint_Documents/LungFlag/Posters/20231019%20ESMO%20Póster.pdf) | Budget Impact | 2023 |
| [Artificial intelligence–aided lung cancer screening in routine clinical practice: A pilot of LungFlag at Geisinger](../SharePoint_Documents/LungFlag/Posters/ASCO2024%20Artificial%20intelligence–aided%20lung%20cancer%20screening%20in%20routine%20clinical%20practice%20A%20pilot%20of%20LungFlag%20at%20Geisinger.pdf) | Geisinger - US | 2024 |
| [Budget impact model of LungFlag, a predictive risk model for lung cancer screening](../SharePoint_Documents/LungFlag/Posters/ASCO2024%20Budget%20Impact%20Model%20of%20LungFlagTM,%20a%20Predictive%20Risk%20Model%20for%20Lung%20Cancer%20Screening.jpg) | Budget Impact | 2024 |
| [Validation of LungFlag™ Prediction Model Using Electronic Medical Records (EMR) On Taiwan Data](../SharePoint_Documents/LungFlag/Posters/20240909%20WCLC%20Final%20Poster.pdf) | National Taiwan University Hospital - Taiwan | 2024 |
| [TARGETED SCREENING METHODOLOGIES TO SELECT HIGH RISK INDIVIDUALS: LUNGFLAG™ PERFORMANCE IN ESTONIAN LUNG CANCER SCREENING PILOT](../SharePoint_Documents/LungFlag/Posters/20240910%20ESMO%20Poster%20Estonia.pdf) | Estonia | 2024 |
| [LungFlag Risk Prediction Validation on Canadian Ever Smokers Pre-Classified as High Risk for Lung Cancer](../SharePoint_Documents/LungFlag/Posters/WCLC2025-Poster-Lungflag%20FINAL%20Final.pdf) | Canada | 2025 |


### On Going Studies

* Validation on CPRD
* Validation on 4 datasets

## Contact Details for Usage

Roche Navify Algosuit - Details to be announced.