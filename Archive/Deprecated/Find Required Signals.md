# Find Required Signals
Find Required Signals is a tool for finding minimal requirement signals. The idea is to find combinations of signals that for a given model achieve a certain performance requirement.
The tool can be found in **MR_Tools/MedProcessUtils/findRequiredSignals** and compiled as part as [AllTools](../../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md)
 
**Algorithm Overview:** 
The algorithm runs over combinations of signals of growing sizes, starting from combinations of size one.
At each combination size, the model runs over different combination sets. For each combination, rep-processors that delete the signals that are not part of the current combination are added, and performance is evaluated.
The number of possible combinations at combination size *k* is generally* number of signals* over *k. *Since this number grows very fast, we limit ourselves with a parameter provided by the user *max_num_tests_per_iter, *and we search only over *n *signals, where *n *is the largest integer so that *n *over *k *is smaller than *max_num_tests_per_iter. *The *n chosen signals *are the best *n *signals from the previous stage.
 
## **Parameters:**

- **Input parameters**
    - model_file::  *.model file.
    - samples_file:: samples file.
    - rep_file:: repository file.
    - bootstrap_json: bootstrap json file
- **Output parameters**
    - out_file:: output file
    - evaluations_to_print:0: Number of evaluations to print in each stage (0 - Only combinations that pass the required performance. 1 - The best result, 2 - The two best results. etc. -1 means print all/
- **Algorithm parameters**
    - req:"BDATE,BYEAR,GENDER": comma-separated list of required signals (signals that are always used).
    - max_num_tests_per_iter:: maximal allowed tests to be done in a iteration. Determines how quick the algorithm finishes. Large number of tests - means that more signals will be checked, but running time will grow. **Recommendation: evaluate it  with a short dummy run**
    - required_ratio: : required performance compared to the full model (either that or required_abs should be entered).
    - required_abs:: absolute required performance (either that or required_ratio should be entered).
    - num_iterations_to_continue:0 :Number of iterations to perform after we get to the required performance.
    - maximal_num_of_signals:666:Maximal number of signals allowed in a required signal set
    - bootstrap_params:sample_per_pid:1: Parameters for bootstrap. e.g. sample_per_id=1 ('/' separated) file")
    - cohort_params:Age:45,120/Time-Window:0,365: Parameters for defining the bootstrap cohort. e.g. Age:50,75/Time-Window:0,365
    - msr_params:AUC: Define the performance measurement. e.g. AUC or SENS,FPR,0.2 for Sensitivity at FPR=20%
    - skip_supersets: true : Whether to skip supersets of acceptable combinations (for example: if signals X,Y are good enough, whether to run on X,Y,Z)
    - delete_signals: : Signals which exists, but never checked (meaning that they are forced to be deleted always).

## **Example: Running Example**

```bash title="Running Example"
findRequiredSignals --model_file example_model.model --samples_file example_samples.samples --rep_file /server/Work/CancerData/Repositories/KP/kp.repository --out_file required_sigs_out.txt --msr_params AUC --max_num_tests_per_iter 1000 --required_ratio 0.95 --evaluations_to_print 0 --num_iterations_to_continue 2 --cohort_params Age:45,80/Time-Window:120,365
```
 
**Output example:**

```txt title="Output example"
Required Performance0.817788
Signals Performance
Smoking_Status 0.82436
ICD9_Diagnosis,Pack_Years 0.823099
WBC,Pack_Years 0.818223
Smoking_Quit_Date,Pack_Years 0.817865
Smoking_Quit_Date,WBC,ICD9_Diagnosis 0.821482
```
 
