# Noiser
This rep processor induces random noise into lab signals. 
This is divided into 3 kinds of noise, which can be used in tandem:
1. time_noise (-1<int) - for noise size t, lowers the date by random value sampled from  uniform_int(0, t). 
2. value_noise (0.0<float) - for noise size v, the rep processor first calculates the std of the lab signal across all patients. Then, it adds to each value of this lab a random noise, sampled from gaussian(0, v*std).
3. drop_probability (0.0<float<1.0) - for noise size d, each lab signal will be randomly dropped with probability d.
In addition, one can truncate the resulting values to n digits by using truncation=n - important to truncate, as we are dealing with randomly sampled floats.
In apply_in_test, if 0 it will apply noise in train only. If 1, will apply noise also in test.
 
The rep processor is defined as such:
```json
{ "pre_processors" : [
{
"action_type":"rp_set",
"members":[
{
"rp_type":"noiser",
"truncation":"2",
"time_noise":"_TIME_NOISE_",
"value_noise":"_VALUE_NOISE_",
"drop_probability":"_DROP_NOISE_",
 "apply_in_test":"_ON_APPLY_STR_",
"signal": ["RBC","MPV","Hemoglobin","Hematocrit","MCV","MCH","MCHC-M","Platelets","Neutrophils%","Lymphocytes%","Monocytes%", "WBC","Eosinophils#","Eosinophils%","Basophils%","Basophils#","Neutrophils#","Lymphocytes#","Monocytes#", "RDW"]
} 
]
}
] }
```
 
We are currently using this processor in two capacities.
The first is to take a trained model and apply it on noised data, to see how much the model is sensitive to noise at prediction. This is much cheaper (adjust_model), and is incorporated into the autotests as 15.test_noise_sensitivity_analysis.py (see [Development kit](/Medial%20Tools/Model%20Checklist/AutoTest/Development%20kit)).
The second is to noise a model at training time, to see how much the model is sensitive to noise at training. For this purpose, see U:\Itamar\MR\Projects\Shared\test_noiser\train_experiment\example_experiment. The file create_preds_train.py is a python script calling shell commands, to test crc_model.json in same directory. The trained models and preds subdirectories contain outputs of the test, including analysis for noising just time, just value, or just drop probability. 
