# Howto create a signal with constant value
In some cases you want to create "signal" with constant value, for example, Race, all population are "White".
You need to add this block:
```json
{ "pre_processors" : [
  {
    "action_type":"rp_set",
    "members":[
		{
			"rp_type":"calc_signals",
			"calculator":"exists",
			"names":"Race",
			"signals":"MEMBERSHIP",
			"max_time_search_range":"0",
			"signals_time_unit":"Minutes",
			"calculator_init_params":"{in_range_val=1}",
			"unconditional":"0"
		}
	]
  }
] }
```
The input signal in : "signals" should contain signal with "time channel" you can't pass BDATE or GENDER (we might change the code to support this).
the  in_range_val="1" contains the output of the signal, 1 for all records. 
If you want to use this as dictionary, you will need to specify a dictionary with the mapping of the value "1" into the desired string. 
In our example, that we want to generate "Race=White" for all, we will need to add this dict to the repository (TODO: in the future we might configure the dictionary virtually and skip that).
```
SECTION	Race
DEF	1	White
```
and add this dicts to the repository
