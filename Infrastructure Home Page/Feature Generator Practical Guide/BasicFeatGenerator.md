# BasicFeatGenerator
This feature generator is used to create features for most common signals with 1 time channel and for a specific value channel (for example lab test like Hemoglobin). This feature calculate some stats in time window.
It can be last value, mean value, slope, last_time in days of last test, etc.
Here is an example block to define this feature generator - you should put this under "model_actions" element and after all the rep_processors and before feature_processors:
```json
{
	"fg_type": "basic",
	//ELEMENT initialization of BasicFeatGenerator 
}
```
 
Full example on numeric values:
```json
{
	"fg_type": "basic",
	"type": [ "last", "max", "min", "avg", "slope", "last_time", "last2" ],
	"window: [ "win_from=0;win_to=365" ], //defines time window. I used list in here to be able to use this feature generator on multiple features. we can also use seperatly "win_from":"0", "win_to":"365"
	"signal": [ "Hemoglobin", "WBC", "Glucose" ], //The signal to operate on
	"val_channel":"0", //if signal has more than 1 channel (for example BP) we can specify on each value channel to work. Deafult is 0
	"tags": "labs,numeric,need_imputer" //we can specify "tags" for this group of feature to later refer all of them. For example, do imputations for all features with "need_imputer" tag
}
```
Categorical example:
```json
{
	"fg_type": "basic",
	"type": "category_set" , //The operator, can also be category_set_count to store the count
	"window: [ "win_from=0;win_to=365" ], //defines time window. I used list in here to be able to use this feature generator on multiple features. we can also use seperatly "win_from":"0", "win_to":"365"
	"signal": "Drug" , //The signal to operate on
	"val_channel":"0", //if signal has more than 1 channel (for example BP) we can specify on each value channel to work. Deafult is 0
	"sets": "ATC_A10B_A02,ATC_A10B_A01", //defined code or list of codes (comma separated) to construct the "set". You can also refer to codes in file with "comma_rel:$FILE_PATH_OF_CODES"
	"in_set_name": "Diabetes_drug", //Optional argument to give name to this set. Otherwise a default of concatinating codes from "sets" will be created as the name of the feature
	"tags": "categorical" //we can specify "tags" for this group of feature to later refer all of them. For example, do imputations for all features with "need_imputer" tag
}
```
 
 
For full list of arguments, please refer to:
[http://node-04/Libs/html/classBasicFeatGenerator.html#a076e93350e71c367d5a4e4e05c7d2f8e](http://node-04/Libs/html/classBasicFeatGenerator.html#a076e93350e71c367d5a4e4e05c7d2f8e)
 
For full list of "type" params:
[http://node-04/Libs/html/FeatureGenerator_8h.html#a3b295bd15168010bd0cac676528c63a8](http://node-04/Libs/html/FeatureGeneratorh.html#a3b295bd15168010bd0cac676528c63a8)
Here are some common operators/types:
- "last" - take last value in the time window
- "max" - take maximal value
- "last_time" - take last time in days of the test in time window (in days)
- "category_set" - for categorical signal. boolean result. Will test if has value part of "sets" parameter in the defined time window
- "category_set_count" - for categorical signal. numeric result. Will count how many times found a value that is part of "sets" parameter in the defined time window
 
For full json model format refer to [MedModel json format](../MedModel%20json%20format)
