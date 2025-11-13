# Iterative Feature Selector

The **Iterative Feature Selector** is a powerful tool designed to identify the most impactful signals (or features) within your data. It does this by building a predictive model incrementally, either from the ground up or by eliminating less important signals.
This tool is a standalone wrapper for the `iterativeFeatureSelector` FeatureProcessor, allowing for a more focused and verbose exploration of the feature selection process than is available within a full model pipeline.

### Core Concepts

The tool operates by adding or removing signals based on how they affect a chosen performance metric, such as AUC. 
It defines a **signal** as a collection of related features, which can be selected or removed as a group. 
If you prefer to work on individual features, you can use the `--work_on_ftrs` flag.

There are two main iterative methods:

1.  **Bottom-Up:** Starts with a small set of signals (or none). In each iteration, it tests the remaining signals and adds the one that provides the greatest improvement to the selected metric.
2.  **Top-Down:** Starts with all available signals. In each iteration, it tests the remaining signals and removes the one that causes the least decrease in the selected metric.

 
### Command Line Arguments

The following parameters control the tool's behavior.

#### Input Data
You must provide data using one of the following methods:

* `--inCsv <path>`: A single CSV file containing your data matrix.
* `--inSamples <path>` + `--inModel <path>`/`--inJson <path>`: The tool will generate the data matrix from raw samples using an existing model file.
* `--rep <path>`: The configuration file for the data repository for generating the matrix from inSamples

#### Output

* `--progress_file_path`: Path for progress output file log that you can track and see performance not only in terminal and wait for program to finish.
* `--out <path>`: The path for the output file, which will contain the selection report.

#### Selector Parameters

* `--mode <top2bottom | bottom2top>`: The direction of the selection process. Default is `bottom2top`.
* `--predictor <type>`: The type of predictor to use in the selection loop (e.g., `xgb`).
* `--predictor_params "<key1=value1;...>"`: A semicolon-separated string of default parameters for your predictor.
* `--predictor_params_file <path>`: A file that specifies predictor parameters based on the number of features. Each line should be tab-delimited with the format: `min_features max_features predictor_param_string`. This file overrides `--predictor_params`.
* `--rate "<rate_string>"`: Defines the number of signals to add or remove in each iteration. The format is a comma-separated list of `bound:step` pairs. For example, `"50:1,100:2"` means add/remove 1 signal when the count is between 1-50, and 2 when it's between 51-100.
* `--required <signal1,signal2,...>`: A comma-separated list of signals that must be included in the model from the start.
* `--work_on_ftrs <boolean>`: If `true`, the selector operates on individual features instead of entire signals. Default is `false`.
* `--group_mode`: Controls the features grouping. Can be a file path with feature to group name for full control or keyword like `BY_SIGNAL_CATEG` that aggregates features by their originating source signal
* `--numToSelect`: stop criteria when to stop. The default is 0. Continue till the end.

#### Performance Evaluation
The tool uses a bootstrap method for performance evaluation.

* `--msr_params <param_string>`: Defines the performance metric. For example, `AUC` or `SENS,FPR,0.2`.
* `--nfolds <number>`: Replaces existing data splits with new folds for cross-validation.
* `--folds <0,2,4>`: A comma-separated list of folds to use for evaluation. If not provided, all folds are used.
* `--verbose <level>`: Controls the level of detail printed to the console.
*  `--bootstrap_params <param_string>`: Parameters for bootstrap. e.g. sample_per_id=1 ('/' separated, key value is separated by ":"). example: "loopcnt:500/sample_per_id:1"
* `--cohort_params <param_string>`: Parameters for defining the booststrap cohort. e.g. "Age:50,75/Time-Window:0,365" for filtering the samples

### Running Example

This command runs a top-down iterative selection process, removing signals that have the least impact on AUC.
Age,Gender are required and forced to remain in the model

```bash title="Running Example"
iterativeSelector --inSamples samples --inJson simple_model.json --out outReport --predictor qrf --predictor_params_file params_iterative_seletcor --nfolds 5 --folds "0,2,4" --mode top2bottom --verbose 1 --msr_params AUC --required "Age,Gender"
```

* `--predictor`: Uses a `qrf` (Quantile Random Forest) predictor.
* `--predictor_params_file`: Loads specific predictor parameters from a file based on the number of features.
* `--nfolds` and `--folds`: Specifies that the evaluation should use 5 folds, but only folds 0, 2, and 4 will be used for testing.
* `--mode top2bottom`: Starts with all signals and removes them one by one.
* `--required`: Ensures Age and Gender are never removed from the model.
 
### Example: Predictor Parameters File

The `predictor_params_file` allows you to change predictor parameters as the number of features changes. Each line is tab-delimited.

```text
0 50 ntrees = 200 ; min_node = 300
51 150 ntrees = 200 ; min_node = 200
151 200 ntrees = 200 ; min_node = 100
201 100000 ntrees = 200 ; min_node = 50
```

### Output Example

The tool provides a verbose output, detailing the changes at each step. 
In this Top-Down example, the tool is showing which signal it is removing and the corresponding AUC of the model after the removal.

```text
Removing family RBC with AUC_Obs = 0.747491
Removing family RDW with AUC_Obs = 0.747476
Removing family INR with AUC_Obs = 0.749214
Removing family PDW with AUC_Obs = 0.751048
Removing family MCV with AUC_Obs = 0.750944
Removing family Hematocrit with AUC_Obs = 0.751496
Removing family WBC with AUC_Obs = 0.751073
...
Removing family MCHC-M with AUC_Obs = 0.750825
Removing family Hemoglobin with AUC_Obs = 0.752080
Removing family Platelets with AUC_Obs = 0.741643
Removing family MCH with AUC_Obs = 0.688449
```
