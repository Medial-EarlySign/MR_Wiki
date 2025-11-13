# action_outcome_effect
The tool can be found at **MR_Tools/action_outcome_effect**
The tool check treatment/action effect on outcome.
the main input is MedSamples+json to create matrix or MedFeatures(the matrix itself) with list of confounders.

## **Disclaimers:**

1. We need to list all covariates that effect action\treatment. because it's human based decision it should be doable to list all. If we miss covariate or confounder we may have missleading results
2. the matching process may be prone to weighting errors that effect matching or predictor with poor results. we may look at the second_weighted_auc and would like it to be as close as it can to 0.5 (0.5 is perfect match, no more information in the covariates left)
3. We need strong ignorabilty (so except to 1st point for listing all covariates) we need all the population to have probability for action\treatment that is not pure 0 or 1. we have defined cutoff probability to drop patients who have no dilemas. so the final population in which we show results is different from the requested original (probablity no patients who are very healthy). we may look at the covariated distribution in the new population after drop
4. the action\treatment may effect indirectly on outcome through other covariates. For example taking statins will lower your LDL value and that's what lower your risk for stroke\MI. It's important to understand that if you have 2 patient with dilema for treatment the treatment effect may occour indirectly by the treatment and we also measure that.
We are not testing for direct treatment effect only
 
## **What the tool does?**

1. Selects a model thats when using it's prediction score on cross validation sqeeze all the information in the covariates:If we do inverse probabilty reweighting (similar method like matching to match populations) and try to learn validation model with cross validation we reach low AUC.It selects the model that the secondry validaiton model after the matching achieves the worst AUC.
2. Trains a model for predicting the action\treatment and calibrates the scores to probabilty 
3. Matches or Reweight with the model score to cancel the confounders - it drops patients who are only treated\only untreated because we can't measure treatment effect on them.It also show comperasion of the populations before and after the matching for each of the covariates
4. writes the stats (number of cases,contols with the original outcome) for each of the given groups to compare.
5. Does all the process in bootstrap manner to ahve mean, std, CI for each measured number on each group
 
### **App Help**
**get help from the app**

```bash
$> action_outcome_effect --h
##     ## ######## ########  ####    ###    ##
###   ### ##       ##     ##  ##    ## ##   ##
#### #### ##       ##     ##  ##   ##   ##  ##
## ### ## ######   ##     ##  ##  ##     ## ##
##     ## ##       ##     ##  ##  ######### ##
##     ## ##       ##     ##  ##  ##     ## ##
##     ## ######## ########  #### ##     ## ########Program General Options:
  -h [ --help ]         help & exit
  --base_config arg     config file with all arguments - in CMD we override those settings
  --debug               set debuging verbose
Program options:
  --rep arg                                                                     the repository if needed for age\gender cohorts
  --input arg                                                                   the location to read input
  --input_type arg (=samples)                                                   the input type (samples,samples_bin,features,medmat_csv,features_csv)
  --down_sample_max_cnt arg (=0)                                                the maximal size of input to downsample to. if 0 won't do
  --change_action_prior arg (=-1)                                               If > 0 will change prior of action in the sample to be the given number
  --output arg                                                                  the location to write output
  --json_model arg                                                              json model for creating features for the filtering of cohorts in bootstrap
  --confounders_file arg                                                        the file with the list of confounders [TAB] binSettings init line
  --patient_groups_file arg                                                     each sample and belongness - same order as input
  --patient_action arg                                                          each sample and belongness - same order as input
  --probabilty_bin_init arg                                                     the init line for probabilty binning (only in bin squezzing method)
  --features_bin_init arg                                                       the init line for features. if not empty and probabilty_bin_init not empty will
                                                                                so bin splitting(only in bin squezzing method)
  --model_type arg (=xgb)                                                       the model type to learn
  --models_selection_file arg                                                   the model selection file with all params
  --method_price_ratio arg (=-1)                                                if -1 will do reweight. if 0 - no matching. otherwise matching with this price
                                                                                ratio
  --pairwise_matching_caliper arg (=-1)                                         If > 0 will do pairwise matching using caliper for std on prctiles
  --nFolds_train arg (=5)                                                       0 means use all. no train\test. other number splits the matrix
  --nFolds_validation arg (=5)                                                  0 means use all. no train\test. other number splits the matrix
  --min_probablity_cutoff arg (=0.00499999989)                                  the minimal probabilty cutoff in reweighting
  --model_validation_type arg (=qrf)                                            the predictor type of the validation
  --model_validation_init arg (=ntrees=100;maxq=500;spread=0.0001;min_node=50;ntry=4;get_only_this_categ=1;n_categ=2;type=categorical_entropy;learn_nthreads=1;predict_nthreads=1)
                                                                                the predictor init line of the validation predictor
  --model_prob_clibrator arg (=caliberation_type=binning;min_preds_in_bin=200;min_prob_res=0.005)
                                                                                the init line for model probability calibrator
  --bootstrap_subsample arg (=1)                                                bootstrap subsample param in each loop if nbotstrap>1
  --nbootstrap arg (=1)                                                         bootstrap loop count
```
example Run with config file with all arguments in /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/base_config_example.cfg:

