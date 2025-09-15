# RepAggregationPeriod
The rep processor will only work on categorical signals.
The rep processor assumes that the input signal has no time range - it only considers the first time channel.
It is a logical rep processor to run before RepBasicRangeCleaner.
rp_type - "aggregation_period". (required)
input_name - the name of the (categorical) signal to process. (required) The obvious choice for this is one of the drug signals, ie "DRUG_PRESCRIBED". 
output_name - the name of the resulting virtual signal.(required)
sets - the set of values that will be considered as a signal. (required) ie "ATC_C03C____" or "ATC_C03C____,ATC_N02A____" note: [ "ATC_C03C____","ATC_N02A____"] (cross product) is not supported.
period - the length of the window to be considered a treatment period - defaults to 0.
time_unit_sig - the signal time unit - defaults to the global_default_windows_time_unit.
time_unit_win - the period time unit - defaults to the global_default_windows_time_unit.
```json
	{
      "action_type": "rep_processor",
	  "rp_type":"aggregation_period",
	  "input_name":"DRUG_PRESCRIBED",
      "output_name":"drugs_sets_period",
	  "sets": ["ATC_C03C____"],
      "period":"43200"
      },
```
 
<img src="/attachments/9765541/9765540.png"/>
 
(Code that tests this rep processor: U:\ReutF\MR\Projects\Shared\check_medication_period_rep_processor)
