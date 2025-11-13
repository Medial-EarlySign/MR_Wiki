
# Test 04: Imputers

## Purpose
Ensure that all input signals to the model have defined imputation rules, so missing data is handled consistently and robustly.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 4
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Checks that every signal input to the model has an imputer defined
- Flags any signals missing imputation rules
- Fails the test if any required imputer is missing

## Output Location
- Main log: `WORK_DIR/04.test_imputers.log` (lists signals missing imputers)

## How to Interpret Results
- If the log lists missing imputers, update your configuration to define them
- The test passes only if all signals have imputation rules

@@@[PLEASE_COMPLETE]: Add troubleshooting tips and example log output
