# Test 9 - Lab Frequency

**Overview**
One of the major difference between dataset, and health systems, is rate of lab samples. Here we explore lab frequency for the signal behind the important features.
 
**Parameters (see env.sh)**
All parameters are included in env.sh and described in [External Silent Run](http://confluence:8090/display/WIK/External+Silent+Run).
- CMP_FEATURE_RES=... list of important features
****
**What is actually done?**
For every signal relevant to an important feature, create value counts table - how many patients have n labs from this type.
 
**Test Results Review**
Results, separate signal.tsv per relevant signal, are located in signals_cnt 
 
**How to read the results**
It is difficult to learn from the results without a reference. 
