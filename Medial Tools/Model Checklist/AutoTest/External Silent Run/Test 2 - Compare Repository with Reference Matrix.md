# Test 2 - Compare Repository with Reference Matrix

**Overview**
The main goal of this 'test' is to understand the differences between the current dataset, and the dataset that was used to train the model. It would be important, at later phase, in estimating model performance with the new dataset.
****
**Parameters (see env.sh)**
All parameters are included in env.sh and described in [External Silent Run](../External%20Silent%20Run).
In particular, this test uses:

- REFERENCE_MATRIX=... full path to reference matrix (feature matrix from model train)
- CMP_FEATURE_RES=... list of important features for the model (based on butwhy of original model)
****
**What is actually done?**
The test builds 2 propensity models to separate and predict if data point is from reference or the new dataset:

- "Over fitted model" - a model trained and tested on the full data, that uses all model features => output in directory 'compare'
- "modest_model" - using standard separation to train and test, a model that uses just the important features => output in directory 'compare.no_overfitting'
****
**Test Results Review**
Each directory (compare, compare.no_overfitting) includes 4 major outputs: 

- compare_rep.txt - file that compares mean, std for each feature in reference matrix and in "loaded repository" based on input files
- test_propensity.bootstrap.pivot_txt - how good is the separation between reference and input data
- shapley_report.tsv - butwhy of the model that separates the input data reference matrix
- features_diff - graphs comparisons of top 10 most different features.
 
**How to read compare_rep.txt**
During the ETL we tested each signal against its reference. Here we test every feature.
First, look in the file just in the compare directory.
It includes 2 tables in txt format. Run the following code to turn it into readable dataframes.
```
f = os.path.join(DIR, 'compare/compare_rep.txt')
t2 = pd.read_csv(f, sep= '\r')
t2 = t2[t2[t2.columns[0]].map(lambda x: x[0:3])=='MAN']
cut = t2.index.min()
t21 = pd.read_csv(f, nrows=cut)
t21['status'] = t21.index.map(lambda x: x[0].split(' ')[0])
t21['feature'] = t21.index.map(lambda x: x[0].split('::')[0].rstrip().split(' ')[-1])
t21['TRAIN mean'] = t21.index.map(lambda x: x[0].rstrip().split('mean=')[1])
t21['TRAIN std'] = t21.index.map(lambda x: x[1].rstrip().split('=')[1])
t21['TRAIN miss_cnt'] = t21.index.map(lambda x: x[2].rstrip().split('=')[1].split("|")[0])
t21['TEST mean'] = t21.index.map(lambda x: x[2].rstrip().split('mean=')[1])
t21['TEST std'] = t21[t21.columns[0]].map(lambda x: x.rstrip().split('=')[1])
t21['TEST miss_cnt'] = t21[t21.columns[1]].map(lambda x: x.split('|')[0].split('=')[1].rstrip())
t21['mean_diff_ratio'] = t21[t21.columns[1]].map(lambda x: x.split('mean_diff_ratio=')[1].split('|')[0].rstrip())
t21['IMP'] = t21[t21.columns[1]].map(lambda x: x.split(' ')[-1])
cols = ['status', 'feature', 'TRAIN mean', 'TRAIN std', 'TRAIN miss_cnt', 'TEST mean', 'TEST std', 'TEST miss_cnt', 'mean_diff_ratio', 'IMP'] 
t21 = t21[t21.status=='BAD'][cols].reset_index(drop=True)
 
t22 = pd.read_csv(f, skiprows=cut+1, sep='\t')
```
The first dataframe, t21, should be ignored.
t21 shows moments, range and missing values count, for every feature, comparing the reference to the tested dataset. A general status is calculated - however, logic is unclear and need debug.
<img src="/attachments/13926455/13926475.png"/>
The second dataframe, t22, shows the same information (without range), plus Mann Whitney test result.

- _1 is for the new dataset
- _2 is for the reference
- The Mann-Whitney U Test assesses whether two sampled groups are likely to derive from the same population, but note test limitations - if median and shape are the same for both samples, P_value would be high even for different std/scale. 
<img src="/attachments/13926455/13926476.png"/>
In table t22:

- We need to make sure we don't see low P_value for any important feature to the model, or proxy for such features, i.e.. we may list MCH.min.win_0_180 as important feature, and we don't want it or MCH.min.win_0_360 to have low P-value.
- We need to understand the reasons for the low P-value when happened, in order to better understand the new data set. For instance, in the table above, we see that in the tested dataset RDW was not given close to sample point, probably because it is not part of the panel. As RDW is not an important signal, we can ignore it.
****
**How to read test_propensity.bootstrap.pivot_txt**
If we looked in the compare directory - we are likely to see AUC=1, i.e., perfect separation between the two dataset. However, it is not a problem, as it might use features that are not important to the model.
Therefore, look in the file just in the compare.no_overfitting directory:

- Watch the AUC_Mean. 
- We would like it to be close to 0.5.
- Higher AUC would reduce sample size when we match the samples to estimate performance, and smaller matched sample means bad accuracy.
- However often AUC is greater than 0.5, and we don't have a clear definition of what is bad:
  - 0.99 is bad, for sure, but what about 0.8? 0.7?
To see if we have statistically significant difference in one of the important feature, look at compare_rep.txt in the compare.no_overfitting directory. However, we may see very high AUC without any significant difference in any specific feature (recall Mann Whitney limitations mentioned above) ...
 
**How to read shapley_report.tsv and features_diff**
To better understand the results of the separation model we have two more outputs:

- shapley_report.tsv is a standard butwhy report, look in the file just in the compare.no_overfitting directory. Here you can see the feature importance in the separation model that uses just the important features of the model we want to apply to the dataset. 
- Graphical representation of the differences for every feature can be found in the feature_diff directory:
  - Look for anomalies in the graphs for the features with highest imprtance in the shapley report.
  - Always look at Age, as some other differences might be proxy to difference in Age distribution.
Good separation, no matter what feature/features were used, would hurt the accuracy of model performance estimate by matching (ass later). However, we don't have a good measure to say by how much ...  
 
**Example**
AUC_Mean is 0.98 - very high. However no significant different seen in compare_rep.txt Mann Whitney test. In shapely_report one feature has very high importance. Next we look at the difference dataset-reference for this feature - comparing controls to controls.
<img src="/attachments/13926455/13926485.png"/>
We see that the reference has several dominant values - probably due to imputations.
So how come the feature was important for the model?

- In this case we use as reference a dataset different from the one we use for model training and feature importance. 
- However, the reference dataset has many missing values for the relevant signal.
- Lesson learned is that we need to use as reference the original dataset (test samples only).
 
 
