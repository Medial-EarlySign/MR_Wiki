# How to rename signal
When a model is trained on repository A and test on repository B, then we might face signal naming issue.
Example:

- model A: ICD9_Diagnosis
- model B: DIAGNOSIS
 To resolve we adjust the model with the following json
```bash
adjust_model --preProcessors rename_signal_diag.json --skip_model_apply 1 --learn_rep_proc 0 --inModel ${IN_MODEL} --out ${OUT_MODEL} 
```
While rename_siganl_diag.json is:
```json
{ "pre_processors" : [
   {
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"filter_channels",
		  "signal":"DIAGNOSIS",
		  "output_name":"ICD9_Diagnosis",
		  "signal_type":"T(i),V(i)"
        }
      ]
    }
  ]
}
```
