
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
| [1561P Targeted screening methodologies to select high risk individuals: LungFlag performance in Estonia Lung Cancer Screening Pilot](https://www.annalsofoncology.org/article/S0923-7534(24)03142-9/fulltext) | Estonia | 2024 |
| [Validation of LungFlag™ Prediction Model Using Electronic Medical Records (EMR) On Taiwan Data](https://www.jto.org/article/S1556-0864(24)01541-7/fulltext) | National Taiwan University Hospital - Taiwan | 2024 |
| [Validation of LungFlag Lean machine-learning model to identify individuals with lung cancer using multinational data](https://ascopubs.org/doi/10.1200/JCO.2025.43.16_suppl.e13649) | KPSC - US, Geisinger - US, THIN - UK, additional site in US | 2025 |
| [Maximizing Lung Cancer Screening in High-Risk Population Leveraging ML-Developed Risk-Prediction Algorithms: Danish Retrospective Validation of LungFlag](https://pubmed.ncbi.nlm.nih.gov/40592640/) | Southern Denmark | 2025 | 

Validation on CPRD, Canada are in progress

## Contact Details for Usage

Roche Navify Algosuit - Details to be announced.