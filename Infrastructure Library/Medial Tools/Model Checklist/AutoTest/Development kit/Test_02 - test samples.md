
# Test 02: Test Samples

## Purpose
Analyze the distribution and integrity of test samples, similar to [Test 01](Test_01%20-%20test_train_samples_over_years.md), but focused on the evaluation set. This helps ensure the test data is representative and free from temporal or sampling bias.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `TEST_SAMPLES`: Path to the test samples

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 2
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Checks the distribution of cases/controls in the test samples by year and month
- Flags any unusual patterns, imbalances, or trends
- Creates a folder `samples_stats.test` with summary statistics and HTML plots

## Output Location
- Main log: `WORK_DIR/02.test_test_samples_over_years.log`
- Additional stats and plots: `WORK_DIR/samples_stats.test/`

## How to Interpret Results
- Review distributions for balance and representativeness
- Use plots and tables to spot anomalies or unexpected patterns
