# Test 01 - Load Outcome

## Purpose

Load outcome/register data into the working repository. This prepares the repository structure and signals needed by later tests (samples generation, model fitting and evaluation).

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where the repository and outputs will be written
- `FIRST_WORK_DIR`: Path to the reference / silent run (used for copying inputs when running the silent/external run)
- `OUTCOME_INPUT_FILES_PATH`: Path(s) or pattern to the raw outcome input files that `load_outcomes.py` expects

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 1
```

Or include as part of the full suite:

```bash
./run.sh
```

Check `${WORK_DIR}/rep` and `${WORK_DIR}/ETL` for the loaded repository and ETL artifacts.

## What This Test Does

- Runs the Python ETL loader to parse and import the provided outcome files.
- If the repository hasn't been marked as loaded (no `${WORK_DIR}/rep/loading_done`), or when `OVERRIDE` > 0, it makes `${WORK_DIR}/ETL/rep_configs/load_with_flow.sh` executable and runs it to build the repository files.
- Writes a simple marker file `${WORK_DIR}/rep/loading_done` to indicate successful load.

## Output Location

- Repository: `${WORK_DIR}/rep` (look for a `*.repository` directory)
- ETL and temporary files: `${WORK_DIR}/ETL`, `${WORK_DIR}/tmp`
- Load marker: `${WORK_DIR}/rep/loading_done`

## How to Interpret Results

- Verify `${WORK_DIR}/rep` contains the expected `*.repository` directory and related data files.
- Check `${WORK_DIR}/rep/loading_done` exists after a successful run.
- Inspect the stdout/stderr and any logs printed by `load_outcomes.py` and `load_with_flow.sh` for errors.

Make sure the ETL was done correction, same as in [Test 01 - Generate Repository](../External%20Silent%20Run/Test%2001%20-%20Generate%20Repository.md)

## Common failure modes and suggestions

- Missing input files or incorrect `OUTCOME_INPUT_FILES_PATH`:
    * Ensure input files exist and are in the format expected by `load_outcomes.py`.
- Missing helper scripts or broken ETL config in `${FIRST_WORK_DIR}/ETL`:
    * Confirm the ETL folder contains `rep_configs/load_with_flow.sh` and helper modules used by the Python loader.
- Python environment/package errors when running `load_outcomes.py`:
    * Ensure the required Python packages are installed in the environment.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/ETL` (copied ETL configs and scripts)
