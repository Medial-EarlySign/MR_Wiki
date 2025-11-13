# Test 18 - Analyze Messages

## Purpose

Summarize textual messages returned by the model runner (AlgoMarker) in the outputs. Useful to spot common error messages or unexpected status codes from the algorithm.

## Required Inputs

- `WORK_DIR`: working directory to place outputs
- `SILENCE_RUN_OUTPUT_FILES_PATH`: path to the silence-run output file produced by the algorithm, unless set to the special value `GENERATE` (in which case this test will skip)

## How to Run
```bash
./run.specific.sh 18
```
Or run with the full suite:
```bash
./run.sh
```

## What This Test Does

- If `SILENCE_RUN_OUTPUT_FILES_PATH` is not `GENERATE`, the script scans the provided TSV/CSV of algorithm outputs, counts occurrences of each message (uses the last column as the message), and computes the percentage of total outputs for each message.
- Outputs the sorted message counts to `${WORK_DIR}/outputs/messages.tsv`.
- If `SILENCE_RUN_OUTPUT_FILES_PATH` equals `GENERATE`, the test prints a message and skips processing.

## Output Location

- `${WORK_DIR}/outputs/messages.tsv` - columns: message, count, percent_of_total

## How to Interpret Results

- Use the TSV to identify the most frequent messages returned by the algorithm. Messages with high frequency may indicate systematic errors or common success markers (e.g., `<OK>`). Investigate rare but critical error messages.

## Troubleshooting

- If the script prints "No output files from AlgoMarker - skips", ensure `SILENCE_RUN_OUTPUT_FILES_PATH` is set to the path of the algorithm output file and not `GENERATE`.
- If parsing fails, inspect the input file for expected tab-separated columns and ensure the last column contains the message strings.

## Files to inspect

- `${WORK_DIR}/outputs/messages.tsv`
