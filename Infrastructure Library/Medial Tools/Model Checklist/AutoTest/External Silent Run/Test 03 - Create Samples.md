# Test 03 - Create Samples

## Purpose

Generate sample cohorts from the prepared repository or from an external samples file. These samples are used by subsequent tests for scoring and evaluation.

## Required Inputs
From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working folder where the repository and Samples outputs will be written
- `SILENCE_RUN_OUTPUT_FILES_PATH`: Either the special value `GENERATE` (to generate samples from the repository) or a path to an input TSV/CSV file containing sample definitions
- `TAKE_JUST_LAST`: Applicable when `SILENCE_RUN_OUTPUT_FILES_PATH` is `GENERATE`. If set to `1` will filter and take only most recent Hemoglobin lab test date as candidate for the analysis, otherwise will use all Hemoglobin dates for the analysis.
- `FILTER_LAST_DATE`: The reference matrix contains multiple dates for each patient. If provided `1` will filter and take only most recent date for each patient. Might be better analsys if that's what we are doing in the client/in this dataset.

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 3
```
Or include as part of the full suite:
```bash
./run.sh
```

Check `${WORK_DIR}/Samples` for produced sample files.

## What This Test Does

Behavior depends on `SILENCE_RUN_OUTPUT_FILES_PATH`:

- If `SILENCE_RUN_OUTPUT_FILES_PATH` is `GENERATE`:
    - Reads the repository located under `${WORK_DIR}/rep` (looks for `*.repository`)
    - Generates a samples file at `${WORK_DIR}/Samples/3.test_cohort.samples`
    - Two generation modes exist (controlled by `TAKE_JUST_LAST` in the script):
        * If `TAKE_JUST_LAST` > 0: for each patient take only the last Hemoglobin record
        * Otherwise: take all Hemoglobin records for each patient
    - Copies the generated file to `${WORK_DIR}/Samples/1.all_potential.samples`
- If `SILENCE_RUN_OUTPUT_FILES_PATH` is a path to an existing file:
    - The script converts the input file into the internal `SAMPLE` format, transforming dates from `DD-MMM-YYYY`-style strings into integer yyyymmdd timestamps and sorting samples.
    - Produces `${WORK_DIR}/Samples/test.bf.samples` and `${WORK_DIR}/Samples/test.bf.orig.preds` (original predictions preserved)
    - If `${WORK_DIR}/ETL/FinalSignals/ID2NR` exists, the script remaps identifiers and writes `${WORK_DIR}/Samples/3.test_cohort.samples` and `${WORK_DIR}/Samples/test.orig.preds`. Otherwise it symlinks the generated files.

- The script also prepares `${WORK_DIR}/ref_matrix` either by symlinking `REFERENCE_MATRIX` or by filtering it to the last date when `FILTER_LAST_DATE` > 0.
- Finally it runs `samples_by_year.sh` on the generated cohort file to produce year-based summaries.

## Output Location

- Main cohort samples: `${WORK_DIR}/Samples/3.test_cohort.samples`
- All potential samples (copy): `${WORK_DIR}/Samples/1.all_potential.samples`
- Intermediate samples: `${WORK_DIR}/Samples/test.bf.samples`
- Original predictions file: `${WORK_DIR}/Samples/test.bf.orig.preds` and/or `${WORK_DIR}/Samples/test.orig.preds`
- Reference matrix (symlink or filtered): `${WORK_DIR}/ref_matrix`

## How to Interpret Results

- Verify all generated files are non empty with just headers.
- Verify there are no errors and the execution finished successfully.

### Common failure modes and suggestions

- Input file formatting errors:
    * If the external file isn't the expected format (columns in different order or different date format), the awk parsing and date conversion will produce incorrect times. Confirm column positions and pre-normalize the file if needed.
- Missing repository or incorrect `*.repository` file:
    * If generation mode is selected but the repository isn't present or contains unexpected schema, the process will fail

## Example output snippets

1) Generated sample header and a sample line:

```text
EVENT_FIELDS	id	time	outcome	outcomeTime	split
SAMPLE	12345	20230115	0	20990101	-1
```

2) When `ID2NR` mapping is used, final lines preserve the remapped ID as the second column.

## Notes and Implementation Details

- The script uses several small utilities and conventions from the TestKit (`Flow`, `paste.pl`, `samples_by_year.sh`). Ensure these helper scripts are available on PATH or in `configs/env.sh`

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/Samples/3.test_cohort.samples`
- `${WORK_DIR}/Samples/test.bf.samples`
- `${WORK_DIR}/Samples/test.orig.preds` (when present)
- `${WORK_DIR}/ref_matrix`

