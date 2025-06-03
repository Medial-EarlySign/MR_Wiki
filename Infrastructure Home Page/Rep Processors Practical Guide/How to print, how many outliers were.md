# How to print, how many outliers were
**print_clear_info.json**
```json
{
  "changes": [
       {
                        "change_name":"Turn on verbose cleaning",
                        "object_type_name":"RepBasicOutlierCleaner",
                        "json_query_whitelist": [],
                        "json_query_blacklist": [],
                        "change_command": "print_summary=0.00001;print_summary_critical_cleaned=0.00001",
                        "verbose_level":"2"
           }
     ]
}
```
 
Full flow command that uses this when model is applied:
```bash
Flow --get_model_preds --rep $REP --f_samples $SMAPLES_PATH --f_model $MODEL_PATH --f_preds $OUTPUT_PREDS --change_model_file print_clear_info.json
```
