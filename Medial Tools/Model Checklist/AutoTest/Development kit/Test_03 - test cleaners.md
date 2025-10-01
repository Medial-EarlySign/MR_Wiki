
# Test 03: Cleaners

## Purpose
Verify that all input signals have appropriate data cleaning rules applied before model training and testing. This ensures data quality and consistency throughout the pipeline.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 3
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Checks that every input signal has a defined cleaner rule
- Flags any signals missing cleaner definitions
- Fails the test if any required cleaner is missing

## Output Location
- Main log: `WORK_DIR/03.test_cleaners.log` (lists signals missing cleaners)

## How to Interpret Results
- If the log lists missing cleaners, update your configuration to define them
- The test passes only if all signals have cleaner rules
