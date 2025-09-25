
# Bootstrap Result File: Column Legend

The bootstrap result file is a tab-delimited file with three columns:

1. **Cohort**
     - The name of the filter used to define the cohort for which the results are reported. Examples: `All` (no filters), `Males` (only males), `Age:45-80`, etc.
     - Cohort names are set in the bootstrap cohort configuration file (see the `--cohort_file` argument), which maps each cohort name to a set of filter rules. For more details, see: [bootstrap_app](../bootstrap_app).

2. **Measurement**
     - The name of the measured metric. For example, `AUC_Mean` is the mean value of the AUC metric across bootstrap runs.
     - Measurement names have two parts: the metric measured in each bootstrap experiment, and the statistical summary calculated over all experiments. The suffix indicates the summary statistic:
         - `_Mean`: Mean value across all bootstrap experiments
         - `_Std`: Standard deviation across all bootstrap experiments
         - `_CI.Lower.95`: Lower 95% confidence interval (2.5th percentile)
         - `_CI.Upper.95`: Upper 95% confidence interval (97.5th percentile)
         - `_Obs`: Observed value (calculated on the full data, without bootstrap randomization)
     - Metrics can be simple (e.g., `AUC`, `RMSE`) or compound, separated by `@`. For example, `SENS@FPR_10.000` means Sensitivity at a False Positive Rate cutoff of 10.000. The second part after `@` can be:
         - `SCORE`: Cutoff by score
         - `FPR`: Cutoff by False Positive Rate
         - `SENS`: Cutoff by Sensitivity
         - `PR`: Cutoff by Positive Rate
     - The first token (metric) can be:
         - `SENS`: Sensitivity / Recall / True Positive Rate (Y-axis in ROC)
         - `FPR`: False Positive Rate (X-axis in ROC)
         - `PR`: Positive Rate
         - `PPV`: Positive Predictive Value / Precision
         - `SCORE`: Model score
         - `LIFT`: Lift
         - `OR`: Odds Ratio
         - `RR`: Relative Risk
         - `NPV`: Negative Predictive Value
         - `SPEC`: Specificity (1 - FPR)
     - Additional measures:
         - `NNEG`: Number of negatives (controls) in the cohort
         - `NPOS`: Number of positives (cases) in the cohort
         - `checksum`: A unique hash for the population pid,time combination without randomization to identify and compare executions were performed on the same cohort. It has no `_Mean`, `_Std` or other suffixes.

3. **Value**
     - The numeric value corresponding to the cohort and measurement.
