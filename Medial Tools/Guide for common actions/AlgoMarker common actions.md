# AlgoMarker common actions
How to list all Rules outliers
```bash
Flow --print_model_info --f_model $MODEL_PATH 2>&1  | egrep "RepRuleBasedOutlierCleaner|BasicOutlierCleaner"
```
How to list all Outliers bounds:
```bash
Flow --print_model_info --f_model $MODEL_PATH 2>&1 | grep BasicOutlierCleaner | grep -v "FeatureBasicOutlierCleaner"
```
 
Print model used signals + categories (some of the signals can turned to be virtual if not exists - for example BMI):
```bash
Flow --print_model_sig --f_model $MODEL_PATH 
```
