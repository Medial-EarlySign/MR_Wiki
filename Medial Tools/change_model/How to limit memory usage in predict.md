# How to limit memory usage in predict
If 'bad alloc' occur in predict, you may need to limit memory usage
Use this flag:
```bash
Flow --get_model_preds ... --change_model_file ${LIMIT_MEMORY_JSON}
```
Where LIMIT_MEMORY_JSON is:
```json
{
  "changes": [
	{
		"change_name":"Decrease mem size",
		"object_type_name":"MedModel",
		"change_command":"max_data_in_mem=1000000000"
	}
  ]
}
```
