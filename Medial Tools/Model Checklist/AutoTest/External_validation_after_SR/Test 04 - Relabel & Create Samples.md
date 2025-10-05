# Test 04 - Relabel & Create Samples

## Purpose

Relabel an input samples file with outcome labels derived from the repository's diagnosis registry, produce a cleaned cohort file and filter samples to the requested comparison cohort. This prepares evaluation-ready sample files for downstream bootstrap and comparison tests.

> Note: This test is distinct from [Test 03 - Create Samples](../External%20Silent%20Run/Test%2003%20-%20Create%20Samples.md) from `External Slient Run` kit which generates a samples cohort from raw inputs or an external file. `Test 04` assumes a sample cohort has already been created (from `Test 03`) and focuses on relabeling and filtering by outcome codes.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where outputs will be written
- `FIRST_WORK_DIR`: Path to the reference run (contains Silent Run Samples and model outputs)
- `BT_JSON`: Path to bootstrap features JSON, default used from `${FIRST_WORK_DIR}/json/bootstrap/bt_features.json`
- `COMPARE_COHORT`: Cohort identifier used by `FilterSamples` to select a subset of samples
- `CODE_LIST_FILE`: File listing diagnosis codes to use (e.g., ICD lists)
- `CODE_DIR`: Directory containing code lists
- `SUB_CODES`: Comma-separated list of sub-cohort identifiers

## How to Run

From your TestKit folder, execute:

```bash
./run.specific.sh 4
```

Or include as part of the full suite:

```bash
./run.sh
```

Primary output files will be placed under `${WORK_DIR}/Samples` and `${WORK_DIR}/outputs`.

## What This Test Does

- Creates an outcome registry with `create_registry.py` (if missing or `OVERRIDE` > 0):
    - `python ${CURR_PT}/resources/lib/create_registry.py --rep $REP_PATH --signal DIAGNOSIS --output ${WORK_DIR}/Samples/outcome.reg --end_of_data 20230101 --codes_dir ${CODE_DIR} --codes_list ${CODE_LIST_FILE} --sub_codes ${SUB_CODES}`
- Relabels samples using `relabel.py` (writes dropped samples too):
    - `python ${CURR_PT}/resources/lib/relabel.py --registry ${WORK_DIR}/Samples/outcome.reg --samples ${FIRST_WORK_DIR}/Samples/3.test_cohort.samples --output ${OUTPUT} --output_dropout ${WORK_DIR}/Samples/dropped.samples --follow_up_controls 730 --time_window_case_maximal_before 730 --time_window_case_minimal_before 0 --future_cases_as_control 0 --sub_codes ${SUB_CODES}`
- Runs `samples_by_year.sh` to show distribution by year and month.
- Computes sample statistics with `samples_stats.py`.
- Produces a cleaned sample file and runs `FilterSamples` to generate `${WORK_DIR}/Samples/3.test_cohort.samples` filtered by `COMPARE_COHORT` and the bootstrap JSON (`BT_JSON`).
- Runs `samples_by_year.sh` again on the final cohort file.

## Output Location

- Relabeled samples: `${WORK_DIR}/Samples/relabeled.samples`
- Filtered test cohort: `${WORK_DIR}/Samples/3.test_cohort.samples`
- Dropped samples: `${WORK_DIR}/Samples/dropped.samples` with exclusion reason.
- Clean intermediate file: `${WORK_DIR}/Samples/clean.samples`
- Statistics: `${WORK_DIR}/samples_stats` (path passed to `samples_stats.py`)

## How to Interpret Results

- Inspect `${WORK_DIR}/Samples/relabeled.samples` to confirm samples are labeled with outcome columns and have expected counts.
- Check `${WORK_DIR}/Samples/dropped.samples` to see why samples were excluded.
- Verify `${WORK_DIR}/Samples/3.test_cohort.samples` exists and matches expected cohort selection.
- Review `${WORK_DIR}/model/04.create_samples.log` for other info and statistics

## Common failure modes and suggestions

- Missing or incorrect code lists (`CODE_LIST_FILE` / `CODE_DIR`):
    * Ensure code files (ICD lists, etc.) are present and the `create_registry.py` arguments point to the correct directory.
- Input sample file missing or malformed:
    * The test expects `${FIRST_WORK_DIR}/Samples/3.test_cohort.samples` or the configured `SILENCE_RUN_OUTPUT_FILES_PATH` outputs.
- `FilterSamples` utility missing or not on PATH:
    * Ensure the `FilterSamples` executable is available in PATH 

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/Samples/relabeled.samples`
- `${WORK_DIR}/Samples/3.test_cohort.samples`
- `${WORK_DIR}/Samples/dropped.samples`

