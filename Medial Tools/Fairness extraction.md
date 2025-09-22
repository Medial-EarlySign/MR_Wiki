
# Fairness Extraction

To evaluate fairness, we compare Sensitivity and Specificity at specific score cutoffs across different groups. The required tool is available in the [SCRIPTS](https://github.com/Medial-EarlySign/MR_Scripts) repository, which should already be in your PATH for direct use.

## Process Overview

1. **Run bootstrap analysis** to generate detailed results, reporting performance at each 1% increment of positive rate (PR) and false positive rate (FPR).
2. **Define the base cohort** (`FAIRNESS_BASE_COHORT`) for baseline performance assessment.
3. **Specify comparison groups** (`FAIRNESS_GROUPS`) to stratify and compare within the base cohort.

## Example Usage

```bash
#!/bin/bash
FAIRNESS_BASE_COHORT="Age:40,89;Time-Window:90,365;Ex_or_Current_Smoker:0.5,1.5"
FAIRNESS_GROUPS=("Gender:1,1" "Gender:2,2")
OUTDIR=/tmp

# Prepare cohorts file
echo "MULTI;${FAIRNESS_BASE_COHORT}" | sed 's|;|\t|g' > ${OUTDIR}/cohorts
for fr_grp in "${FAIRNESS_GROUPS[@]}"; do
    echo "MULTI;${FAIRNESS_BASE_COHORT};${fr_grp}" | sed 's|;|\t|g' >> ${OUTDIR}/cohorts
done

PREDS_FILE=/nas1/Work/Users/Eitan/Lung/outputs/models2023/EX3/model_63/Test_Kit/bootstrap/TimeWindow.alt/result_win_90_365.preds
RATES_1_99="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99"

# Run bootstrap analysis
bootstrap_app --use_censor 0 --sample_per_pid 0 --input ${PREDS_FILE} --rep /nas1/Work/Repositories/KP/kp.repository  --json_model /nas1/Work/Users/Alon/LungCancer/configs/analysis/bootstrap/bootstrap.json --output ${OUTDIR}/bt.fairness.by_pr --cohorts_file ${OUTDIR}/cohorts --working_points_fpr ${RATES} --working_points_pr ${RATES}

# Analyze fairness at 3% and 5% positive rate cutoffs
fairness_extraction.py --bt_report ${OUTDIR}/bt.fairness.by_pr.pivot_txt --output ${OUTDIR} --bt_cohort "${FAIRNESS_BASE_COHORT}" --cutoffs_pr 3 5
```

## `fairness_extraction.py` Arguments

- `--bt_report`: Path to the bootstrap output file (should include results for multiple PR or FPR cutoffs and all comparison groups).
- `--bt_cohort`: The base cohort used for baseline filtering. If omitted, the script will use the shortest cohort description found in the bootstrap file.
- `--output`: Directory for output files.
- `--cutoffs_pr`: List of PR cutoffs to evaluate (if not available, FPR will be used), based on the baseline cohort.

The script above first runs the bootstrap analysis, then defines the base cohort and comparison groups (e.g., `Gender:1,1` and `Gender:2,2`).

## Output

The tool compares Sensitivity and Specificity for the specified `FAIRNESS_GROUPS` at the same cutoff (e.g., top 3% and 5% positive rate). It also performs a chi-square statistical test to assess differences between groups.