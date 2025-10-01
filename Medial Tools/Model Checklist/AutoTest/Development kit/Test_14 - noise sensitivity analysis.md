
# Test 14: Noise Sensitivity Analysis

## Purpose
Evaluate model robustness by testing sensitivity to different types of input noise, including missing values, date shifts, and value perturbations. This helps ensure the model remains stable under real-world data conditions.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples
- `TRAIN_SAMPLES_BEFORE_MATCHING`: Path to the training samples
- `BT_JSON`: Bootstrap JSON for cohort filtering
- `BT_COHORT`: Bootstrap cohort definition
- `NOISER_JSON`: Path to noiser JSON config
- `TIME_NOISES`, `VAL_NOISES`, `DROP_NOISES`: Parameters to control the noise levels

## Depends On
- [Test 06: Bootstrap Results](Test_06%20-%20bootstrap%20results.md)

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 14
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Applies controlled noise to input data using settings from `NOISER_JSON`, `TIME_NOISES`, `VAL_NOISES`, and `DROP_NOISES`
- Measures the impact of each type of noise on model predictions and performance
- Assesses model stability and identifies potential resolution problems

## Output Location
- `$WORK_DIR/test_noiser/results/`
	- `time_analysis.csv`: Effect of time noise on model performance at different levels
	- `value_analysis.csv`: Effect of value noise on model performance at different levels
	- `drop_analysis.csv`: Effect of dropping tests/values on model performance at different drop levels

## How to Interpret Results
- Review CSV files to see how model metrics change as noise increases
- Use findings to improve model robustness and data preprocessing
