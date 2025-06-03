# Rep Processors Practical Guide
This page intends to list current RepProcessors with explanations on parameters and a json line example.
 
- basic_cln : Basic outlier cleaner : learn ditribution and throw extreme values
- nbrs_outlier_cleaner : Neighborhood outlier cleaner
- [configured_outlier_cleaner ](Cleaners%20Json%20Examples): Configured outlier cleaner - Wrapper for basic_cln  with fixed bounderies for each signal
- [rulebased_outlier_cleaner ](Cleaners%20Json%20Examples): Rule Based outlier cleaner - Rules based on panels (for example BMI) to remove mismatched values in panels
- [calculator ](Rep%20Calculator): virtual signals calculator - Virtual signals calculator - linear sum, log, and more..
- [complete ](Full%20Rep%20Processor): panel completer - Completes signals using panels calculations. searches for signals in exact same time that are relate to calculate (TODO: time window support). for example BMI = Weight/Height^2
- req : check requirement processor
- sim_val : sim val processor  - When signal has more than one value in same time - which one to choose
- signal_rate : signal rate processor - divide signal value by time diff in 2 time channels that describe the signal period
- combine : combine signals processor - combines 2 signals to 1 signal with same name
- split : split signal processor - splits signal by rule for 2 different signals (to apply different rules for example on each split)
- aggregation_period : create periods signal of categorical signals
- basic_range_cleaner : range cleaner
- aggregate : get signals in or out of a given period signal
- [create_registry](#RepProcessorsPracticalGuide-create_registry_rp) : create a virtual signal of a registry to some common medical situations (Diabetes, Hypertension)
- [limit_history](History%20Limit%20repo%20processor) : limit or eliminate signals. Needed mainly as a pre processor
 
## Rep Processors usage in a MedModel
Rep processors are the first elements running in a MedModel run. They are packed into MultiProcessors, each containing 1 or more rep processors. Each such multi processor contains processors allowed to run in parallel to each other, and indeed the MedModel will parallelize those runs. This is true for both learn and apply stages (mainly for learn, as in apply we anyway parallize on the pids records). Hence once defined it is important to pack the processors in the way that allows maximal parallelism.
Example of packing processors when defining them in a json file:
```json
#############################################################################################################################
# new format example
 
"model_json_version": "2",
"serialize_learning_set": "0",
 
# pack all actions (rp, fg, fp) into model_actions
  "model_actions": [
# add a group of first rep processors (will run first and in parallel)
    { "action_type": "rp_set",
      "members": [
        { "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": [ "ALT", "Na" ] }, //Not used in LGI
        { "rp_type": "basic_cln", "type": "iterative", "range": "range_min=0.0001;range_max=10000", "trimming_sd_num": "7","removing_sd_num": "14", "signal": "Hemoglobin"} //USED in LGI
      ]
    },
# add another group (will run after first group and in parallel)
    { "action_type": "rp_set",
      "members": [
        { "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": [ "RBC", "WBC" ] },
        { "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": "Creatinine"}
      ]
    }
 
# continue with your json ...
	]
 
####################################################################################################################
# old format example
  "processes": {
# rep processors in group 0 (running first and in parallel)
	"process" : { "process_set": "0", "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": [ "ALT", "Na" ] },
	"process" : { "process_set": "0", "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": "Hemoglobin" },
#rep processors in group 1 (running after first and in parallel)
	"process" : { "process_set": "1", "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": [ "RBC", "WBC" ] },
	"process" : { "process_set": "1", "rp_type": "basic_cln", "type": "quantile", "range": "range_min=0.100;range_max=6500.000",  "signal": "Creatinine" }
 
# continue with your json ....
}
	
```
 
## Running with a pre processor
The pre processor mechainsm allows one to define new rep processors to be added to a ready model, in order to be run before all the pre processors of the model.
This allows for example limiting the history of a model, or deleting signals in an elegant way when searching for signal importance and minimal requirements. 
A pre processor hence, will typically be one that has an empty learn() and relies only on user given parameters, and is used only at apply time.
The most convenient way to use rep_processors is using a json defining them and the add_pre_processors_json_string_to_model API in MedModel.
Example json:
```json
# example : limiting some signals to tests done at a window of 1 year before prediction time
{
        "pre_processors" : [ {"rp_type" : "history_limit" , "signal" : "ref:signals", "win_from" : "0" , "win_to" : "365"} ] ,
        "signals" : ["Hemoglobin", "MCV", "MCH"]
}
```
 
The Flow App has an option to get predictions of a model with an added pre_processors file. Use the following:
```bash
Flow --rep data.repository --get_model_preds --f_model my.model --f_samples test.samples --f_pre_json pre.json --f_preds output.preds
```
### Create Registy Processor
Creates a registry for the chosen medical condition. Currently implemented are hypertension and diabetes.
- name : "create_registry"
Rough registry definition:
1. Diabetes:
  
1. Diabetes : one of:
    
1. 2 tests within 2y of Glucose above 125, or HbA1C above 6.5 (the second one)  
    
2. 1 test of Glucose above 200, or HbA1C above 8.0
    
3. A diagnostic code
    
4. Starting point of using diabetes drugs.
  
4. PreDiabetes:
    
1. Non Diabetic
    
2. 1 Glucose test above 110, or 1 HbA1C above 5.7
    
3. 2 Glucose tests within 2y above 100 (the second), but still not diabetic.
    
4. Not taking diabetes drugs
  
4. Healthy
    
1. Non Diabetic
    
2. Non PreDiabetic
    
3. Normal range Glucose/HbA1C tests period.
2. HyperTension: 
  
1. 
Example:
```json
    {
      "rp_type":"create_registry",
      "registry":"ht",
      "names":"my_HT_Registry",
	  "ht_systolic_first": "1",
      "ht_drugs":"list_rel:registries/ht_drugs.full",
      "ht_identifiers":"list_rel:registries/ICD10/hyper_tension.2020.desc",
      "chf_identifiers":"list_rel:registries/ICD10/heart_failure_events.2020.desc",
      "mi_identifiers":"list_rel:registries/ICD10/mi.2020.desc",
      "af_identifiers":"list_rel:registries/ICD10/AtrialFibrilatioReadCodes.2020.desc",
      "ht_chf_drugs":"ATC_C03_____",
      "ht_dm_drugs":"ATC_C09A____,ATC_C09C____",
      "ht_extra_drugs":"ATC_C07A_A__,ATC_C07A_B__",
	  "signals":"BP,DIAGNOSIS,Drug,BDATE,_v_DM_Registry"
    },
```
  
2. The code (RepCreateRegistry) uses the following definitions - 
    
1. High blood pressure - Diastolic BP over 90 or Systolic BP over 140 (for people younger than 60) or 150 (for people 60 or older)
    
2. Drugs - Relevant drugs are divided into 4 groups. The first is always indicative of HT. The second is indicative of HT unless there are other indication of CHF. The third indicative of HT unless there are other indicaiton of Diabetes. The last is indicative of HT uless other indications of CHF, Diabetes or MI
  
2. An individual is considered non hyper-tensive, as long as there are no tests showing high blood pressure, no Read (ICD9/10) codes and no drugs indicative of hypertension
  
3. Conditions for HT positive:
    
1. The first appearance of HT diagnosis (note - until 3/3/25 we waited for 2nd indication)
    
2. Two consequtives high BP tests, without normal BP test between them
    
3. Drug indication after high BT test
    
4. Two drug indications, less than 'ht_drugs_gap' days apart
    
5. With just one bad test / drug indication - the status is 'gray' however considered as not HT
  
5. After first HT positive => always HT positive
5. Proteinuria:
  
1. Goes over a list of urine tests
  
2. For the categorial ones: each has the categories that match states of normal, medium, or severe proteinuria.
  
3. For the value based tests : ranges are given for the normal, medium and proteinuria stages.
  
4. The code goes over all the given tests, and in each day there's a test records if it was normal (0) , medium (1) , or severe (2) .
  
5. If there are several tests in the same day, the worst of them is considered as the result to use.
  
6. The output is a DateVal signal with times and values of 0,1,2 matching normal, medium, severe states (note this is DIFFERENT from the 0-4 proteinuria states we used in the past and which are calculated in the Diabetes registries calculator.
6. CKD:
  
1. Goes over eGFR and Proteinuria states and calculates at each time point the CKD state (0-4) based on the last known values of eGFR and Proteinuria.
  
2. In many cases it would be recommended to have a double layered calculation in which:
    
1. Layer 1 creates the virtual signals needed for eGFR and Proteinuria
    
2. Layer 2 calculates the CKD levels based on Layer1 results.
 
 
parameters:
general:
- registry : "dm" for siabetes, "ht" for hypertension
- names : the name/names of the virtual signals created by the processor, these will hold the actual registry signal.
- signals : the signals the rep depends on, in case of working with slightly different signal names than the defaults
  - defaults for dm : "Glucose","HbA1C","Drug","RC"
  - defaults for ht : "BP","RC","Drug","BYEAR","DM_Registry"
  - defaults for proteinuria: all relevant rine tests : "Urine_Microalbumin", "UrineTotalProtein" , "UrineAlbumin" , "Urine_dipstick_for_protein" , "Urinalysis_Protein" , "Urine_Protein_Creatinine" , "UrineAlbumin_over_Creatinine"
  - defaults for ckd : in ckd it is always reccomended to create the proteinuria signal and then use it, see the examples below.
- time_unit : of repository (can rely on default though)
- registry_values : the names of the registry values created in a dictionary (first will be 0, second 1, and on....)
diabetes related:
- dm_drug_sig , dm_diagnoses_sig , dm_glucose_sig , dm_hba1c_sig : the names for the matching signals, defaults are respectively Drug , RC , Glucose , HbA1C
- dm_drug_sets : the drug sets to be used as defining a diabetic patient.
- dm_diagnoses_sets : the set of codes for diabetes
- dm_diagnoses_severity : 3 or 4 : 3 means a diagnoses needs more supporting evidence (such as bad glucose tests) to decided diabetic, 4 means the code is enough on its own.
hypertension related:
- ht_identifiers: Read (ICD9/10) codes for hypertension
- chf_idientifiers, mi_identifiers, af_identifiers: Read (ICD9/10) codes for CHF, MI and AF retrospectively
- ht_drugs: Drugs sets for hyper-tenstion
- ht_chf_drugs, ht_dm_drugs, ht_extra_drugs: Drugs sets for hyper-tension unless there is other indication of CHF, Diabetes and CHF/Diabetes/MI, retrospectively
- ht_drugs_gap: See above for details
proteinuria related:
- urine_tests_categories : a listing of the urine tests to use, each with a bit static if it is numeric or not, and then categories or ranges for the signal for the normal, medium and severe states. 
- Example: 
"**Urine_Microalbumin**:1:0,30:30,300:300,1000000/**UrineTotalProtein**:1:0,0.15:0.15,0.60:0.60,1000000/**UrineAlbumin**:1:0,30:30,300:300,1000000/**Urine_dipstick_for_protein**:0:Urine_dipstick_for_protein_normal:Urine_dipstick_for_protein_medium:Urine_dipstick_for_protein_severe"
- 
Note the usage of the '/' separator between signals, the use of ':' between the five fields for each signal, and the use of ',' within the ranges or categories fields.
ckd related:
- ckd_egfr_sig : the name of the signal holding the eGFR
- ckd_proteinuria : the name of the signal holding the proteinuria signal (the 3 levels one !!!)
 
Json Examples:
```json
#
# creating a diabetes registry
#
{"rp_type": "create_registry", "registry" : "dm", "names" : "_v_DM_Registry",
                          "dm_drug_sets" : "list:/nas1/UsersData/avi/MR/Tools/Registries/Lists/diabetes_drug_codes.full",
                     "dm_diagnoses_sets" : "list:/nas1/UsersData/avi/MR/Tools/Registries/Lists/diabetes_read_codes_registry.full.striped"}
 
#
# creating a hyper tension registry
# It is important to clean and handle simultanous values beforehand
# note that default lists of codes are in $MR_ROOT/Tools/Registries/Lists/
#
{"action_type":"rep_processor","rp_type":"basic_outlier_cleaner","range_min":"0.001","range_max":"100000","val_channel":"0","signal":"BP"},
{"action_type":"rep_processor","rp_type":"basic_outlier_cleaner","range_min":"0.001","range_max":"100000","val_channel":"1","signal":"BP"},
{"action_type":"rep_processor","rp_type":"sim_val","type":"min","signal":"BP"},
{"action_type":"rep_processor","rp_type":"create_registry","registry":"ht","names":"my_HT_Registry"},
#
# creating a proteinuria registry
#
{"action_type":"rep_processor","rp_type":"create_registry","registry":"proteinuria","names":"_v_Proteinuria_State"},
 
#
# creating a CKD registry, note we use the previously defined proteinuria registry
#
{"action_type":"rep_processor","rp_type":"create_registry","registry":"ckd", "names" : "_v_CKD_State" , 
				"signals" : "_v_Proteinuria_State,eGFR_CKD_EPI" ,
                "ckd_egfr_sig" : "eGFR_CKD_EPI" , 
				"ckd_proteinuria_sig" : "_v_Proteinuria_State"},
```
 
 
