# Test 12 - Lab Frequency

## Purpose

Analyze lab frequency for signals that back the model's important features. The test produces counts of how many patients had N observations of a given signal (per-signal histogram of patient-level lab counts).

## Required Inputs
From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: working directory where repository and output folders live
- `CMP_FEATURE_RES`: comma-separated list of important features (used to derive the list of relevant signals)
- A prepared repository under `${WORK_DIR}/rep`, containing `test.signals` and `test.repository`

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 12
```
Or include as part of the full suite:
```bash
./run.sh
```

After run, check `${WORK_DIR}/signals_cnt/` for per-signal TSV results.

## What This Test Does

- Parses `CMP_FEATURE_RES` to extract signal names. It strips category prefixes like `ICD9_CODE:`/`ICD10_CODE:`/`ATC_CODE:` and excludes some control features (e.g., `FTR_`, `Age`, `category_`, `Smoking`). It also ensures `DIAGNOSIS` and `Smoking_Status` signals are included by default.
- For each signal it verifies the signal exists in `${WORK_DIR}/rep/test.signals` and skips signals not present.
- For present signals it runs:
	- `Flow --rep ${WORK_DIR}/rep/test.repository --pids_sigs --sigs <signal>` to retrieve patient-signal rows (id, date, ...)
	- An awk pipeline deduplicates per-patient-date entries and counts how many distinct dates each patient has for the signal, then aggregates across patients to produce counts: how many patients had exactly 1 sample, 2 samples, ...
- Writes per-signal files: `${WORK_DIR}/signals_cnt/<signal>.tsv` with rows: signal, count, num_patients

## Output Location

- `${WORK_DIR}/signals_cnt/` - one TSV per signal named `<signal>.tsv` containing columns: signal, num_labs, num_patients

## How to Interpret Results

- Each per-signal TSV shows how many patients had N lab entries for that signal during the observation window. Compare these distributions across signals or against a reference dataset to find differences in monitoring intensity.
- Without a reference, raw counts indicate whether certain signals are rarely or frequently measured in this dataset (useful for data quality and expected feature availability).

## Troubleshooting

- Missing `test.signals` or `test.repository`: the script checks for the signal list in `${WORK_DIR}/rep/test.signals` and will skip signals not found. Ensure the repo was created by Test 03 and contains expected files.
- `Flow` not found or failing: ensure `Flow` is on PATH.
- Empty output files: if `${WORK_DIR}/rep/test.signals` lists the signal but Flow returns no rows, inspect the repository content to ensure the signal has records (search for the exact signal token in `test.signals`).

## Example output

A sample `${WORK_DIR}/signals_cnt/Hemoglobin.tsv` might look like:

```text
Hemoglobin	1	10234
Hemoglobin	2	4230
Hemoglobin	3	1231
Hemoglobin	4	512
```

## Notes and Implementation Details

- The script deduplicates by patient-date so multiple entries on the same day count as a single lab for that day.
- The signal extraction logic excludes some features (e.g., `Age`, features starting with `FTR_` or `category_`) because they are not time-series signals.

## Test Results Review

Primary files to inspect after running this test:

- `${WORK_DIR}/signals_cnt/` (per-signal TSVs)
