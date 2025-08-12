# Bootstrap legend
The bootstrap result file is tab delimited file with 3 columns:
1. Cohort - The name of the "filter" used to select and defined the cohort which the results are reffered to. For example "All" - means no filters, "Males" - only males, "Age:45-80", etc.. The name is configured in bootstrap cohort configuration file (--cohort_file argument) that maps name of cohort to set of filter rules, as described under: [bootstrap_app](/Medial%20Tools/bootstrap_app)
2. Measurement - The name of the measurement. For example "AUC_Mean" - which is the mean value of the AUC measured in the bootstrap analysis process.The name is divided into 2 sections - The metric that was measured in each bootstrap experiment and the statistical calculation over this measure from all experiments. For each metric we extract the following statistical values which appears in the suffix:

- _Mean - mean value of the metric from all bootstrap experiments
- _Std - Standard Deviation of the metric from all bootstrap experiments
- _CI.Lower.95 - The lower confidence interval of the metric from all bootstrap experiments. lowest 2.5% percentile. 
- _CI.Upper.95 - The higher confidence interval of the metric from all bootstrap experiments. highest 2.5% percentile.
- _Obs - The observed metric value when there is no bootstrap randomization - the calculated metric on the all data where each record is taken exactly once
The metrics are sometimes simple as "AUC", "RMSE", but in some cases have more complicated names that can be divided into 2 parts by "@" delimeter. For example "SENS@FPR_10.000"- The first token is the measured metric and the second part is the cutoff defined by the second metric. The second metric can be "SCORE" to define cutoff by score, "FPR" to define cutoff by False Positive rate, "SENS" - by sensitivity and "PR" - positive rate.
- The First token can be one of the following: 
    - * SENS - Sensitivity/Recall/True Positive Rate (Y axis in the ROC curve)
    - * FPR - False Positive Rate (X axis in the ROC curve)
    - * PR - Positive Rate
    - * PPV - Positive Predictive Values / Precision
    - * SCORE - the score of the model
    - * LIFT - the lift
    - * OR - Odds Ratio
    - * RR - Relative Risk
    - * NPV - Negative Predictive Value
    - * SPEC = Specificity := 1 - FPR
Additional Measures: NNEG - number of negatives (controls in the cohort), NPOS - number of positive/cases in the cohort
3. Value - The numeric value that relates to the cohort and measurement
