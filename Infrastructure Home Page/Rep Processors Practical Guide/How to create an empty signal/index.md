# How to create an empty signal
When a model is trained on repository A and test on repository B, then we might face missing signal.
Example:

- model A: has RDW signal
- model B: do not have RDW signal
 To resolve we adjust the model with the following json
```bash
adjust_model --preProcessors add_empty_signal.json --skip_model_apply 1 --learn_rep_proc 0 --inModel ${IN_MODEL} --out ${OUT_MODEL}
```
 
While add_empty_signal.json is:
```json
{ "pre_processors" : [
   {
      "action_type": "rp_set",
      "members": [
	    {
          "rp_type":"calc_signals",
          "calculator":"empty",
          "names":"RDW",
          "signals":"BDATE" 
      }
      ]
    }
  ]
}
```