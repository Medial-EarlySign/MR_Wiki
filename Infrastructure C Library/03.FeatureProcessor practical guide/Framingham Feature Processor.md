# Framingham Feature Processor
```json
//Diabetes registry virtual signal (rep processor) to create signal DM_Registry:
{
      "action_type": "rp_set",
      "members": [
		{
		  "rp_type":"create_registry", 
		  "registry":"dm", 
		  "names":"DM_Registry",
		  "dm_diagnoses_sig":"DIAGNOSIS",
          "dm_drug_sets":"list_rel:registries/diabetes_drug_codes.2020.full",
          "dm_diagnoses_sets":"list_rel:registries/diabetes_read_codes_registry.full.striped",
		   "signals":"Glucose,HbA1C,Drug,DIAGNOSIS"
		}
	]
},
 
//Age + Gender input features:
{ "action_type": "feat_generator", "fg_type": "age" },
{ "action_type": "feat_generator", "fg_type": "gender" },
//DM last value:
{
      "action_type":"feat_generator",
            "fg_type":"range",
            "type":"ever",
            "window":"win_from=0;win_to=100000",
            "time_unit":"Days",
            "signal":"DM_Registry",
            "sets":"DM_Registry_Diabetic"
},
//Other signals:
{    "feat_generator":"basic",
    "type": "last",
    "window:  "win_from=0;win_to=1095" ,
    "signal": [ "Cholesterol", "HDL" ], //The signal to operate on
    "val_channel":"0"
},
{    "feat_generator":"basic",
    "type": "last",
    "window:  "win_from=0;win_to=1095" ,
    "signal": [ "BP" ], //The signal to operate on
    "val_channel":["0", "1"]
},
 
{
  "action_type":"fp_set",
  "members": [
    {
		"fp_type":"do_calc",
		"calc_type":"framingham_chd",
		"source_feature_names":"Gender,Age,DM_Registry,Current_Smoker,BP.last.win_0_1095,BP.last.win_0_1095.t0v1,Cholesterol.last.win_0_1095,HDL.last.win_0_1095,Drug.category_set_hypertension_drugs.win_0_1095",
		"name":"Framingham_feature_name"
	}
  ]
}
```
