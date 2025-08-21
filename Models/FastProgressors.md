
# FastProgressor

## Overview

This model is designed to screen patients after a creatinine test to identify those at risk of rapid eGFR decline. The definition of fast deterioration aligns with KDIGO guidelines:

- A yearly average drop of more than 5 points in eGFR
- The observation period is at least 18 months
- Excludes acute conditions (e.g., AKI)
- Excludes patients who begin SGLT2 drug treatment, as they are already being managed

This model is not the KFRE, which predicts ESRD (end-stage renal disease). Instead, it targets otherwise healthy patients to help slow, stop, or prevent kidney function decline earlier in the disease process.

The model was developed using the UK THIN (The Health Improvement Network) dataset and externally validated at a US site. However, there are no peer-reviewed publications due to competing interests.

## Model Inputs

Inputs are listed in the "/discovery" API, including signal names and required units.

## Intended Usage

Refer patients identified as high risk for rapid deterioration to the endocrinology track.

## List of Publications


## Contact Details for Usage

The model may be released as open source upon request.
please contact : alon (dot) medial at gmail (dot) com