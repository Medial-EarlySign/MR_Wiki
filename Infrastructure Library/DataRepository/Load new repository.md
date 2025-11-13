# Loading a New Repository

## Best Practices

* **Keep it Simple**: Load signals with minimal preprocessing. Handle outliers and clean data within the model itself, not during the ETL stage. This approach simplifies implementation, reduces ETL errors, and results in a more robust model. Future implementations will be easier with a straightforward ETL process.
* Ensure that all signals are in the correct units - each signal is expected to use the appropriate measurement unit.
* It is recommended to separate your code into two parts:
    - Code for fetching the data  
    - Code for processing the data  

  This makes the code easier to read and helps clarify what minimal processing was applied to each signal.

You can use your own tools and methods to create “loading files” (described below), or use our ETL tool to both build the ETL process and test the results.  
More details here: [ETL Tool](../../Tutorials/01.ETL%20Tutorial)
You can start from this [code example](https://github.com/Medial-EarlySign/MR_Tools/tree/main/RepoLoadUtils/common/ETL_Infra/examples/simple_test_pipeline) and change it for your own needs

Steps to create loading files on your own:

## Step 1: Prepare Load Files:
In this step you will need to create ETL loading files for each signal.

### Data File Format

- Files are TAB-delimited, **no header**.
- Columns:
  1. Patient ID
  2. Signal name
  3. Time channel 0 value
  4. ...
  5. Time channel *i* value
  6. Value channel 0 value
  7. ...
  8. Value channel *i* value
  9. Any additional columns are ignored

**Notes:**

- A single file can contain multiple signals (different values in the "signal name" column).
- Rows should be sorted by patient ID and the first time channel (if present).
- The number of time/value channels used depends on the signal definition.
- For categorical value columns, use strings without spaces (use underscores `_` instead). A suitable dictionary is required for conversion to numeric values.

### Example: Blood Pressure Signal

(1 time channel, 2 value channels; extra columns are ignored)

```
5000001 BP 20030324 60.0 100.0 246..00-1005010500 null value
5000001 BP 20061218 60.0 90.0 246..00-1005010500 null value
5000001 BP 20071008 60.0 90.0 246..00-1005010500 null value
5000001 BP 20090309 60.0 90.0 246..00-1005010500 null value
5000001 BP 20100802 60.0 90.0 246..00-1005010500 null value
5000001 BP 20120125 67.0 90.0 246..00-1005010500
```

## Step 2: Prepare Configuration file `load_config_file`

The configuration file uses a delimited format with the following settings:

- **DESCRIPTION**: Description of the repository (ignored by loader)
- **RELATIVE**: Use relative paths (set to 1)
- **SAFE_MODE**: If 1, stops on critical errors (set to 1)
- **MODE**: Use value 3
- **PREFIX**: Prefix for data file names stored in OUTDIR
- **CONFIG**: Output path for the repository config file (contains dictionaries, signals, etc.)
- **SIGNAL**: Path to signal definitions ([Signal file format](Repository%20Signals%20file%20format.md))
- **FORCE_SIGNALS**: Comma-separated list of required signals (e.g., BYEAR,GENDER); patients missing these are dropped
- **DIR**: Path for config files and data files (relative if RELATIVE=1)
- **OUTDIR**: Output directory for the repository
- **DICTIONARY**: Path(s) to dictionary files for categorical data
- **DATA**: Path(s) to data files
- **LOAD_ONLY**: (Optional) Comma-separated list of signals to load; others are ignored (useful for partial updates)

### Example Configuration File

```
# Example file - lines starting with "#" are comments
DESCRIPTION     THIN18 data - full version
RELATIVE        1
SAFE_MODE       1
MODE            3
PREFIX          data/thin_rep
CONFIG          thin.repository
SIGNAL          thin.signals
FORCE_SIGNALS   GENDER,BYEAR
DIR             /nas1/Temp/Thin_2018_Loading/rep_configs
OUTDIR          /nas1/Work/CancerData/Repositories/THIN/thin_2018_2
DICTIONARY      dicts/dict.drugs_defs
DICTIONARY      dicts/dict.bnf_defs
DATA            ../demo2/GENDER
DATA            ../demo2/BYEAR
DATA            ../demo2/BDATE
```

After you have completed and prepered all loading files please execute:

---

## Step 3: Load the Repository

```bash
Flow --rep_create --convert_conf $PATH_TO_CONFIG_FILE --load_err_file $OPTIONAL_FILE_PATH_TO_STORE_ERRORS
# Optional: Control error thresholds with --load_args, e.g.:
# --load_args "check_for_error_pid_cnt=0;allowed_missing_pids_from_forced_ratio=0.05;max_bad_line_ratio=0.05;allowed_unknown_catgory_cnt=50"
```

## Step 4: Generate Reverse Index

After a successful load, generate the reverse index:

```bash
Flow --rep_create_pids --rep $REPOSITORY_PATH
```


