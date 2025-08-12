# Iterative Feature Selector
Iterative Selector is a tool for finding important signals (or features), by building predictors iteratielvy (by a greedy bottom up approach or vice versa).
The tool can be found in **$MR_ROOT/Tools/MedProcessUtils/IterativeSelector. **This is an envelope for running the FeatureProcessor iterativeFeatureSelector.
For brevity we will refer to signals or features as signals.
There are two methods for finding  the important signals:
1. Bottom up - Start with a low number of signals (some required signals, or none). In each iteration run on the remaining signals, and add those who improve the selected metric the most (i.e., AUC).
2. Top down - Start with all the signals. In each iteration run on the remaining signals, and remove those who least decrease the selected metric.
 
**Parameters:**

- Input parameters (either inCsv, inBin or inSamples+inModel+config should be given):
    - inCsv: input matrix as csv file.
    - inBin: input matrix as bin file.
    - inSamples: input samples for generating matrix
    - inModel: Bin model file for generating matrix from samples
    - inJson: Json model file for generating matrix from samples (either inModel or inJson should be given with inSamples)
    - rep: Repository config file
    - inpatient: :indicate that relevant data is in-patient data.
- Output parameters
    - out: : output file.
- Selector parameters:
    - predictor: : predictor type (i.e, qrf)
    - predictor_params: : default predictor parameters. in the form of  "param1=value1;param2=value2 " .There is an option to provide a file with "number of features" ranges, and a predictor parameters  string (will be explained later). If the current number of features is not covered in the file (or the file doesn't exist), then this value is used.
    - predictor_params_file:"":input predictor parameters file - if exists, overrides predictor parameters. The file  has one line per number or features range. each line's fomat is "min_number_of_features  max_number_of_features predictors parameter string". Tab  delimited. see example below.
    - nfolds: : if given, replace given splits with id-index%nfolds
    - folds: :comma-separated list of folds to actually take for test. If not given - take all.
    - mode: top2bottom : directions of selection (top2bottom/bottom2top).
    - rate:"50:1,100:2,500:5,5000:10": instruction on rate of selection - comma separated pairs : #-bound:step. Determines how many signals to add or to drop. For example, in the default setting, when working with bottom up, when number of signals is between 1 to 50, the program adds 1 signal each iteration. When number of signals is 51 to100, the program adds 2 signals each iterations, etc. It works symmetrically in top2bottome.
    - univariate_nfeatures: : number of features (not signals!) to select in an initial univariate selector stage.
    - univariate_params:"method=mi": univariate selector parameters.
    - required: comma-separated list of required features.
    - work_on_ftrs:false:if true - work on features, if false, work on signals.
    - verbose: Verbosity flag
    - Performance evealuation is done by MedBootstrap with nbootstrap=0 (written as "loopcnt:0"), looking at the observed measurement:
        - bootstrap_params: Parameters for bootstrap. e.g. sample_per_id=1 ('/' separated)
        - cohort_params: Parameters for defining the booststrap cohort. e.g. Age:50,75/Time-Window:0,365
        - msr_params: Define the performance measurement. e.g. AUC or SENS,FPR,0.2 for Sensitivity at FPR=20%
    - selector_params: iterativeFeatureSelection initialization string (semicolon-separated. Json files format) that replaces all the above parameters
**Example of running line:**
**Running Example**
```bash title="Running Example"
yaron@node-02:/nas1/Work/Users/yaron/Examples/iterativeSelector$ /nas1/UsersData/yaron/MR/Tools/MedProcessUtils/Linux/Release//iterativeSelector --inSamples samples --inJson simple_model.json --out outReport --predictor qrf --predictor_params_file params_iterative_seletcor --nfolds 5 --folds "0,2,4" --mode top2bottom --verbose 1 --msr_params AUC --cohort_params "Age:0,200" --required "Age,Gender"
```
 
**Example for predictor parmeters file:**
(Can be found at /nas1/Work/Users/yaron/Examples/iterativeSelector/params_iterative_seletcor).
0 50 ntrees = 200 ; min_node = 300
51 150 ntrees = 200 ; min_node = 200
151 200 ntrees = 200 ; min_node = 100
201 100000 ntrees = 200 ; min_node = 50
 
**Output Example:**
File can be found at /nas1/Work/Users/yaron/Examples/iterativeSelector/outReport

**Output example**

```txt
Removing family RBC with AUC_Obs = 0.747491
Removing family RDW with AUC_Obs = 0.747476
Removing family INR with AUC_Obs = 0.749214
Removing family PDW with AUC_Obs = 0.751048
Removing family MCV with AUC_Obs = 0.750944
Removing family Hematocrit with AUC_Obs = 0.751496
Removing family WBC with AUC_Obs = 0.751073
Removing family MCHC-M with AUC_Obs = 0.750825
Removing family Hemoglobin with AUC_Obs = 0.752080
Removing family Platelets with AUC_Obs = 0.741643
Removing family MCH with AUC_Obs = 0.688449
```
