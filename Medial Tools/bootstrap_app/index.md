# bootstrap_app
*This is a user manual page. For list of frozen versions and updates see *
**
this is a bootstrap application for running bootstrap (which uses [MedBootstrap](/Infrastructure%20Home%20Page/MedProcessTools%20Library/MedBootstrap) Library). The code is availbe under: $MR_ROOT/Tools/bootstrap_app
**I have also created alias for the bootstrap_app named "bootstrap" so you can simply type "bootstrap --help" or run bootstrap without providing the full path in linux**
 
```
./bootstrap_app --help
```
Program options:
- --help help & exit
- --h help & continue
- --base_config arg config file with all arguments - in CMD we override those settings
- --rep arg the repository if needed for age\gender cohorts
- --input arg the location to read input
- --input_type arg (=samples) the input type (samples,samples_bin,features,medmat_csv,features_csv)
- --output arg the location to write output
- --use_censor arg (=1) if true will use repository censor
- --incidence_file arg the location to load incidence file
- --json_model arg json model for creating features for the filtering of cohorts in bootstrap
- --registry_path arg the registry from_to path to calc accurate incidence by samplings (slower)
- --incidence_sampling_args arg (=start_year=2007;end_year=2014;day_jump=365;conflict_method=all;use_allowed=1)  the init argument string for theMedSamplingAge for the sampling. has default value
- --nbootstrap arg (=500) bootstrap loop count
- --sample_per_pid arg (=1) num of samples to take for each patient. 0 - means take all samples for patient
- --sample_pid_label sample on each pid and label
- --sample_seed arg (=0) seed for bootstrap sampling
- --whitelist_ids_file arg file with whitelist of ids to take
- --blacklist_ids_file arg file with blacklist of ids to remove
- --sample_min_year arg (=-1) used for filtering samples before that year. when sample_min_year < 0 will not filter anything
- --sample_max_year arg (=-1) used for filtering samples after that year. when sample_max_year < 0 will not filter anything
- --cohorts_file arg cohorts definition file
- --do_autosim to do auto simulation - requires min_time,max_time
- --min_time arg min_time for autosim
- --max_time arg max_time for autosim
- --score_resolution arg (=9.99999975e-05) score bin resolution rounding for speed up. put 0 to no rounding
- --score_bins arg (=0) score bin count for speed up. put 0 to no use
- --max_diff_working_point arg (=0.0500000007) the maximal diff in calculated working point to requested working point to put missing value
- --force_score_working_points force using scores as working points
- --working_points_sens arg sens working point - list with "," between each one. in percentage 0-100
- --working_points_fpr arg fpr working point - list with "," between each one. in percentage 0-100
- --working_points_pr arg pr working point - list with "," between each one. in percentage 0-100
- --output_raw flag to output bootstrap filtering of label,score to output
- --use_splits flag to perform split-wise analysis in addition to full_data
- --sim_time_window flag to treat cases as controls which are not in time window and not censor them
- --debug set debuging verbose
 
example run:
 
```bash
bootstrap_app --base_config /nas1/Work/Users/Alon/UnitTesting/examples/bootstrap_app/bootstrap_example.cfg
```
 
 
the bootstrap_example.cfg contains all program arguments in "ini" file format - parameter_name = parameter_value
you may not provide this file or override all parameter with command arguments.
The bootstrap_example.cfg content is:
 
```
#The repository path:
rep = /home/Repositories/THIN/thin_jun2017/thin.repository
#The MedSampels input or if provding other input type we can use input_type paramter
input = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/validation_samples.preds
#where to write output path:
output = /tmp/bootstrap_test
#the json model to create additional features for cohort filtering by cohorts_file
json_model = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/model_stats.json
#the json model content (without the leading "#" before each line):
#{
#   "processes":{
#      "process": {
#         "process_set": "0",
#         "rp_type": "basic_cln",
#         "take_log": "0",
#         "range": "range_min=0.001;range_max=100000",
#         "signal": ["Glucose","HbA1C","BMI"]
#      },
#      "process":{
#         "process_set":"0",
#         "fg_type":"basic",
#         "type":["last","max","last_time"],
#         "window":["win_from=0;win_to=10000"],
#         "time_unit":"Days",
#         "signal":["Glucose","HbA1C","BMI"]
#      }
#   }
#}
#cohorts defintion file:
cohorts_file = /server/Work/Users/Alon/UnitTesting/examples/bootstrap_app/bootstrap_new.params
#The file has those lines (without the leading "#" before each line):
#TimeWindow 0-365 & age 40-80 Time-Window:0,365;Age:40,80
#TimeWindow 0-365 All Ages Time-Window:0,365
#TimeWindow 0-365 with glucose < 110 Time-Window:0,365;Glucose.last.win_0_10000:0,110
##This line will create all the options for time windows: 0-30,30-180,180-365 with ages 40-60,60-80,40-80 for both male,females
#MULTI Time-Window:0,30;Time-Window:30,180;Time-Window:180,365 Age:40,60;Age:60,80;Age:40,80 Gender:1,1;Gender:2,2
```
For exact format of cohorts_file please reffer to [MedBootstrap](/Infrastructure%20Home%20Page/MedProcessTools%20Library/MedBootstrap) wiki page or [doxygen](http://node-04/Libs/html/classMedBootstrap.html#a719ddf45e236146cd0020b0f587b78a1).
 
## Fixing incidence with incidence file
It calculates the average incidence in your cohort based on sex, age group and count of patients in this group. Then to calculate ppv: it multiplies the sensitivity by the incidence - sensitivity* average incidence. it divides it with sensitivity* average incidence + fpr * (1 - average incidence). Equivalent to give this weight for cases: average incidence * total cohort / total casesWeight for control as (1- average incidence)*total cohort / total controls . Sanity test: if model is random, results in sensitivity = fpr, results in ppv = incidenceThe bootstrap program also assesses what would happen to the incidence by other filters of the bootstrap cohort besides (sex, age). For example, taking anemic patients would cause bias toward cases and increase the incidence driven from global population SEER. It assumes that the effect on stratified outcome,age,sex within input samples and the SEER samples(Or generated samples yearly) is the similar - by measuring lift in odds ratio between after applying the bootstrap filters and before the filters.
An example for Incidence file format may be seen here (The file can be created via Flow App):
 
```
head /nas1/Work/Users/Alon/UnitTesting/examples/bootstrap_app/pre2d_incidence_thin.new_format
```
```
AGE_BIN 3
AGE_MIN 21
AGE_MAX 90
OUTCOME_VALUE   0.0
OUTCOME_VALUE   1.0
STATS_ROW       MALE    21      1.0     5242
STATS_ROW       MALE    21      0.0     94758
STATS_ROW       FEMALE  21      1.0     5242
STATS_ROW       FEMALE  21      0.0     94758
STATS_ROW       MALE    24      1.0     5338
```
 
the registry_path is a text format of [MedRegistry](/Infrastructure%20Home%20Page/MedProcessTools%20Library/MedRegistry). look for the code documentation for more info in the write_text_file method.
 
