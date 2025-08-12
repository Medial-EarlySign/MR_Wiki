# History Limit repo processor
A rep processor that allows to limit the history of a signal to a given time range relative to the prediction time point.
There is also an option to virtually erase the signal completely so when the model will try to access the signal it will be empty.
Mainly used as a [pre processor](/Medial%20Tools/Using%20the%20Flow%20App/Using%20Pre%20Processors.html) in model apply to see how history impact performance.

- name : "limit_history" or "history_limit"
parameters:
- signal - signal name
time_channel - the time channel to limit by
- win_from , win_to - the time window to select
- delete_sig : if 1 : delete the signal from record.
- rep_time_unit , win_time_unit : global by default, otherwise as stated.
Example json lines:
```json
# limit Hemoglobin and Creatinine to tests done up to one year before the prediction time
{"rp_type" : "history_limit" , "signal" : ["Hemoglobin" , "Creatinine"] , "win_from" : "0" , "win_to" : "365"}
 
# delete GENDER and Hemoglobin signals from each record
{"rp_type" : "history_limit" , "signal" : ["GENDER", "Hemoglobin"], "delete_sig" : "1" }
 
```
Example as pre processor:
A pre processor json file that limits history for RDW:
 
```json
{
        "pre_processors" : [ {"rp_type" : "history_limit" , "signal" : ["RDW"], "win_from" : "0" , "win_to" : "365"} ] ,
}
```
