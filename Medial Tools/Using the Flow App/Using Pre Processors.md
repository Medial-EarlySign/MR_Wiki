# Using Pre Processors

Given a trained model , one may need to apply some additional rep processors before the model is applied. 

A classical example is : the model was trained without history limits on the signals, and one needs to test the results when limiting the signals (or some of them) to say only 1 year of history.

The way to do that is add a pre processor at apply time to the model.

This can be done using the Flow --get_model_preds option and adding the pre processors using the --f_pre_json parameter

 

Example:

A pre processor json file that limits histrory:

```

{

        "pre_processors" : [ {"rp_type" : "history_limit" , "signal" : "ref:signals", "win_from" : "0" , "win_to" : "365"} ] ,

        "signals" : ["Hemoglobin", "MCV", "MCH"]

}

```

 

A Flow get prediction example using pre processors

```

Flow --get_model_preds --rep myrep.repository --f_samples test.samples --f_model trained.model --f_preds out.preds --f_pre_json pre.json

```

