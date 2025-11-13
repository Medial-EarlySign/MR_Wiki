
# Test 01: Train Samples Over Years

## Purpose
Ensure that training samples are properly distributed across years and months, helping to detect data leakage, temporal bias, or sampling issues in model development.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `TRAIN_SAMPLES_BEFORE_MATCHING`: Path to the raw training samples

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 1
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Analyzes the distribution of cases and controls by year and by month
- Flags any unusual patterns, imbalances, or trends in the sample
- Creates a folder `samples_stats.train` with:
    - `stats.txt`: Table and histogram showing how many distinct outcomes each patient has in the samples (e.g., case/control status changes)
    - `cases_controls_id_histogram.html`: Histogram of how many times each patient appears as case/control in the samples

## Output Location
- Main log: `WORK_DIR/01.test_train_samples_over_years.log`
- Additional stats: `WORK_DIR/samples_stats.train/`

## How to Interpret Results
- Check for balanced distribution of cases/controls across years and months
- Review histograms for repeated patients and outcome changes
- Investigate any anomalies, such as unbalanced years or unexpected patient repeats
