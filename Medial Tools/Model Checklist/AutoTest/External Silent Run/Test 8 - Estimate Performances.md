# Test 8 - Estimate Performances

# **Overview**
Estimate performance on tested dataset based on matching important factors.
 
**Parameters (see env.sh)**
All parameters are included in env.sh and described in [External Silent Run](http://confluence:8090/display/WIK/External+Silent+Run).
In particular, this test uses:
- REFERENCE_MATRIX=... reference matrix to compare with
- CMP_FEATURE_RES=... list of important features
****
**What is actually done?**
Sample the reference cohort based on the distribution of the important features in the tested dataset, and calculate predicted AUC. Bootstrap the matched reference to estimate accuracy.
 
**Test Results Review**
compare.no_overfitting/summary_table.estimated_performance.tsv gives the bottom line, for example:
<img src="/attachments/13926552/13926554.png"/>
Detailed bootstrap analysis can be found in compare.no_overfitting/bt_reference.estimated.pivot_txt
******How to read the results?**
In the example above, we estimate expected drop in AUC, and maybe more significant, larger confidence interval for the tested data set (column D). To decrease the confidence interval we could decrease the number of important features. That would yield better separation in Test 3 and smaller confidence interval here. However, it is just number games. In the example here, the important features covers ~80% of feature importance in the original model. We don't have yet thumb rule for the right number though.
More work regarding model performance is needed ...
 