```bash title="example run"
Linux/Release/action_outcome_effect --base_config /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/base_config_example.cfg
WARNING: header line contains unused fields [EVENT_FIELDS,]
[date]=2, [id]=1, [outcome]=3, [outcome_date]=4, [split]=5,
read [635795] samples for [635795] patient IDs. Skipped [0] records
Samples has 635795 records. for uniq_pids = [ 0=621655 1=14140 ] all = [ 0=621655 1=14140 ]
Printing by prediction time...
Year    Count_0 Count_1 ratio
2007    131494  2398    0.017910
2008    137281  2661    0.019015
2009    137154  2791    0.019944
2010    121066  3011    0.024267
2011    94660   3279    0.033480
Adding new features using /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_1/ldl_test.json
init model from json file [/server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_1/ldl_test.json], stripping comments and displaying first 5 lines:
{
       "processes":{
        "process":{
            "process_set":"0",
model_json_version [1]
USING DEPRECATED MODEL JSON VERSION 1, PLEASE UPGRADE TO model_json_version: 2
init model from json file [/server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_1/ldl_test.json], stripping comments and displaying first 5 lines:
{
       "processes":{
        "process":{
            "process_set":"0",
Adding new rep_processor set [0]
Adding new feature_processor set [0]
Adding new feature_processor set [1]
fp_type [imputer] acting on [7] features
Adding new feature_processor set [2]
NOTE: no [predictor] node found in file
MedRepository: read config file /home/Repositories/THIN/thin_jun2017/thin.repository
MedRepository: reading signals: BP,BYEAR,Cholesterol,DM_Registry,Drug,GENDER,HDL,LDL,Smoking_quantity,Triglycerides,
Read 10 signals, 635795 pids :: data  1.552GB :: idx  0.051GB :: tot  1.603GB
Read data time 5.216681 seconds
adding virtual signals from rep type 0
MedModel::get_required_signal_names 10 signalNames 0 virtual_signals
MedModel::get_required_signal_names 10 signalNames 0 virtual_signals after erasing
MedModel::learn() : learn rep processors time 777.803 ms
MedModel::learn() : learn feature generators 4.993 ms
MedModel::learn() : generating learn matrix time 1310.35 ms
MedModel::learn() : feature processing learn and apply time 156.1 ms
printing stats for outcome:
Samples has 635795 records. for uniq_pids = [ 0=621655 1=14140 ] all = [ 0=621655 1=14140 ]
Done reading 635795 lines from [/server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/pid_groups.list]
Has 120 groups
Done reading 635795 lines from [/server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/pid_action.list]
no_outcome_no_action: 534437, no_outcome_yes_action: 87218, yes_outcome_no_action:11515, yes_outcome_yes_action:2625
outcome_prior=2.22%(14140 / 635795). action_prior=14.13%(89843 / 635795).
no_action_prob_outcome=2.109%, yes_action_prob_outcome=2.922%
Done reading 11 Confounders in [/server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/confounders.list]
I have 1 models in model selection.
Starting bootstrap loop 1
printing stats for learning action:
Samples has 635788 records. for uniq_pids = [ 0=344975 1=56611 ] all = [ 0=546381 1=89407 ]
scores hist: HISTOGRAM[0.0%:0.000, 10.0%:0.008, 20.0%:0.020, 30.0%:0.036, 40.0%:0.057, 50.0%:0.083, 60.0%:0.116, 70.0%:0.162, 80.0%:0.235, 90.0%:0.366, 100.0%:0.997]
Prob hist: HISTOGRAM[0.0%:0.000, 10.0%:0.005, 20.0%:0.020, 30.0%:0.037, 40.0%:0.060, 50.0%:0.085, 60.0%:0.119, 70.0%:0.169, 80.0%:0.244, 90.0%:0.361, 100.0%:0.886]
TRAIN_CV_AUC = 0.817, TRAIN_AUC_BINNED=0.824
Warning: matching group has very small counts - skipping group=0.019608 [199, 4]
Warning: matching group has very small counts - skipping group=0.009926 [398, 4]
Warning: matching group has very small counts - skipping group=0.009877 [401, 4]
Warning: matching group has very small counts - skipping group=0.009756 [399, 4]
Warning: matching group has very small counts - skipping group=0.006633 [597, 4]
Warning: matching group has very small counts - skipping group=0.004963 [401, 2]
Warning: matching group has very small counts - skipping group=0.004926 [399, 2]
Warning: matching group has very small counts - skipping group=0.003731 [802, 3]
Warning: matching group has very small counts - skipping group=0.003317 [1206, 3]
Warning: matching group has very small counts - skipping group=0.003306 [603, 2]
Warning: matching group has very small counts - skipping group=0.003300 [603, 2]
Warning: matching group has very small counts - skipping group=0.002982 [1003, 3]
Warning: matching group has very small counts - skipping group=0.002481 [1608, 4]
Warning: matching group has very small counts - skipping group=0.002475 [806, 2]
Warning: matching group has very small counts - skipping group=0.001990 [1002, 2]
Warning: matching group has very small counts - skipping group=0.001658 [604, 1]
Warning: matching group has very small counts - skipping group=0.001657 [1207, 2]
Warning: matching group has very small counts - skipping group=0.001656 [602, 1]
Warning: matching group has very small counts - skipping group=0.001653 [1203, 2]
Warning: matching group has very small counts - skipping group=0.001650 [1812, 3]
Warning: matching group has very small counts - skipping group=0.001325 [3015, 4]
Warning: matching group has very small counts - skipping group=0.001244 [2410, 3]
Warning: matching group has very small counts - skipping group=0.001243 [2412, 3]
Warning: matching group has very small counts - skipping group=0.001242 [2409, 3]
Warning: matching group has very small counts - skipping group=0.001241 [805, 1]
Warning: matching group has very small counts - skipping group=0.000902 [2217, 2]
After Matching has 88530.0 controls and 82542.0 cases with 48.250% percentage
SECOND_WEIGHTED_AUC = 0.499
Comparing populations - original population has 635795 sampels, matched has 171072 samples. Features distributaions:
BAD feature Age :: original mean=53.255[30.000 - 78.000],std=14.132. matched mean=59.597[40.000 - 78.000],std=11.555. mean_diff_ratio=11.908%
BAD feature FTR_000003.DM_Registry.ever_DM_Registry_Diabetic.win_0_100000 :: original mean=0.050[0.000 - 1.000],std=0.219. matched mean=0.110[0.000 - 1.000],std=0.313. mean_diff_ratio=119.001%
BAD feature FTR_000004.Current_Smoker :: original mean=0.244[0.000 - 1.000],std=0.429. matched mean=0.282[0.000 - 1.000],std=0.449. mean_diff_ratio=15.259%
GOOD feature FTR_000005.BP.last.win_0_1095 :: original mean=80.974[64.000 - 100.000],std=10.374. matched mean=82.565[67.000 - 100.000],std=10.551. mean_diff_ratio=1.964%
GOOD feature FTR_000006.BP.last.win_0_1096.t0v1 :: original mean=134.039[108.000 - 166.000],std=17.669. matched mean=139.302[112.000 - 172.000],std=17.973. mean_diff_ratio=3.926%
BAD feature FTR_000007.LDL.last.win_0_1095 :: original mean=128.172[73.359 - 189.189],std=36.009. matched mean=145.561[84.942 - 204.633],std=37.765. mean_diff_ratio=13.567%
BAD feature FTR_000008.Cholesterol.last.win_0_1095 :: original mean=209.340[146.718 - 277.992],std=39.961. matched mean=231.132[166.023 - 297.297],std=41.690. mean_diff_ratio=10.410%
GOOD feature FTR_000009.HDL.last.win_0_1095 :: original mean=55.937[34.749 - 84.942],std=16.492. matched mean=53.698[30.888 - 84.942],std=16.333. mean_diff_ratio=4.003%
BAD feature FTR_000010.Triglycerides.last.win_0_1095 :: original mean=130.621[53.100 - 274.350],std=96.524. matched mean=164.286[61.950 - 336.300],std=116.033. mean_diff_ratio=25.773%
BAD feature FTR_000013.Drug.category_set_BloodPressureDrugs.win_0_1095 :: original mean=0.108[0.000 - 1.000],std=0.310. matched mean=0.166[0.000 - 1.000],std=0.372. mean_diff_ratio=54.031%
GOOD feature Gender :: original mean=1.550[1.000 - 2.000],std=0.497. matched mean=1.484[1.000 - 2.000],std=0.500. mean_diff_ratio=4.258%
predictor AUC with CV to diffrentiate between populations is 0.751
Processed 1 out of 5(20.00%) time elapsed: 3.7 Minutes, estimate time to finish 14.7 Minutes
Starting bootstrap loop 2
...
 
```

