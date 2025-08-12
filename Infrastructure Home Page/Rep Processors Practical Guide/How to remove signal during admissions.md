# How to remove signal during admissions
### Motivation
When the repository includes info from inpatients, we might want to remove lab, measurements and drugs from admission periods, as it might be biased by the temporarily medical situation.
Note that we are likely to keep diagnosis, as we are typically interested in chronic issues.
### Example
In the following example:

- We use**** rep processor
- We have **** signal in the repository
- We set **get_values_in_range** to 0 (will keep just input from inside of timeslots of **ranges_sig_name**) , as default is 1 (outside timeslots)
- We need to define signal appropriate ****
- The **signal_options:**
	- Can have a list of input&output, all of them must have the same ****
	- The default **output_name** is combination of the **signal_name** and **ranges_sig_name** - in this example (if we have not wrote output_name=BP), it would have been BP_ADMISSION. However, keeping the original name is continent when this rep processor is added in the beginning of existing process. 
 
```json
{
	"action_type": "rp_set",
	"members": [
	{
		"rp_type":"basic_range_cleaner",
		"ranges_sig_name":"ADMISSION",
		"time_channel":"0",
		"range_time_channel":"0",
		"get_values_in_range":"0",
		"range_operator":"all",
		"output_type":"T(i),V(s,s)",
		"signal_options": [ 
			"signal_name=BP;output_name=BP"
		]
	}
]}
```
### Remove just from predict
When a model was trained without the need to remove admissions (repository without inpatient data), but we apply the model on a repository with inpatient info, we need to remove admissions before predict, and this pre processor is not integral part of the model.
We would run:
```bash
Flow --get_model_preds --rep $REP --f_model $MODEL --f_samples $SAMPLES --f_preds $PREDS --f_pre_json $REMOVE_ADMISSIONS
```
 where the REMOVE_ADMISSIONS json is as above, covered with
```json
{
"pre_processors":[
add the json here
]
}
```
### Important
The new REMOVE_ADMISSIONS pre-processor should come before the original model pre-processors executed. Otherwise, it might be a problem. For instance, if the original model pre-processors are calculating virtual signal or creating registry, they would use the data during admissions (before the REMOVING). To avoid that, the default in Flow is that the new pre-processor comes first. If, from any reason you want it differently, set the parameter add_rep_processor_first to False.
If we have panel completer in our json, after the basic_range_cleaner, it might 'return' the signal during admission, if we have not cleaned all relevant signals. For instance, removing just Hemoglobin is not enough as the panel completer add it back using other signals.
