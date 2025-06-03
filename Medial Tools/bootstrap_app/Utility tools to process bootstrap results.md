# Utility tools to process bootstrap results
 
# Process bootstrap result to create text table (Excel like):
You can use bootstrap_format.py to process the results into nice table.
The script is under "[MR_SCRIPTS](http://bitbucket:7990/projects/MED/repos/mr_scripts/browse)" git repo and suppose to be in your PATH under $MR_ROOT/Projects/Scripts/Python-scripts, so you can just call it.
```bash
bootstrap_format.py --report_path $BT_REPORT_PATH_1 $BT_REPORT_PATH_2 $BT_REPORT_PATH_3 ... $BT_REPORT_PATH_N \
  --report_name $NAME_FOR_1 $NAME_FOR_2 $NAME_FOR_3 ... $NAME_FOR_N \
  --cohorts_list $REGEX_TO_FILTER_COHORTS_FORM_BOOTSTRAP \
  --measure_regex $REGEX_TO_FILTER_MEASUREMENTS
  --table_format $TABLE_FORMAT
#Full example:
bootstrap_format.py --report_path /tmp/bt_baseline.pivot_txt /tmp/bt_full.pivot_txt --report_name baseline MES_Full --cohorts_list . --measure_regex "AUC|OR@PR" --table_format "cm,r"
```
- You can specify 1 or multiple bootstrap file results and give each file a name.
- You can filter the cohorts using regex "–cohorts_list" argument or pass "–cohorts_list ." to keep all cohorts (. will match all characters in regex)
- You can specify which measurements to extract with "–measure_regex". For example "AUC|SENS@FPR" - to extract both AUC and SENS@FPR
- The final output is a table and you can control the rows/columns with "table_format" argument. There are 3 dimensions that are being projected into 2D table. Here are the letters that describe each one of them
  - r - "report". The bootstrap report file. In the example it's either baseline or MES_Full 
  - c - "cohort". The bootstrap files can contain multiple cohorts
  - m - "measurement" - The bootstrap results is based on multiple measurements, like "AUC", "SENS@FPR_05", etc.
In order to control how to project those 3 dimensions into row/cols (2D), you need to specify those 3 characters and put "," to separate rows and cols. The first token will control "rows" of the table and the second token will controls the "columns".As you can see, one of the tokens will have 2 characters - it will expend all possible combinations of those values (Cartesian multiplier) and use a delimiter of "$" between the 2 tokens. In the example, The rows will be based on "cohort" X "Measurement" and the columns will be the 2 reports - so we will see side by side the baseline VS MES_Full in this example
Additional arguments:
- --break_cols "breaks" Cohort filters into columns by comma - each filter condition is separated by comma.
- --break_mes "breaks" measurement values (e.g. 8.4[7.8 - 9.2]) to 3 columns - Mean, Min and Max
- --output_path to save the results in csv
Full output example without "--break_cols":
****
 Expand source
```
Cohort$Measurements     baseline        MES_Full
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$AUC        0.807[0.801 - 0.814]    0.816[0.809 - 0.822]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$OR@PR_3    8.4[7.8 - 9.2]  9.5[8.7 - 10.3]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$OR@PR_5    8.1[7.6 - 8.7]  8.8[8.2 - 9.4]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000$OR@PR_10   7.6[7.2 - 8.2]  8.3[7.7 - 8.8]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000$AUC        0.812[0.805 - 0.818]    0.821[0.815 - 0.827]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000$OR@PR_3    9.2[8.5 - 9.9]  10.1[9.4 - 11.0]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000$OR@PR_5    8.4[7.8 - 9.0]  9.4[8.7 - 10.1]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000$OR@PR_10   8.0[7.5 - 8.6]  8.7[8.1 - 9.2]
```
With "–break_cols" (which is the default):
****
 Expand source
```
Cohort  Age     Ex_or_Current   Suspected       Time-Window     Measurements    baseline        MES_Full
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000    50-80   1       0       90-360  AUC     0.807[0.801 - 0.814]    0.816[0.809 - 0.822]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000    50-80   1       0       90-360  OR@PR_3 8.4[7.8 - 9.2]  9.5[8.7 - 10.3]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000    50-80   1       0       90-360  OR@PR_5 8.1[7.6 - 8.7]  8.8[8.2 - 9.4]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-0.000,Ex_or_Current:1.000-1.000    50-80   1       0       90-360  OR@PR_10        7.6[7.2 - 8.2]  8.3[7.7 - 8.8]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000    50-80   1       0-1     90-360  AUC     0.812[0.805 - 0.818]    0.821[0.815 - 0.827]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000    50-80   1       0-1     90-360  OR@PR_3 9.2[8.5 - 9.9]  10.1[9.4 - 11.0]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000    50-80   1       0-1     90-360  OR@PR_5 8.4[7.8 - 9.0]  9.4[8.7 - 10.1]
Time-Window:90.000-360.000,Age:50.000-80.000,Suspected:0.000-1.000,Ex_or_Current:1.000-1.000    50-80   1       0-1     90-360  OR@PR_10        8.0[7.5 - 8.6]  8.7[8.1 - 9.2]
```
 
How to generate graphs like ROC from bootstrap results file:
Please use plt_bt.py in scripts.
```bash
plt_bt.py --input $BT_REPORT_PATH_2 $BT_REPORT_PATH_3 ... $BT_REPORT_PATH_N \        
  --names NAMES  $NAME_FOR_1 $NAME_FOR_2 $NAME_FOR_3 ... $NAME_FOR_N \     
  --output $OUTPUT_PATH \
  --measure $MEASURE
  --filter_cohorts $REGEX_TO_FILTER_COHORTS_FORM_BOOTSTRAP
  --show_ci 1
  --add_y_eq_x 1  #If true will add y=x graph
```
measure for ROC for example is SENS@FPR