you may see that after the matching the secondry model doesn't achieves good results "SECOND_WEIGHTED_AUC = 0.499".
but you can see that the population is very different from the original requested one. a predictor can seperated them with AUC=0.751. you can see that the "DM_Registry" has more than doubled it's value from 0.05 to 0.11!!
the GOOD/BAD keywords only shows you where the populations are differs. you need to remember that those diffrences are unavoidable - to induce causality you have to look on population with strong ignorabilty!
If you have for example very healty patients with LDL = 70, low BMI and without statins (and you never see treated patients with those covariates in the data), you just can't induce treatment effect on them so you have to drop them.
the same thing happend on "very sick people". inducing treatment effect only works on grey zones when we have dilemas
 
It also output the results to /tmp/LDL.txt (if nbootstrap==1 all the numbers are without STD, and CI):

```bash title="head of output"
head  /tmp/LDL.txt
mean_incidence_precantage=2.13% chi-square=4649.937     DOF=119 prob=0.000
risk_factor     controls_count  cases_count     case percentage lift    chi-square      chi-prob
LDL_Group=0.00, LDL_Delta=-1, Treated_Group=0   54.0    5.0     8.47%   3.97    11.37   0.00
LDL_Group=0.00, LDL_Delta=-1, Treated_Group=1   26.6    2.4     8.41%   3.94    3.37    0.07
LDL_Group=0.00, LDL_Delta=-1, Treated_Group=2   47.9    0.0     0.00%   0.00    1.02    0.31
LDL_Group=0.00, LDL_Delta=-2, Treated_Group=0   6.0     3.0     33.33%  15.63   41.97   0.00
```
We may see each risk_factor and it's stats - number of controls,cases

