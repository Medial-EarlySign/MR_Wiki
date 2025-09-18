# Limiting Memory Usage in predict
If you encounter a `bad alloc` error during prediction, you may need to restrict memory usage.
Run `--get_model_preds` with an additional flag:

```bash
Flow --get_model_preds ... --change_model_file ${LIMIT_MEMORY_JSON}
```

Where `LIMIT_MEMORY_JSON` is defined as:
```json
{
  "changes": [
	{
		"change_name":"Decrease mem size",
		"object_type_name":"MedModel",
		"change_command":"max_data_in_mem=100000000"
	}
  ]
}
```

This setting limits the maximum matrix flat array size to 100M float elements (~400 MB).
If out model has 1000 features it will split the predictions into 100K batches.
Keep in mind:

* Actual memory usage can reach up to 2× this value due to temporary duplication.
* Additional constant and object overhead also contributes to memory consumption that are not taking into account in the batch size
* The limit applies specifically to **matrix creation** and **batch processing during prediction**.