# SignalsDependencies
The Code exists in: **MR_Tools/SignalsDependencies** and is basically using library functions in [MedRegistry](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry) object - method called "calc_signal_stats" after loading the registry.
This tool will allow you to discover relevant categorical signals (for example: readcodes or drugs) that has statstical connection to you outcome within a defined time-window.
The tool will create MedSamples based on the signal time points and than label those samples based on the registry and "labeling_params" parameter which defines the rules for the labeling - either case, control or excluded (if can't determine for example).
It will create contingency table from samples within time-window for each gender and age group:

- Signal value doesn't exists (the patient didn't have certain readcode value in the time window) & the registry outcome is false - will be calcluated based on the incidence rate of the outcome in this age bin
- Signal value doesn't exists (the patient didn't have certain readcode value in the time window) & the registry outcome is true - will be calcluated based on the incidence rate of the outcome in this age bin
- Signal value exists (the patient certain readcode value in the time window) & the registry outcome is false
- Signal value exists (the patient certain readcode value in the time window) & the registry outcome is true
It will allow you the sort and filter the results using fdr (false detection rate, minimal count for signal existence, minimal coutn for positive registry in siganl existence.. and more)
It will also allow you to create and look at specific tables of Male,Female and all age-group for certain readcode value to see the connection between the specific signal and the registry
 
