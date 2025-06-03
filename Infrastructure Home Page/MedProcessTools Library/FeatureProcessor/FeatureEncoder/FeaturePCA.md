# FeaturePCA
example json configuration:
```json
....... 		
	   "process":{
            "process_set":"3",
            "fp_type":"pca",
			"duplicate":"no",
			"pca_top":"10", //Taking top 10 PCA dim
			"subsample_count":"100000"
        },
		"process":{
            "process_set":"4",
            "fp_type":"tags_selector",
			"duplicate":"no",
			"selected_tags":"pca_encoder" //feature selection of the PCA features
        }
......
```
