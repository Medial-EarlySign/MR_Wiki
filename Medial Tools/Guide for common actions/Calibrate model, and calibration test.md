# Calibrate model, and calibration test
****: Calibrate a model on one repository, and check calibration on another repository.
****
****
```bash
FilterSamples --filter_train 0 --rep $REP --filter_by_cohort "Time-Window:0,365" --samples $SAMPLES --output $OUTPUT --json_mat $JSON
```
Comments:
- Time Window should be 0 to horizon. Thus, 0,365 means calibrated risk for outcome within 1 year. And 0,730 would mean calibrated risk for outcome within 2 years.
- json_mat is required even though it has no effect (to be removed)
- filter_train default is 1 => take just train. As we set '0' - all samples are taken.
****
****
Standard predict for the samples generated previously.
```bash
Flow --get_model_preds --rep $REP --f_samples $INPUT --f_model $MODEL --f_preds $PREDS_FOR_CALIBRATION 
```
 
****
```bash
adjust_model --postProcessors $JSON --rep $REP --samples $PREDS_FOR_CALIBRATION --inModel $MODEL --skip_model_apply 1 --out $OUTPUT 
```
Comments:
- The OUTPUT is a model with calibration
- The terminal output is 'staircase graph' - bins and calibrated risk (printed on screen and reachable through Flow --print_model_info) 
Output format example:
```
Succesfully added 1 post_processors
Created 44 bins for mapping prediction scores to probabilities
Range: [0.7224, 2147483648.0000] => 1.0000 | 10.77%(107736.000000 / 1000000.000000)
Range: [0.6419, 0.7224] => 0.2500 | 9.98%(99850.000000 / 1000000.000000)
Range: [0.4393, 0.6419] => 0.1123 | 11.70%(116964.000000 / 1000000.000000)
Range: [0.4373, 0.4393] => 0.1000 | 4.30%(43022.000000 / 1000000.000000)
Range: [0.4284, 0.4373] => 0.0889 | 7.88%(78793.000000 / 1000000.000000)
...
```
 
The required JSON is:
```json
{
	"post_processors": [
		{
			"action_type":"post_processor",
			"pp_type":"calibrator",
			"calibration_type":"isotonic_regression",
			"use_p":"0.25"
		}
	]
} 
```
 
****
Run the program:
```bash
TestCalibration --rep ${REP} --tests_file ${TEST} --output ${OUT_PATH}
```
The test file has 3 TAB tokens in each line: samples_path, optional model_path to apply on samples and optional split to filter from samples.
 
****
File with expected risk and actual in validation, for each bin of the calibrated model, e.g., plus some KPIs:
```
probabilty_of_model 	Validation_probabilty  	 cases 	 total_observations 	Diff
0.0000% 	 			0.0000% 	 			 0 	 	 11 	 				0.0000%
0.0046% 	 			0.0062% 	 			 92 	 1493236 	 			0.0016%
0.0103% 	 			0.0096% 	 			 513 	 5329513 	 			0.0007%
0.0158% 	 			0.0184% 	 			 398 	 2166035 	 			0.0026%
 
9.9270% 	 			7.6923% 	 			 2 	     26 	 				2.2347%
10.8825% 	 			2.0000% 	 			 1 	 	 50 	 				8.8825%
tot_diff(L2)=0.001983 prior=0.002349 prior_loss(L2)=0.003845 R2=0.484125 Num_Bins=108 Calibration_Index=0.000890
```
 
And a graph
<img src="/attachments/13403040/13403057.png"/>
 
