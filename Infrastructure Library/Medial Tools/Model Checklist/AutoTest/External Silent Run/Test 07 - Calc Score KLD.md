# Test 07 - Calculate Score Kullback–Leibler Divergence (KLD)

## Purpose

Compute the Kullback–Leibler Divergence (KLD) between the reference score distribution and the new test run score distribution. This quantifies how different the two score histograms are and provides related summary metrics used for quick drift detection.

## Required Inputs
From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: Working directory where `compare/score_dist.tsv` and other compare artifacts are stored
- The test depends on Test 06 (score distributions) and expects `${WORK_DIR}/compare/score_dist.tsv` to exist

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 7
```
Or include as part of the full suite:
```bash
./run.sh
```

Check `${WORK_DIR}/compare` for the printed KLD summary and related outputs created by Test 06.

## What This Test Does

Based on `07.calc_score_kld.py`:

- Reads `${WORK_DIR}/compare/score_dist.tsv` which contains binned score percentages for `Reference` and `Test_Run`
- Converts the two distributions into aligned probability vectors
- Calls an internal helper `calc_kld` to compute:
    - Number of bins
    - KLD between reference and test distributions
    - KLD to a uniform distribution (KLD_to_Uniform)
    - entropy_p (a summary entropy-based metric)
- Prints a short one-line summary recommending to review `${WORK_DIR}` for details

## Output Location

- `${WORK_DIR}/compare/score_dist.tsv` - input to this test (binned distributions)
- Script prints a summary line to stdout; check the test log `${WORK_DIR}/07.calc_score_kld.log` (or the general test runner log) for the KLD output

## How to Interpret Results

- KLD is a non-symmetric measure of how one distribution diverges from another. Higher KLD indicates greater difference.
- `KLD_to_Uniform` gives a sense of how concentrated the distribution is relative to uniform; very small values mean the distribution is close to uniform. The score distribution is not suppose to be uniform, but it gives you a sense of what is a "high" KLD value. 
- `entropy_p` is an entropy-derived metric used as an auxiliary indicator.

Practical guidance:

- Small KLD (close to zero) indicates little distributional change in scores.
- Large KLD (order of magnitude larger than typical baselines for your model) should trigger deeper inspection (compare score histograms and top contributing factors such as age or missing signals).

## Example output snippet

Example printed line from the script:

```text
KLD (20)= 0.005790, KLD_to_Uniform=0.740022, entory_p=4.105875
```

This indicates the computation used 20 bins and returned the three summary metrics.

## Notes and Implementation Details

- The script uses a small epsilon (1e-4) to avoid log-of-zero issues when computing KLD.
- It relies on the helper function `calc_kld` from the project's `lib.PY_Helper` module which handles bin alignment and normalization.
- If `score_dist.tsv` is missing or malformed, the script will fail - ensure Test 06 produced valid binned distributions first.

## Troubleshooting

- If you get a file-not-found error for `score_dist.tsv`, re-run Test 06 and confirm the file exists and has `Test`, `score`, and `Percentage` columns.
- If KLD values are extremely large, inspect the two histograms (`score_dist.html` from Test 06) to see which score bins differ and whether one distribution contains zero mass for bins present in the other. Consider re-binning or smoothing if needed.

## Test Results Review

Primary items to inspect after running this test:

- `${WORK_DIR}/compare/score_dist.tsv`
- `${WORK_DIR}/compare/score_dist.html`
- The test runner log containing the printed KLD summary (e.g., `${WORK_DIR}/07.calc_score_kld.log`)