The registry format is tab-delimited:
[PID, Start_Date, End_Date, RegistryValue] 
Start_date - is the outcome registry start time for the outcome to be labeled (in cancer it's the first time the patient got cancer)
End_date - is the outcome registry finish time (where after it the outcome value isn't valid anymore) - for example it may be censoring date. for control it's the last time we know it's still control
for more details reffer to [MedRegistry ](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry)
 
Explain on labeling_params and inc_labeling_params can be given in [TimeWindowInteraction](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry/TimeWindowInteraction.md). Those arguments are LabelParams objet that defines how to label sampels.
 
**Important parameters for the tool (that most be supplied, don't use default ones unless you know what you are doing):**

- global_rep - Repository path
- registry_path - the path to the MedRegistry file
- labeling_params - the parameters to control how to label the samples created by the signal time points
- test_from_window, test_to_window - to control the time window
- test_main_signal - the signal to test
If you are using default parameters, you are at high risk of a problem.

## Hirarchy Filtering parameters:
The filtering happens in this method: medial::contingency_tables::filterHirarchy
The filtering happens in this order:

1. float filter_child_count_ratio (default value is 0.05)
 If child ratio count is similar to the parent, keep only parent code. For example child has 10,000 samples and parent has 10,100 samples. The additional 100 samples out of 10,100 are little ~1% which is less than default value of 5%, so the child is eliminated.
2. Those are used together
 float filter_child_pval_diff (default value is 1e-10 )
 float filter_child_lift_ratio (default value is 0.05)
When both p_value difference between parent and child is below filter_child_pval_diff AND diff in average lift is below filter_child_lift_ratio 
, will remove parent. The parent "behaves" differently from at least 2 children, so aggregation of those children into the parent category might be unreasonable. 
3 .float filter_child_removed_ratio (default value is 1)
Only when node has child that pass the above filters and at least 1 child eliminated.
 If the aggregated sum of removed samples due to filtered children is high, consider removal of parent code.
For example: if parent has 10,000 samples, and removed children with 8,000 codes, than remove the parent, since aggregation of the children below the parent is unreasonable.

## Examples
### labeling_params parameter examples:
since this parameter is tricky, here are some examples:

- **Outcome which can happen several times for a specific period (For example Flu). labeling_params="label_interaction_mode=0:after_start|1:before_start,after_start;conflict_method=all"**Explaination - cases has the settings of "before_start,after_start",  which means the from_time_window from the signal time should happen before registry start time records (tha patient starts as control) AND the to_time_window from the signal time should happen after the start time of the same registry record (the patient turned into case). Controls has the settings of "before_end,after_start" - which means you should have some overlap with control period of non pregnancy - start time window of signal is before end of control period and end time window of signal is after the start. conflict_method=all - means if we have sample which is also control and also case be those settings - treat it (for counting prupose) also as control and as case.

- **outcome which occours once (for example cancer)-  labeling_params="label_interaction_mode=0:after_start,before_end|1:before_start,after_start;conflict_method=max"**Explanation - controls are the ones who the from_time_window of the sample occours after_start of registry control period AND before_end of the same registry control period - means the whole time window is inside the control period. Cases are those where the from_time_window is before_start of specific case time period and the to_time_window is after_start of that same case period. the end_period for cases in this registry is not use since there is no "due" date for cancer.
### Run Examples:
**Program Help**
```bash title="Program Help"
SignalsDependencies --help
##     ## ######## ########  ####    ###    ##
###   ### ##       ##     ##  ##    ## ##   ##
#### #### ##       ##     ##  ##   ##   ##  ##
## ### ## ######   ##     ##  ##  ##     ## ##
##     ## ##       ##     ##  ##  ######### ##
##     ## ##       ##     ##  ##  ##     ## ##
##     ## ######## ########  #### ##     ## ########
 
Program General Options:
  -h [ --help ]                         help & exit
  --help_module arg                     help on specific module
  --base_config arg                     config file with all arguments - in CMD we override those settings
  --debug                               set debuging verbose
 --version                              prints version information of the program
Global Options:
  --global_rep arg                      repository path to fetch signal\registry
  --global_stats_path arg               location to save or load stats dictionary for fast load in the second time for more filtering
  --global_override arg (=0)            whather or not override stats file if already exists
  --global_age_bin arg (=5)             age bin size (default is 5 years)
Registry Options:
  --registry_path arg                   location to load registry txt file
  --registry_init_cmd arg               An init command for registry creation on the fly
  --registry_save arg                   location to export registry txt file created by this tool on the fly
  --registry_filter_train arg (=1)      if True will filter TRAIN==1
  --labeling_params arg (=conflict_method=all;label_interaction_mode=0:all,before_end|1:before_start,after_start;censor_interaction_mode=all:within,all)
                                         the labeling params
  --sub_sample_pids arg (=0)             down-sample pids till this number to speedup calculation. If 0 no sub sampling
Censoring Registry Options:
  --censoring_registry_path arg         location to load registry txt file for censoring
  --censoring_registry_type arg (=keep_alive)
                                        censoring registry default path
  --censoring_registry_args arg         An init command for registry creation on the fly
Test Signal Options:
  --test_main_signal arg                main signal to look for it's values when creating test signal
  --test_from_window arg (=0)           min time before the registry to look for signal (if negative means search forward)
  --test_to_window arg (=365)           max time before the registry to look for signal (if negative means search forward)
  --test_hierarchy arg                  Hierarchy type for test signal. free string to filter regex on parents to propage up. to cancel pass "None"
  --inc_labeling_params arg (=conflict_method=all;label_interaction_mode=all:before_end,after_start)
                                        params for outcome registry interaction with age bin
Filtering Options:
  --filter_min_age arg (=20)            minimal age for filtering population in stats table nodes
  --filter_max_age arg (=90)            maximal age for filtering population in stats table nodes
  --filter_gender arg (=3)              filter by gender - 1 for male, 2 - for female, 3 - take both
  --filter_positive_cnt arg (=0)        minimal positive count in registry for signal value to keep signal value from filering out
  --filter_total_cnt arg (=100)         minimal count for signal value to keep signal value from filering out to remove small redandent signal values
  --filter_pval_fdr arg (=0.0500000007) filter p value in FDR to filter signal values
  --filter_min_ppv arg (=0)             filter minimal PPV for signal value and registry values
  --filter_positive_lift arg (=1)       should be >= 1. filtering of lift > 1. from which value? for example at least lift of 1.5
  --filter_negative_lift arg (=1)       should be <= 1. filtering of lift < 1. from which value? for example at tops lift of 0.8
  --filter_child_pval_diff arg (=1.00000001e-10)
                                        p value diff to consider similar in hirarchy filters
  --filter_child_lift_ratio arg (=0.0500000007)
                                        lift change ratio in child comapred to parent to consider similar
  --filter_child_count_ratio arg (=0.0500000007)
                                        count similarty to consider similar in hirarchy filters
  --filter_child_removed_ratio arg (=1) If child removed ratio is beyond this and has other child taken - remove parent
  --filter_stats_test arg (=mcnemar)    which statistical test to use: (mcnemar,chi-square,fisher)
  --filter_chi_smooth arg (=0)          number of balls to add and smooth each window
  --filter_chi_at_least arg (=0)        diff in ratio for bin to cancel - will get change of at least greater than
  --filter_chi_minimal arg (=0)         the minimal number of observations in bin to keep row
  --filter_fisher_smooth arg (=0)       fisher bandwith for division to happend. in ratio change from total_count of no_sig to with_sig [0-1]
Output Options:
  --output_value arg (=-1)              if exists will print stats table for only selected signal value else will print all sorted list
  --output_full_path arg                will only treat if output_value <> NULL. if exist will use to run all and print out all pids data with corersponding
                                        signal in output_value
  --output_debug arg (=0)               If true & output_value!=-1 will output intersetions into file for debuging
```
 
Example Usage can be found here:
```bash
SignalsDependencies --base_config /nas1/Work/Users/Alon/UnitTesting/examples/signalDependency/pregnancy.cfg
```
 
The File config file content (where all parameters may be override with command arguments) is:
**Config File Example**
 Expand source
```ini title="Config File Example"
#The Repository path:
global_rep = /home/Repositories/THIN/thin_jun2017/thin.repository
#A param which controls if to override "global_stats_path" file or use it if exists and save running time:
global_override = 0
#the bining of age
global_age_bin = 5
#the output binary dictionary of the stats to save for faster load in next time (when we want to play with the filtering params)
#global_stats_path = /server/Work/Users/Alon/Models/outputs/dicts/preg_rc_after.dict
global_stats_path = /server/Work/Users/Alon/Models/outputs/dicts/preg_rc_before.new.dict
#registry args:
#each line in registry format looks like: [PID, Start_Date, End_Date, RegistryValue]
#registry can be create on the fly by specifying "registry_init_cmd" or with command:
#created by create_registry --rep $rep_thin --registry_type binary --registry_censor_init "max_repo_date=20170101;start_buffer_duration=365;end_buffer_duration=365;duration=1095;signal_list=RC" --conflicts_method none --registry_init "max_repo_date=20170101;start_buffer_duration=365;end_buffer_duration=365;config_signals_rules=/server/Work/Users/Alon/Models/configs/registry.pregnancy.cfg"  --registry_save /server/Work/Users/Alon/Models/registry/pregnancy.reg
registry_path = /server/Work/Users/Alon/Models/registry/pregnancy.new.reg
#,Hemoglobin,Glucose,LDL,ALT,Creatinine
censoring_registry_args = max_repo_date=20170101;start_buffer_duration=365;end_buffer_duration=365;duration=1095;signal_list=RC
#the signal to fetch and test compared to the registry\samples file
registry_filter_train = 1
labeling_params = label_interaction_mode=0:before_end,after_start|1:before_start,after_start;censor_interaction_mode=all:within,all;conflict_method=all
inc_labeling_params = label_interaction_mode=all:before_end,after_start;censor_interaction_mode=all:within,all;conflict_method=all
#test signal
test_main_signal = RC
#the time window parameters in days:
test_from_window = 30
test_to_window = 720
#some filtering parameters of the output - age- ranges, minimal count of positives, minimal total count for signal...
filter_min_age = 15
filter_max_age = 50
#To filter by gender - 1 for only males, 2 -only females, 3-males and females(default)
filter_gender = 2
filter_positive_cnt = 0
filter_total_cnt = 1000
filter_pval_fdr = 0.05
filter_min_ppv = 0
filter_chi_smooth = 10
filter_chi_minimal = 10
filter_chi_at_least = 0
#whater to bring general stats on all the values, or print specific tables of male,gender with all age-groups for specific readcode\drug value
output_value = -1
```
The output for all values (the example for the pregnancy in time window before the pregnancy read code of at least 1 month till 2 years):
**Output example**
```
read [267598] records on both male and female stats.
Filter male stats - using only females
using mcnemar statistical test
After Filter Age [15 - 50] have 0 keys in males and 137519 keys in females
creating scores vector with size 137519
After total filter has 18095 signal values
After positive filter has 18095 signal values
After positive ratio filter has 18095 signal values
After Hirarchy filter has 11964 signal values
After lifts has 11964 signal values
AfterFDR has 6908 signal values
Signal Chi-Square scores (6908 results):
Index   Signal_Value    Chi-Square_Score        pValue  dof     Count_allBins   Positives_allBins       LiftProb_allBins        Signal_Name
StatRow: 1      287376  196.492 0       7       10324   1434    4.4591  GROUP: IVF      G_8C84.
StatRow: 2      122633  224.836 0       7       3896    847     3.5023  Fertility_counselling_#1        6778.11
StatRow: 3      122614  3430.6  0       7       34254   9975    3.3106  Pre-pregnancy_counselling       676..00
StatRow: 4      106282  1099.49 0       7       30692   5717    3.2144  Fertility_problem       1AZ2.00
StatRow: 5      287372  485.476 0       7       24642   3745    3.1663  GROUP: Treatment_for_infertility        G_8C8..
StatRow: 6      142172  139.051 0       7       7288    1022    3.1596  IVF     8C84.11
StatRow: 7      270286  771.086 0       7       11988   2828    3.1565  GROUP: Fertility_counselling_#1 G_6778.
StatRow: 8      122884  747.336 0       7       11399   2762    3.1528  Pre-conception_advice   67IJ.00
StatRow: 9      270272  3432.34 0       7       39358   10753   3.1124  GROUP: Pre-pregnancy_counselling        G_676..
StatRow: 10     292418  478.115 0       7       11690   2244    3.1101  GROUP: Seen_in_fertility_clinic_#1      G_9N07.
StatRow: 11     262820  147.48  0       7       19118   1796    3.0742  GROUP: Hepatitis_C_antibody_test        G_43X2.
StatRow: 12     268007  1049.69 0       7       13455   3485    3.0688  GROUP: Planning_to_start_family G_6125.
StatRow: 13     289114  459.583 0       7       10729   2171    3.0278  GROUP: Referral_to_fertility_clinic     G_8HTB.
StatRow: 14     122632  547.773 0       7       8122    1988    2.9820  Procreat/fertility_counselling  6778.00
StatRow: 15     342228  111.969 0       7       2130    460     2.7558  GROUP: Advice_relating_to_pregnancy_and_fertility       G_ZG9..
StatRow: 16     120165  124.06  0       6       1852    462     2.6691  Planning_to_start_family        6125.11
StatRow: 17     311447  771.139 0       7       19060   3776    2.6687  GROUP: Subfertility     G_K5Byz
StatRow: 18     255323  2462.54 0       7       86948   14995   2.6330  GROUP: Genitourinary_symptoms_NOS       G_1AZ..
StatRow: 19     142164  286.2   0       7       8664    1608    2.6292  Treatment_for_infertility       8C8..00
StatRow: 20     262814  180.03  0       7       27468   2508    2.5821  GROUP: Hepatitis_antibody_test  G_43X..
StatRow: 21     264801  138.169 0       7       6613    892     2.5780  GROUP: Urine_sex_hormone_titre  G_46J..
StatRow: 22     292409  68976.8 0       7       4769351 359266  2.4232  GROUP: Encounter_administration G_9N...
StatRow: 23     254586  5232.19 0       7       119552  22218   2.4079  GROUP: Last_menstrual_period_-1st_day   G_1513.
StatRow: 24     106283  1515.82 0       7       57061   9796    2.3924  Infertility_problem     1AZ2.11
StatRow: 25     170163  225.844 0       7       8639    1390    2.2657  Missed_miscarriage      L02..11
StatRow: 26     270530  571.406 0       7       18561   3127    2.2606  GROUP: Pre-conception_advice    G_67IJ.
StatRow: 27     254603  487.864 0       7       19694   2774    2.2502  GROUP: Missed_period    G_151I.
StatRow: 28     311873  194.39  0       7       11567   1667    2.2349  GROUP: Bleeding_in_early_pregnancy      G_L10y.
StatRow: 29     122760  280.372 0       7       15156   2331    2.2160  Pregnancy_advice        67A..00
StatRow: 30     311416  1845.72 0       7       78378   13105   2.1946  GROUP: Infertility_-_female     G_K5B..
StatRow: 31     254592  1212.24 0       7       43897   6499    2.1937  GROUP: Menstrual_period_late    G_1517.
StatRow: 32     254233  98.3707 0       7       5035    111     2.1780  GROUP: H/O:_pneumonia   G_14B2.
StatRow: 33     170257  99.7106 0       7       4515    673     2.1447  Inevitable_miscarriage_complete L045.11
StatRow: 34     292563  311.94  0       7       15052   2266    2.1305  GROUP: Seen_by_health_visitor   G_9N23.
StatRow: 35     311867  954.495 0       7       60058   8672    2.0825  GROUP: Haemorrhage_in_early_pregnancy   G_L10..
StatRow: 36     40006   137.015 0       7       30239   192     2.0744  Heart_Disease   Heart_Disease
StatRow: 37     306897  223.302 0       7       19487   196     2.0243  GROUP: Cerebrovascular_disease  G_G6...
StatRow: 38     261609  137.577 0       7       24348   2370    2.0054  GROUP: HIV_antibody/antigen_(Duo)       G_43d5.
StatRow: 39     267999  38651.2 0       7       2959607 274901  2.0043  GROUP: Family_planning  G_61...
StatRow: 40     264551  8138.74 0       7       397242  52412   1.9975  GROUP: Urine_pregnancy_test     G_465..
```
We can see the results are reasonable for pre pregnancy - we see some pre pregnancy tests\vaccinations consults, fertility and IVF treatments... the resutls for the after pregnancy are also reasonables.. you may try it out yourself
 
Example run for printing out specific value 106283 (which is "Infertility_problem"):
```bash
SignalsDependencies --base_config /nas1/Work/Users/Alon/UnitTesting/examples/signalDependency/pregnancy.cfg --output_value 106283
```
And the output (there are some gender problems with the pregancny readcode which needs to be eliminated. Some patients are seen as Males with pregnancy readcode - but small amount.
for example there are 39 males in the age 20-25 which will be pregnant in THIN out of almost 3M males who are in THIN in those years):
```
read [267598] records on both male and female stats.
After Filter Age [15 - 50] have 130079 keys in males and 137519 keys in females
using mcnemar statistical test
Test Signal:106283 - Infertility_problem
Stats for Males
              [NO_SIG&REG_FALSE, NO_SIG&REG_TRUE, SIG&REG_FALSE, SIG&REG_TRUE]
Age_Bin: 15: [1031209,          9,         80,          0] score=    0.00070 [ 0.001%,  0.000%] indep_ratio=0.001%
Age_Bin: 20: [895861,         10,        875,          0] score=    0.00977 [ 0.001%,  0.000%] indep_ratio=0.001%
Age_Bin: 25: [884222,         17,       2739,          0] score=    0.05266 [ 0.002%,  0.000%] indep_ratio=0.002%
Age_Bin: 30: [889268,         28,       4275,          0] score=    0.13460 [ 0.003%,  0.000%] indep_ratio=0.003%
Age_Bin: 35: [867361,         25,       3201,          0] score=    0.09226 [ 0.003%,  0.000%] indep_ratio=0.003%
Age_Bin: 40: [823505,         16,       1631,          0] score=    0.03169 [ 0.002%,  0.000%] indep_ratio=0.002%
Age_Bin: 45: [768280,         13,        597,          1] score=    0.97005 [ 0.002%,  0.167%] indep_ratio=0.002%
Age_Bin: 50: [701062,          9,        230,          0] score=    0.00295 [ 0.001%,  0.000%] indep_ratio=0.001%
Stats for Females
              [NO_SIG&REG_FALSE, NO_SIG&REG_TRUE, SIG&REG_FALSE, SIG&REG_TRUE]
Age_Bin: 15: [1068203,      42935,        764,        162] score=   80.54961 [ 3.864%, 17.495%] indep_ratio=3.875%
Age_Bin: 20: [1200618,     103881,       5911,       1052] score=  154.07719 [ 7.963%, 15.108%] indep_ratio=8.001%
Age_Bin: 25: [1304870,     158141,      12256,       2489] score=  196.26870 [10.809%, 16.880%] indep_ratio=10.870%
Age_Bin: 30: [1251426,     165653,      14471,       3471] score=  338.85030 [11.690%, 19.346%] indep_ratio=11.785%
Age_Bin: 35: [1120124,      92800,       9884,       2144] score=  488.71722 [ 7.651%, 17.825%] indep_ratio=7.751%
Age_Bin: 40: [1028137,      25450,       3439,        450] score=  233.07304 [ 2.416%, 11.571%] indep_ratio=2.449%
Age_Bin: 45: [944238,       2424,        486,         26] score=   22.31869 [ 0.256%,  5.078%] indep_ratio=0.259%
Age_Bin: 50: [857528,        179,         54,          2] score=    1.96521 [ 0.021%,  3.571%] indep_ratio=0.021%
```
We may see that in Females young females 15-20 the Infertility_problem readcode has percentage of 17.495% in the time before pregnancy compared to 3.864% in the females 15-20 that don't have Infertility_problem.
We see that when you have Infertility_problem you are more probable to get pregnant in the future. this population wants to get pregnant in the first place and eventually sucessed  
