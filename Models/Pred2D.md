
# Pre2D

## Overview

Pre2D is a predictive model developed using data from THIN (The Health Improvement Network) in the UK. Its purpose is to identify patients in the pre-diabetes stage who are likely to develop diabetes within the next two years.

The criteria for defining diabetes are as follows:

- Two consecutive fasting glucose tests above 125 mg/dL
- HbA1C above 6.5
- A single glucose measurement above 200 mg/dL
- A diabetes diagnosis code with at least one abnormal test (glucose or HbA1C)
- Evidence of treatment with any glucose-lowering agent other than metformin

## Model Inputs

The model utilizes the following input signals:

- Birth year (used to calculate age)
- Sex
- Measurements: BMI
- Diabetes screening: Glucose, HbA1C
- Lipid panel: Triglycerides, HDL
- WBC
- ALT
- Prescriptions (optional): NDC, RX NORM, which may be converted to ATC codes in the future

## Intended Usage

For the user guide, please contact the author.

## Publications

Partial list of publications:

| Manuscript | Population | Year |
|------------|------------|------|
| [Prediction of progression from pre-diabetes to diabetes: Development and validation of a machine learning model](https://pubmed.ncbi.nlm.nih.gov/31943669/) | THIN - UK, MHS - Israel, AppleTree - Canada | 2020 |

## Contact Information

The model may be released as open source upon request.
For inquiries, please contact: alon (dot) medial at gmail (dot) com