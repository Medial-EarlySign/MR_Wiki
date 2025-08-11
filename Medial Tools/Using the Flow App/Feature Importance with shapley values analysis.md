# Feature Importance with shapley values analysis
Please reffer to this page: [ButWhy Practical Guide](/Infrastructure%20Home%20Page/PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md) which is more recent
 
Prints average/median feature contribution by SHAPLEY values for each feature by different feature value bins.
For example: average SHAPLEY contribution for the model on young population compared to middle age populaiton and elderly
 
```bash
$> Flow --help_module shap_val_request
shap_val_request option(switch):
  --                                    f_model - model file name
  --                                    f_matrix - features mat (for SHAP values feature importance) - in MedMat csv format.
  --                                    f_samples - samples file name for SHAP values
  --                                    rep - repository. Used when samples file is given for calculating SHAP feature importance
  --max_samples arg (=0)                if > 0 : how many samples to subsample if matrix is large - to speedup
  --group_ratio arg (=0.200000003)      group size aroung prctile
  --group_cnt arg (=3)                  how many groups
  --group_names arg                     naes groups with ,
  --                                    normalize - to normalize each prediction to sum score
  --bin_uniq arg (=1)                   whether to bin groups without respect to the distribution - only by values
  --normalize_after arg (=0)            If true, will do the normalization to percentage after sum of all contribs from all data - The global feature
                                        importance will sum to 100
  --remove_b0 arg (=1)                  If true, will remove b0 contrib if exists
  --group_signals arg                   a file to signals to group by or BY_SIGNAL or BY_SIGNAL_CATEG to group by signals or group by signal and support
                                        diffrent categ values
  --                                    bin_method - bining method to bin each feature
  --                                    f_output - the output file location to write
Example run:
$> Flow --rep ${REPOSITORY_PATH} --shap_val_request --f_model ${MODEL_PATH} --f_samples ${SAMPLES_PATH} --max_samples 10000 --group_cnt 3 --group_names Low,Medium,High --group_ratio 0.1 --normalize 1 --bin_uniq 1 --f_output ${OUTPUT}
 
 
```

Can be given either f_matrix  or f_samples .
- group_cnt - how many groups to split each feature, corresponding argument is  group_names  - if we want to provide names to the groups (optional)
- group_ratio - how many values to catch in each bin. 0.2 - means each bin is 20% of the data
- normalize - whether or not to normalize shap values to percentage
- bin_uniq: 0 - the group_ratio is taken with respect to all data. 0.1 means 10% of the data in each bin. 1 - means 10% of the different flatted values. For example if age range is 0-100, 0.1 means taking 10 years in each bin
- remove_b0 : 1 - remove prior/baseline score. the baseline score (like in linear model) is constant that is added to sum the contributions to the prediction score (it is constant for all samples, you can think about it as prior score when no information is given to match the prevalence). if 0 - will keep it and print also b0
- normalize_after :0 - If 1 will use normalization factor after calculating global feature importance by summing contribution for all features (without normalizing) - will normalize by the sum of all global feature importance.  If 0 - will do the normalization to for each prediction seperatly.
- group_signals : option to use file path in format of Feature_name [TAB] group_name to map features into groups. can also specify BY_SIGNAL to group feature by signal or BY_SIGNAL_CATEG to group feature by signal, but categorical signals liek Diagnosis/Drug to group also by thier category value.
- bin_method - binning argument of how to bin each feature into groups - more configurable than group_cnt,group_ratio arguments. If provided will use this instead of group_cnt,group_ratio,bin_uniq,group_names arguments example parameter: --bin_method "split_method=iterative_merge;binCnt=50;min_bin_count=100;min_res_value=0.1" splits into 50 bins, each has at least 100 observations, minimal feature resulotion value is 0.1 - does the bining iteratively, each iteration combines 2 adjacents bins which thier sum is the smallest.
 
 
output example:
#output of first 3 feature in a model
 
