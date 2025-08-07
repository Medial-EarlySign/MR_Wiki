# TimeWindowInteraction
This class defines how two time windows interact (boolean result - Yes or No).
**Motivation** - it is being used to decide:
- How to label samples based on registry - given outcome registry time range and prediction time range. return True/False if we should label the sample based on the registry record outcome value.
- Whether or not to censor the sample - given outcome registry time range and prediction time range. return True/False if we should censor the sample
the object is being initialized by [ medial::sampling::init_time_window_mode](https://Medial-EarlySign.github.io/MR_LIBS/namespacemedial_1sampling.html#a964913fff8a3d1352a55f0f40d6d6f12) function.
### the initialization string format
the init strings define the Rules for interaction between sample time window and the registry time window.
this is abstraction of the time windows definitions:
<img src="/attachments/9765361/9765367.png"/>
 
The init string has format of “label_value:Interaction_string|label_value:Interaction_string;…”
Can also use label_value for all labels by specifying “all” or just the numeric value: "0" for controls and "1" for cases.
We can specify diffrent rules for cases/controls
 
 Interaction_string has format of “condition,condition”.
The first condition is for sample from time window interaction with [registry start, registry end]
The first condition is for Sample to time window interaction with [registry start, registry end]
 
Condition is enum with those options:
•“before_start” – condition for time to be before registry start•“after_start” – condition for time to be after registry start•“within” – condition for time to be after registry start and before registry end
 
•“before_end” – condition for time to be before registry end•“all” – no condition, always true
### Examples:
First example - Diseases that occurs once and forever like cancer
full init string: “0:within,within|1:before_start,after_start”
Explain controls rule "within,within": samples should by within registry start to end time (which registry defines time range we mark the patient as sure control). also the from time window of sample/prediction and the end time window of sample/prediction
Explain cases rule "before_start,after_start": sample should start before start_time of registry and finish after start_time of registry. in the registry there meaning for end time only start time = outcome time. there is no end_time for cancer and it's not being used
Second example for vaccination registry (each vaccination holds for X time)
full init string: “0:within,within|1:all,within”
Explain controls rule "within,within": sample time window should be within all time range of unvaccinated period to be counted. can also specify less strict rule by "before_end,after_start" and conlifct_method="max" 
to include controls as patients with some interseciton with sure unvaccinated period and no intersection with vaccination period.
Explain cases rule "all,within": sample time window should finish within registry vaccination period (never mind if started already vaccinated or not vaccinated). can also provide more strict rule by providing 3rd argument
for intersection rate like "all,within,0.5-1.0" to count only samples with at least 50%-100% intersection.
 
 
 
 
