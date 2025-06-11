# Test_12 - fairness

## Overview
Compare sensitive groups in the same cutoff and check that the performance is similar. \
A common definition is to have similar sensitivity for the same cutoff. In other words: no matter if you are a case from this group or that group (black/white male/female) - you will have similar probability to be captured by the model - which is the sensitivity

## Input
- WORK_DIR - output work directory
- MODEL_PATH - path for model
- REPOSITORY_PATH - repository path
- TEST_SAMPLES - test samples
- BT_JSON_FAIRNESS - bootstrap json features to filter the cohort for testing
- FAIRNESS_BT_PREFIX - bootstrap cohort definition to define the cohort for testing for fairness
- config/fairness_groups.cfg - defines the group that we want to compare:
Each line defines 2 or more groups to compare one with each other.
Each line consist of 2 tokens tab delimited. First token is bootstrap filter definition for each group separated by "|". 
The second token is the "pretty" names to give each of the filters separated by "|".
For example:
```
Gender:1,1|Gender:2,2  [TAB]   Males|Females
```

## Output
$WORK_DIR/fairness
- fairness_report.tsv - a summary table that compare sensitivity/ specificity AUC in the same cutoff 5%,10%
- fairness_report.* - result that compare statistical chi square between the groups to see if the different in sensitivity is statistically significant. There are 2 files. 1 for 5% PR cutoff and 1 for 10% PR cutoff
- Graph_fairness - plots the sensitivity as function of score threshold in the different groups (with confidence intervals) that we can compare not just 5,10%
- graph_matched - If the model is not "fair" we tried to do matching by strata (The default in the config is age). Here we have graphs results after matching
 
What to look for?
please search for low chi square in fairness report and similar sensitivity. Have a look on the graph Graph_fairness. If needed see the matched resutls.
