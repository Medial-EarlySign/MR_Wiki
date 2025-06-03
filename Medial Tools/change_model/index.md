# change_model
In some cases we need to manipulate Existing MedModel without need for relearn.
For example:
- In production models with use special flags in the BasicCleaner to store in the MedSamples information about the cleaning process
- Normalization, Imputation - we might want to turn it off for some use cases to create matrixes
- ButWhy - we might want to turn it off or change some arguments for the apply without realearn - change grouping arguments for example...
A new app in Tools repository called **change_model** can handle all of those in a very simple manner.
Example for use-case #1 - how to disable the attributes storage in existing model:
```bash
change_model --model_path /server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/crc/base_model.bin --output_path $NEW_CHANGE_MODEL_PATH --interactive_change 0 --search_object_name RepBasicOutlierCleaner --object_command "nrem_attr=;nrem_suff=;ntrim_attr=;ntrim_suff="
read_binary_data_alloc [/server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/crc/base_model.bin] with crc32 [1219618941]
read_from_file [/server/Work/Users/Alon/But_Why/outputs/Stage_B/explainers/crc/base_model.bin] with crc32 [1219618941] and size [5131504]
Found object as RepProcessor
Found object as RepProcessor - touched 20 objects - succesed in 20
```
The above command opens the MedModel in model_path argument, looks for "RepBasicOutlierCleaner" object and passes into all objects the init string command that changes those objects and than stores it in the NEW_CHANGE_MODEL_PATH location.
You can also passed "DELETE" in the object_command to delete a certain objects or interactively navigate trough MedModel object to change/delete certain elements by index numbers.
Be carefull to change only things that won't require relearn!!!
 
## JSON examples of ChangeModelInfo to pass as json
General template:
```json
{ 
  "changes": [
       //Write your change block in here
  ]
}
```
All templates can be seen here: /server/Work/Users/Alon/UnitTesting/examples/ChangeModelInfo/ (symbolic link to git repository /server/UsersData/alon/MR/Projects/Shared/Projects/configs/UnitTesting/examples/ChangeModelInfo)
The json_query_whitelist and json_query_blacklist are lists of conditions to filter the json by regex. If multiple items are presented it does AND condition.
 
Remove Normalizers and Imputers. Remove Only Age+Gender Normalizers and not all of them.
```json
{ 
  "changes": [
       {
			"change_name":"Remove Normalizers",
			"object_type_name":"FeatureNormalizer",
			"json_query_whitelist": [ "Age|Gender" ],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"2"
	   },
	   {
			"change_name":"Remove Imputers",
			"object_type_name":"FeatureImputer",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"2"
	   }
  ]
}
```
Remove attributes from cleaners, remove attribute check and change max_data in memory that used to split model apply into blocks
```json
{ 
  "changes": [
       {
			"change_name":"Remove attributes from cleaners",
			"object_type_name":"RepBasicOutlierCleaner",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "nrem_attr=;ntrim_attr=;nrem_suff=;ntrim_suff=",
			"verbose_level":"1"
	   },
	   {
			"change_name":"Remove attributes Req",
			"object_type_name":"RepCheckReq",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"1"
	   },
	   {
			"change_name":"MedeModel Memory",
			"object_type_name":"MedModel",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "max_data_in_mem=0",
			"verbose_level":"1"
	   }
  ]
}
```
