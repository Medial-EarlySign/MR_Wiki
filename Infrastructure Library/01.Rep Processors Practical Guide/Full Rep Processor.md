# Full Rep Processor
This Page will describe and demonstrate a full rep processor json with all out capabilities:

- Cleaners - basic and rules
- Panel Compelition
- Common Virtual Signals: for example eGFR
- Registries
 
The json can be found in git under [https://github.com/Medial-EarlySign/AM_Lung/blob/main/configs/training/full_rep_processors.json](https://github.com/Medial-EarlySign/AM_Lung/blob/main/configs/training/full_rep_processors.json)

```json
{
  "model_json_version": "2",
  "serialize_learning_set": "0",
  "model_actions": [
	{
      "action_type": "rp_set",
      "members": [
	    {
          "rp_type":"conf_cln",
		  "conf_file":"../settings/cleanDictionary.csv",
          "time_channel":"0",
		  "clean_method":"confirmed",
		  "signal":"file:../settings/all_rules_sigs.list"
		  //,"verbose_file":"/tmp/cleaning.log"
        },
		{
          "rp_type":"conf_cln",
		  "conf_file":"../settings/cleanDictionary.csv",
          "val_channel":["0", "1"],
		  "clean_method":"confirmed",
		  "signal": ["BP"]
		  //,"verbose_file":"/tmp/cleaning.log"
        }
      ]
    },
	{
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"sim_val",
		  "signal":"file:../settings/all_rules_sigs.list",
		  "type":"first",
          "debug":"0"
		  
        }
		
      ]
    },
    {
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"rule_cln",
		  "addRequiredSignals":"1",
          "time_window":"0",
		  "tolerance":"0.1",
		  "calc_res":"0.1",
		  "rules2Signals":"../settings/ruls2Signals.tsv",
		  "consideredRules":[ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22" ] 
		  //,"verbose_file":"/tmp/panel_cleaning.log"
        }
      ]
    },
	{
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"complete",
		  "sim_val":"remove_diff",
		  "config":"../settings/panel_completer.cfg",
		  "panels":["red_line", "white_line", "platelets", "lipids", "egfr", "bmi", "gcs"]
        }
      ]
    },
	{
      "action_type": "rp_set",
      "members": [
		{
		  "rp_type":"create_registry", 
		  "registry":"dm", 
		  "names":"_v_DM_Registry",
          "dm_drug_sets":"list:../settings/registries/diabetes_drug_codes.full",
          "dm_diagnoses_sets":"list:../settings/registries/diabetes_read_codes_registry.full.striped"
		},
		{
		  "rp_type":"create_registry",
		  "registry":"ht",
		  "names":"my_HT_Registry"
		},
		{
		  "rp_type":"create_registry",
		  "registry":"proteinuria",
		  "names":"_v_Proteinuria_State"
		},
		{
		  "action_type":"rep_processor",
		  "rp_type":"create_registry",
		  "registry":"ckd",
		  "names":"_v_CKD_State",
          "signals":"_v_Proteinuria_State,eGFR_CKD_EPI",
          "ckd_egfr_sig":"eGFR_CKD_EPI",
          "ckd_proteinuria_sig":"_v_Proteinuria_State"
		}
      ]
    }
  ]
}
```
to include use: **$MR_ROOT/Projects/Resources/configs/include_jsons/full_rep_processors.inc.json**
****
**Debug & Print repository after applying rep_processors:**
```bash
#prints signal _v_CKD_State after applying full_rep_processors
Flow --rep /home/Repositories/THIN/thin_2018/thin.repository  --pids_sigs_print_raw  --model_rep_processors $MR_ROOT/Projects/Resources/configs/full_model_jsons/full_rep_processors.json --sigs _v_CKD_State
 
Read 0 signals, 0 pids :: data  0.000GB :: idx  0.000GB :: tot  0.000GB
Read data time 0.126360 seconds
MedModel:: init model from json file [/nas1/UsersData/alon/MR/Projects/Resources/configs/full_model_jsons/full_rep_processors.json]:
read 126 lines from: /nas1/UsersData/alon/MR/Projects/Resources/configs/full_model_jsons/../settings/all_rules_sigs.list
read 126 lines from: /nas1/UsersData/alon/MR/Projects/Resources/configs/full_model_jsons/../settings/all_rules_sigs.list
NOTE: no [predictor] node found in file
MedRepository: read config file /home/Repositories/THIN/thin_2018/thin.repository
MedRepository: reading signals: Urinalysis_Protein,BYEAR,eGFR_CKD_EPI,GENDER,UrineTotalProtein,UrineCreatinine,UrineAlbumin_over_Creatinine,Urine_dipstick_for_protein,Urine_Protein_Creatinine,Urine_Microalbumin,UrineAlbumin,Creatinine,
Read 12 signals, 17030409 pids :: data  0.523GB :: idx  0.205GB :: tot  0.728GB
Read data time 1.730095 seconds
#Print# :: Done processed all 17030409. Took 215.3 Seconds in total
pid     signal_name     description_name        description_value       ...
5000001 _v_CKD_State    Time_ch_0       20111201        Val_ch_0        4
5000002 _v_CKD_State    Time_ch_0       20051206        Val_ch_0        4
5000002 _v_CKD_State    Time_ch_0       20080508        Val_ch_0        4
5000002 _v_CKD_State    Time_ch_0       20120516        Val_ch_0        4
5000003 _v_CKD_State    Time_ch_0       20080630        Val_ch_0        4
5000003 _v_CKD_State    Time_ch_0       20120626        Val_ch_0        4
5000003 _v_CKD_State    Time_ch_0       20131125        Val_ch_0        4
5000003 _v_CKD_State    Time_ch_0       20170531        Val_ch_0        4
5000009 _v_CKD_State    Time_ch_0       20050908        Val_ch_0        4
```
**Debug the changes of rep_processors (for example use cleaner and see before\after):**
```bash
#Compares repository from state after cleaner_path_before  to repository state after cleaner_path
#cleaner_path_before - if empty will compare to repository without rep_processors
Flow --rep /home/Repositories/THIN/thin_2018/thin.repository --rep_processor_print --sigs Hemoglobin --cleaner_path_before "" --cleaner_path $MR_ROOT/Projects/Resources/configs/full_model_jsons/full_rep_processors.json --max_examples 5 --f_output /tmp/repositry_after_rep_processors.log
 
head /tmp/repositry_after_rep_processors.log
EXAMPLE pid     10419961        Signal  Hemoglobin      Time    20050310        Value   14.8    [REMOVED]
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    19961001        Value   12.1
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    19970115        Value   12.4
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    19970519        Value   12.8
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    19981022        Value   12.1
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    20010123        Value   13.7
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    20010831        Value   14.8
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    20011025        Value   14.2
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    20030116        Value   8.9
EXAMPLE pid     21605408        Signal  Hemoglobin      Time    20040528        Value   12.3
...
STATS   Hemoglobin      TOTAL_CNT       30787105        TOTAL_CNT_NON_ZERO      30735288        TOTAL_CLEANED   30464195        CLEAN_PERCENTAGE        1.04885%        CLEAN_NON_ZERO_PERCENTAGE       0.882025%
       TOTAL_PIDS      6168092 PIDS_FILTERED   241868  PIDS_FILTERED_NON_ZEROS 164564  PIDS_FILTER_PERCENTAGE  3.92128%        PIDS_FILTER_PERCENTAGE  2.66799%
```
in the above example we can see 5 examples of patients that has at least 1 change from the original signal - we can see that the hemoglobin value of  10419961 is being filtered.
The last line in output file is summary stats on the signal Hemoglobin compared to the original one.
: 
