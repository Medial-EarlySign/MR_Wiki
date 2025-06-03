# Charlson
Json to generate Charlson score.
Path: $MR_ROOT/Projects/Resources/examples/Charlson/charlson.pretify.json
Windows path: %MR_ROOT%\Projects\Resources\examples\Charlson\charlson.pretify.json
 
This is for THIN,  input is DIAGNOSIS signal
****
```json
{
	"model_json_version": "2",
	"serialize_learning_set": "0",
	"model_actions": [
		{
			"action_type": "feat_generator",
			"fg_type": "age"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "MI",
			"sets": "comma_rel:Diseases/MI.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "CHF",
			"sets": "comma_rel:Diseases/CHF.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "PVD",
			"sets": "comma_rel:Diseases/PVD.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "CerebrovascularD",
			"sets": "comma_rel:Diseases/CerebrovascularD.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Dementia",
			"sets": "comma_rel:Diseases/Dementia.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "ChronicPulmD",
			"sets": "comma_rel:Diseases/ChronicPulmD.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "RheumaticD",
			"sets": "comma_rel:Diseases/RheumaticD.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "PepticUlcer",
			"sets": "comma_rel:Diseases/PepticUlcer.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "MildLiver",
			"sets": "comma_rel:Diseases/MildLiver.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "DiabetesNComplx",
			"sets": "comma_rel:Diseases/DiabetesNComplx.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "DiabetesWComplx",
			"sets": "comma_rel:Diseases/DiabetesWComplx.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "XPlegia",
			"sets": "comma_rel:Diseases/XPlegia.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Renal",
			"sets": "comma_rel:Diseases/Renal.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Cancers",
			"sets": "comma_rel:Diseases/Cancers.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "SevereLiver",
			"sets": "comma_rel:Diseases/SevereLiver.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Metastatic",
			"sets": "comma_rel:Diseases/Metastatic.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "HIV",
			"sets": "comma_rel:Diseases/HIV.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Leukemia",
			"sets": "comma_rel:Diseases/Leukemia.list"
		},
		{
			"action_type": "feat_generator",
			"fg_type": "basic",
			"type": "category_set",
			"window": [
				"win_from=0;win_to=18250"
			],
			"time_unit": "Days",
			"signal": "DIAGNOSIS",
			"in_set_name": "Lymphoma",
			"sets": "comma_rel:Diseases/Lymphoma.list"
		},
		//Processings
		{
			"action_type": "fp_set",
			"members": [
				//Age binnings
				{
					"fp_type": "binning",
					"name": "Age",
					"bin_sett": "{bin_cutoffs=49,59,69,79;bin_repr_vals=0,1,2,3,4}",
					"bin_format": "%1.0f",
					"remove_origin": "0",
					"one_hot": "1",
					"keep_original_val": "1"
				},
				//substraction of intersecting conditioins:
				{
					"fp_type": "do_calc",
					"calc_type": "and",
					"source_feature_names": "DiabetesNComplx,DiabetesWComplx",
					"name": "Double_Diabetes"
				},
				{
					"fp_type": "do_calc",
					"calc_type": "and",
					"source_feature_names": "MildLiver,SevereLiver",
					"name": "Double_Liver"
				},
				{
					"fp_type": "do_calc",
					"calc_type": "and",
					"source_feature_names": "Cancers,Metastatic",
					"name": "Double_Cancer"
				}
			]
		},
		{
			"action_type": "feat_processor",
			"fp_type": "do_calc",
			"calc_type": "sum",
			"source_feature_names": "Age.BINNED_1,Age.BINNED_2,Age.BINNED_3,Age.BINNED_4,MI,CHF,PVD,CerebrovascularD,Dementia,ChronicPulmD,RheumaticD,PepticUlcer,MildLiver,SevereLiver,DiabetesNComplx,DiabetesWComplx,XPlegia,Renal,Cancers,HIV,Leukemia,Lymphoma,Double_Diabetes,Double_Liver,Metastatic,Double_Cancer",
			"weights": "1,2,3,4,1,1,1,1,1,1,1,1,1,3,1,2,2,2,2,2,2,6,-1,-1,6,-2",
			"name": "Charlson",
			"duplicate": "0"
		}
	]
}
```
