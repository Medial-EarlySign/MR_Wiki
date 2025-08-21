# GastroFlag

## Overview

The GastroFlag model was created to identify gastric cancer using data from Maccabi Healthcare Services (MHS), Israel’s second largest HMO.

This model is effective not only in detecting colon and rectal cancer but also performs well in recognizing lower gastrointestinal (GI) disorders and pre-cancerous conditions.

The finalized model has been validated across eight different sites:

* THIN (UK dataset)
* Japan
* Taiwan
* United States
* Latvia
* Korea (2 sites)
* MHS

A publication may be available in the future.

## Model Inputs

Inputs are listed in the "/discovery" API, including signal names and required units.

* Birth year (for age calculation)
* Sex
* CBC panel: Hemoglobin, Hematocrit, RBC, MCH, MCV, MCHC, Platelets, RDW, WBC, MPV, Lymphocytes (absolute and %), Monocytes (absolute and %), Eosinophils (absolute and %), Basophils (absolute and %), Neutrophils (absolute and %)
* Iron panel: Ferritin, Iron_Fe
* Basic Metabolic Panel (BMP): Glucose, Sodium, Creatinine, Urea, Potassium
* Comprehensive Metabolic Panel (CMP) additions: Albumin, Protein_Total, ALT, AST, ALKP, Bilirubin


## Intended Usage

- **Not for screening exclusion:** This tool is not intended to rule out patients from screening. Its sensitivity is insufficient for use as a primary screening tool.
- **Purpose:** The model is designed to help increase compliance and improve the yield of colonoscopies among patients who are non-adherent to screening recommendations.
- **Professional use only:** The tool is intended for interpretation and use by healthcare professionals, not patients.

The model is designed to calculate a score when new CBC data is available. Requests to calculate a score without CBC data will be rejected. A score can still be generated even if some other input signals are missing.

For further information, please see the "Contact Details for Usage" section and request the User Guide.

## List of Publications


## Contact Details for Usage

Roche Navify Algosuit - Details to be announced.