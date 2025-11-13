# Test 16 - Sample Dates

## Purpose

Quickly summarize the distribution of sample dates in the test cohort. Useful to check temporal coverage and spot data collection gaps.

## Required Inputs

- `WORK_DIR`: working directory containing `${WORK_DIR}/Samples/3.test_cohort.samples`

## How to Run
```bash
./run.specific.sh 16
```
Or include in full run:
```bash
./run.sh
```

## What This Test Does

- Reads `${WORK_DIR}/Samples/3.test_cohort.samples` and extracts the sample date (the script converts sample `time` to a year/month integer by `int(time/100)`).
- Produces a count of samples per date and writes `${WORK_DIR}/samples_stats/by_date.tsv`.
- Generates an HTML plot `${WORK_DIR}/samples_stats/by_date.html` using `plot.py` and a local HTML template.

## Output Location

- `${WORK_DIR}/samples_stats/by_date.tsv`
- `${WORK_DIR}/samples_stats/by_date.html`

## How to Interpret Results

- Use the TSV to see the number of samples collected per month (or per date unit). Look for irregularities such as sudden drops or spikes indicating data collection problems or cohort selection artifacts.

## Troubleshooting

- Missing `${WORK_DIR}/Samples/3.test_cohort.samples`: ensure Test 03 ran successfully.
- `plot.py` failures: ensure the plot template `${WORK_DIR}/tmp/plotly_graph.html` exists or update the command to point to another template.

## Files to inspect

- `${WORK_DIR}/samples_stats/by_date.tsv`
- `${WORK_DIR}/samples_stats/by_date.html`
