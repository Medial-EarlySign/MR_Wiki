# Compare AUC's
As a part of the Lung cancer paper, we were asked to check the statistical significance of the AUC's difference (our model vs. a baseline model).
We used a non-parmetric empirical method describe by Delong. The method is decribed In the attached bwloe pdf (Comparing Two ROC Cureves - Paired Design - page 547-6)

The tool can be found in [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) `MedProcessUtils/CompareRocs`
 
There are two modes for running the Tool:
1. Using 2 prediction files (one for each model)
Example:
**Running Example**
```bash
python /server/UsersData/ron-internal/MR/Tools/CompareRocs/compareROCs.py --preds_file_1 /server/Work/Users/Ron/Projects/LungCancer/results/model_27/model_27_test.preds --preds_file_2 /server/Work/Users/Ron/Projects/LungCancer/results/Tammemagi_nsclc_ever_smokers_smoking_intensity/Tammemagi_nsclc_ever_smokers_smoking_intensity_non_linear_test.preds
```

```text
sys:1: DtypeWarning: Columns (1,2,3,4,5,6) have mixed types. Specify dtype option on import or set low_memory=False.
preds are equal
model 1: AUC: 0.8647144227120102, Variance: 5.427313956814398e-06, estimated 95% CI: [0.8601482898518649, 0.8692805555721554]
model 2: AUC: 0.823383955909251, Variance: 8.174414229417143e-06, estimated 95% CI: [0.817780133133348, 0.8289877786851539]
Z - score: 23.081440151744086, p-value: 0.0
```
 
 
 
2. 
Using 2 bootstrap .Raw files + the requested cohort string
Example:
```bash
python /server/UsersData/ron-internal/MR/Tools/CompareRocs/compareROCs.py --preds_file_1 /server/Work/Users/Ron/Projects/LungCancer/results/model_27/paper/p_value_bs_out_1.Raw --preds_file_2 /server/Work/Users/Ron/Projects/LungCancer/results/model_27/paper/p_value_bs_out_2.Raw --cohort_string Time-Window:270.000-365.000,Age:55.000-80.000,Lung_Cancer_Type.category_set_NotNonSmallCell.win_-3650_3650:-0.500-0.500,NLST_Criterion_min_age_55_max_age_80_pack_years_30:0.500-15.000
```

```text
preds are equal
model 1: AUC: 0.8011430555038992, Variance: 0.00025990328389302294, estimated 95% CI: [0.7695448837940765, 0.8327412272137219]
model 2: AUC: 0.7436638110941679, Variance: 0.0003739639445801397, estimated 95% CI: [0.7057610422045595, 0.7815665799837763]
Z - score: 4.470422572292469, p-value: 3.903260102799955e-06
```

[Comparing_Two_ROC_Curves-Paired_Design.pdf](../../attachments/11207107/11207109.pdf)