```bash
cat /server/Work/Users/Alon/NWP/outputs/new_flu_comp_importance.tsv | head -n 4 | awk ' { for (i=1;i<=NF;i++) a[i]=a[i]"\t"$i; } END { for (i in a) {printf("%d%s\n", i, a[i])} }' | sort -g -k1
```
<table><tbody>
<tr>
<th>1</th>
<th>Feature</th>
<th>Age</th>
<th>ADMISSION.category_dep_set_Hospital_Emergency_Department.win_0_3650</th>
<th>DIAGNOSIS.category_dep_set_ICD10_CODE:J00-J99.win_0_1825</th>
</tr>
<tr>
<td>2</td>
<td>Importance</td>
<td>5.29565</td>
<td>4.86493</td>
<td>4.14151</td>
</tr>
<tr>
<td>3</td>
<td>SHAP::Low_Mean</td>
<td>15.40829</td>
<td>-4.34948</td>
<td>-5.09209</td>
</tr>
<tr>
<td>4</td>
<td>SHAP::Low_Std</td>
<td>8.55664</td>
<td>1.03023</td>
<td>1.38771</td>
</tr>
<tr>
<td>5</td>
<td>SHAP::Low_Prctile10</td>
<td>4.50017</td>
<td>-5.63054</td>
<td>-6.83017</td>
</tr>
<tr>
<td>6</td>
<td>SHAP::Low_Prctile50</td>
<td>15.01624</td>
<td>-4.32302</td>
<td>-5.22645</td>
</tr>
<tr>
<td>7</td>
<td>SHAP::Low_Prctile90</td>
<td>27.21665</td>
<td>-3.11247</td>
<td>-3.26204</td>
</tr>
<tr>
<td>8</td>
<td>FEAT_VAL::Low_Mean</td>
<td>5.27483</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>9</td>
<td>FEAT_VAL::Low_Std</td>
<td>2.65752</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>10</td>
<td>FEAT_VAL::Low_Prctile0</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>11</td>
<td>FEAT_VAL::Low_Prctile10</td>
<td>2</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>12</td>
<td>FEAT_VAL::Low_Prctile50</td>
<td>6</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>13</td>
<td>FEAT_VAL::Low_Prctile90</td>
<td>9</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>14</td>
<td>FEAT_VAL::Low_Prctile100</td>
<td>9</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>15</td>
<td>SHAP::Medium_Mean</td>
<td>-4.9027</td>
<td>-1.20844</td>
<td>-1.01744</td>
</tr>
<tr>
<td>16</td>
<td>SHAP::Medium_Std</td>
<td>1.24807</td>
<td>4.93947</td>
<td>4.30092</td>
</tr>
<tr>
<td>17</td>
<td>SHAP::Medium_Prctile10</td>
<td>-6.37917</td>
<td>-5.42372</td>
<td>-6.2759</td>
</tr>
<tr>
<td>18</td>
<td>SHAP::Medium_Prctile50</td>
<td>-5.06777</td>
<td>-3.79598</td>
<td>-1.43337</td>
</tr>
<tr>
<td>19</td>
<td>SHAP::Medium_Prctile90</td>
<td>-3.15287</td>
<td>6.85837</td>
<td>4.0099</td>
</tr>
<tr>
<td>20</td>
<td>FEAT_VAL::Medium_Mean</td>
<td>44.95996</td>
<td>0.30183</td>
<td>0.49355</td>
</tr>
<tr>
<td>21</td>
<td>FEAT_VAL::Medium_Std</td>
<td>3.17098</td>
<td>0.45905</td>
<td>0.49996</td>
</tr>
<tr>
<td>22</td>
<td>FEAT_VAL::Medium_Prctile0</td>
<td>40</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>23</td>
<td>FEAT_VAL::Medium_Prctile10</td>
<td>40</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>24</td>
<td>FEAT_VAL::Medium_Prctile50</td>
<td>45</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>25</td>
<td>FEAT_VAL::Medium_Prctile90</td>
<td>49</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>26</td>
<td>FEAT_VAL::Medium_Prctile100</td>
<td>50</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>27</td>
<td>SHAP::High_Mean</td>
<td>10.31504</td>
<td>6.05717</td>
<td>3.16373</td>
</tr>
<tr>
<td>28</td>
<td>SHAP::High_Std</td>
<td>5.51557</td>
<td>1.66402</td>
<td>0.99215</td>
</tr>
<tr>
<td>29</td>
<td>SHAP::High_Prctile10</td>
<td>4.30656</td>
<td>3.79519</td>
<td>1.89119</td>
</tr>
<tr>
<td>30</td>
<td>SHAP::High_Prctile50</td>
<td>9.18254</td>
<td>6.1565</td>
<td>3.20303</td>
</tr>
<tr>
<td>31</td>
<td>SHAP::High_Prctile90</td>
<td>17.50269</td>
<td>8.15519</td>
<td>4.39117</td>
</tr>
<tr>
<td>32</td>
<td>FEAT_VAL::High_Mean</td>
<td>84.57291</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>33</td>
<td>FEAT_VAL::High_Std</td>
<td>2.49059</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>34</td>
<td>FEAT_VAL::High_Prctile0</td>
<td>81</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>35</td>
<td>FEAT_VAL::High_Prctile10</td>
<td>81</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>36</td>
<td>FEAT_VAL::High_Prctile50</td>
<td>85</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>37</td>
<td>FEAT_VAL::High_Prctile90</td>
<td>88</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>38</td>
<td>FEAT_VAL::High_Prctile100</td>
<td>90</td>
<td>1</td>
<td>1</td>
</tr>
</tbody></table>


## Explain for example for Age:
- feature importance (normalized) is about 5.3% of the score on average for the XGBoost raw score without applying sigmoid function (and no calibration after it)
- SHAP::Low_Mean - 15.4 - means that on group "Low" the average contribution is 15.4% of the score (positive). we can see more details about the contribution distribution in this group - std, percentles..
- FEAT_VAL::Low_Prctile0 - the lowest value in the bin of "Low" is age 0. the highest value is FEAT_VAL::Low_Prctile100 = 9 - which means the "Low" age group is 0-9 years old, the average age is FEAT_VAL::Low_Mean - 5.27
- SHAP::Medium_Mean -4.9% - the contribution in negative in about 5% for 40-50 years olds
- SHAP::High_Mean - 10.3% positive contribution to elderly of about 10% for 81-90 years old
 
Graph Creation:
/server/Work/ExternalProjects/NWP_Flu_20190903/scripts/get_feature_importance_2019.sh
or with:
```bash
#Full path of scripts (should already be in system path) $MR_ROOT/Projects/Scripts/Python-scripts/feature_importance_printer.py
feature_importance_printer.py --report_path FLOW_shap_val_request_output  --output_path new_output_path_for_graph --num_format "%2.1f" --feature_name "" --max_count 20
```

To print graph for specific feature influence - pass on feature_name argument - in this example "Age" was passed. to print global features importance of all features (top 20/max_count) eliminate or pass feature_name as empty string.
num_format - is format string for the numbers
 
Example of HTML graph:
<img src="/attachments/11207088/11207102.png"/>
