# Fairness extraction
In order to test fairness we need to compare Sensitivity, Specificity at specific score cutoff among different groups and compare those values.
We have tool in SCRIPTS git repository, so it is already part of the PATH and we can use it directly.
 
Example usage:
```bash
#!/bin/bash
FAIRNESS_BASE_COHORT="Age:40,89;Time-Window:90,365;Ex_or_Current_Smoker:0.5,1.5"
FAIRNESS_GROUPS=("Gender:1,1" "Gender:2,2")
OUTDIR=/tmp
echo "MULTI;${FAIRNESS_BASE_COHORT}" | sed 's|;|\t|g' > ${OUTDIR}/cohorts
for fr_grp in "${FAIRNESS_GROUPS[@]}"; do
    echo "MULTI;${FAIRNESS_BASE_COHORT};${fr_grp}" | sed 's|;|\t|g' >> ${OUTDIR}/cohorts
done
PREDS_FILE=/nas1/Work/Users/Eitan/Lung/outputs/models2023/EX3/model_63/Test_Kit/bootstrap/TimeWindow.alt/result_win_90_365.preds
bootstrap_app --use_censor 0 --sample_per_pid 0 --input ${PREDS_FILE} --rep /nas1/Work/Repositories/KP/kp.repository  --json_model /nas1/Work/Users/Alon/LungCancer/configs/analysis/bootstrap/bootstrap.json --output ${OUTDIR}/bt.fairness.by_pr --cohorts_file ${OUTDIR}/cohorts --working_points_fpr 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99 --working_points_pr 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99
fairness_extraction.py --bt_report ${OUTDIR}/bt.fairness.by_pr.pivot_txt --output ${OUTDIR} --bt_cohort "${FAIRNESS_BASE_COHORT}" --cutoffs_pr 3 5
```
 
fairness_extraction.py inputs:

- bt_report - accepts bootstrap output file (that we run with many PR or FPR cutoffs and on cohorts with the groups we want to compare)
- bt_cohort - the basic bootstrap cohort we used to filter/select as baseline, on top of that we will filter the "groups" to compare. If not given will extract from the bootstrap file the shortest cohort description and will use this.
- output - directory where we will output files:
- cutoffs_pr - and array of cutoffs to inspect based on PR if exists or FPR if not, based on the baseline cohort.
The code before the script calls the bootstrap and we also define the "BASE_COHORT" group and the groups to compare "Gender:1,1" and "Gender:2,2"
