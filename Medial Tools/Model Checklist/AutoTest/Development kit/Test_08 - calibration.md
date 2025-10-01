# Test_08 - calibration

## Purpose
This test evaluates the calibration performance of a predictive model. Calibration measures how well the predicted probabilities reflect actual outcomes, ensuring the model's probability estimates are reliable and actionable.

more about calibration information please refer to [Calibrate model, and calibration test](../../../Guide%20for%20common%20actions/Calibrate%20model,%20and%20calibration%20test.md)


## Required Inputs
From `configs/env.sh`:

- WORK_DIR - output work directory
- CALIBRATED_MODEL - path for calibrated model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES_CALIBRATION - test samples for calibration
- BT_JSON_CALIBRATION - json for bootstrap analysis
- BT_COHORT_CALIBRATION - bootstrap cohort definition to focus on calibration

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 8
```
Or include as part of the full suite:
```bash
./run.sh
```

## Explanation
This test assesses the calibration of the model using calibration curves and calibration metrices like calibration index, R2. It compares predicted probabilities to observed outcomes, typically by binning predictions and plotting the observed mean outcome against expected confidence intervals. Well-calibrated models produce probability estimates that closely match real-world results.

## Output
Results are saved in `${WORK_DIR}/calibration`

- `bt.pivot_txt `- Bootstrap results of calibration measurement
- *.html  - Calibration graph for each cohort; for each score bin, plots observed mean outcome, expected confidence interval, etc.