### Input Arguments:
`cat base_config_example.cfg`

```ini
rep = /home/Repositories/THIN/thin_jun2017/thin.repository
#input = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_2/final_matrix.bin
#input_type = features
input = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_1/random_ldl_test_no_statins.samples
input_type = samples
json_model = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/input_option_1/ldl_test.json
output = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/output/results.txt
patient_action =  /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/pid_action.list
confounders_file = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/confounders.list
patient_groups_file = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/pid_groups.list
#features_bin_init = split_method=partition_mover;binCnt=100;min_bin_count=100;min_res_value=0
#probabilty_bin_init = split_method=iterative_merge;min_bin_count=100;binCnt=500
model_type = xgb
models_selection_file = /server/Work/Users/Alon/UnitTesting/examples/action_outcome_effect/xgb_model_selection.cfg
nFolds_train = 5
nFolds_validation = 4
min_probablity_cutoff = 0.005
model_validation_type = qrf
model_validation_init = ntrees=100;maxq=500;spread=0.0001;min_node=50;ntry=4;get_only_this_categ=1;n_categ=2;type=categorical_entropy;learn_nthreads=20;predict_nthreads=20
model_prob_clibrator = caliberation_type=binning;min_preds_in_bin=200;min_prob_res=0.005
#method_price_ratio = -1
method_price_ratio = 6.2
nbootstrap = 5
```

the input argument is the main data file and it can be MedSamples with json to create matrix or the MedFeatures itself.

- patient_action - a file with same number of lines as the samples in the input, each line is correspond to the same sample in the input. it may be 0/1 for [no treatment, treatment] mark for each sample
- confounders_file - a file list with all the confounders search name (searching contains in the column names) in the matrix of input. each line consist of the the confounder search name
- example: **$> head confounder.list**

```txt
Age
Gender
LDL.last
```

here we have 3 confounders: Age,Gender and LDL.last

- patient_groups_file - a file with same number of lines as the samples in the input, each line is correspond to the same sample in the input. it will be the risk group name for the sample for later split. 
you may write for example in line: "Age=20-40;Gender=Male" to mark the sample as belong to that group in the output results
- models_selection_file - a file with initialization of the parameters of the model. you may provide more than one option for parameter with "," and than the tool will select the best option over all available options. 
you may also provide only one option and than the tool will just use this. for example:
**$> head xgb_model_selection.cfg**

```ini
max_depth=5,6,7
num_round=200
eta=0.1,0.3
```
here we fixed num_round to be 200 and checks all the options of max_depth = 5 or 6 or 7 with eta = 0.1 or 0.3 - we have 6 model options
 
