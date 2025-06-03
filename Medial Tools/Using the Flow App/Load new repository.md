# Load new repository
```bash
Flow --rep_create --convert_conf $PATH_TO_CONFIG_FILE --load_err_file $OPTIONAL_FILE_PATH_TO_STORE_ERRORS 
#optional argument to controls thresholds to "fail" load process when encounter errors --load_args "check_for_error_pid_cnt=0;allowed_missing_pids_from_forced_ratio=0.05;max_bad_line_ratio=0.05;allowed_unknown_catgory_cnt=50"
```
 
Generate reverse index - should be done after succefull load:
```bash
Flow --rep_create_pids --rep $REPOSITORY_PATH
```
 
# Explain about load_config_file
File delimeted settings.
Those are the settings:
- DESCRIPTION - a line that describes the repository and ignored
- RELATIVE - if 1 will use relative paths (please keep this 1)
- SAFE_MODE - if 1 will fail on each critical error and won't continue (please keep this 1)
- MODE - please provide 3
- 
PREFIX - What is the prefix of the file names that will be stored under OUTDIR path directory for "data" files. Just a convention, need to select something
- CONFIG - output path file name to "repository" config file that contains all dictionaries, signals file - similar to this loading config, but without the path to the raw files
- SIGNAL - path to signals file definitions ([Signal file format](/Repositories/Signal/Repository%20Signals%20file%20format))
- FORCE_SIGNALS - list of signals that are required for a paitient. If they are missing the patient is dropped. We usually use BYEAR and GENDER
- DIR - path for config files to copy from the signals file, repository config file and search for data files (if relatively is turned on)
- OUTDIR - where to store repository
- DICTIONARY - path to used dictionary for the repository and also for parsing data files with categorical data
- DATA - path to data file
- LOAD_ONLY - optional argument to specify list of specific signals to load, the rest are ignored (not deleted from repository if exists). It is useful when fixing specific signal or signals, otherwise it will delete the other signals. For example LOAD_ONLY RBC,Glucose
 
Example:
 
**Example file**
```
#Example file - comments can start with "#" and are ignored
 
DESCRIPTION     THIN18 data - full version
RELATIVE        1
SAFE_MODE       1
MODE    3
PREFIX  data/thin_rep
CONFIG  thin.repository
SIGNAL  thin.signals
FORCE_SIGNAL    GENDER,BYEAR
DIR     /nas1/Temp/Thin_2018_Loading/rep_configs
OUTDIR  /nas1/Work/CancerData/Repositories/THIN/thin_2018_2
DICTIONARY      dicts/dict.drugs_defs
DICTIONARY      dicts/dict.bnf_defs
DATA    ../demo2/GENDER
DATA    ../demo2/BYEAR
DATA    ../demo2/BDATE
```
 
```
 
```
 
 
 
# Explain about loading file format:
The loading data files are in TAB delimeted and the columns are (no header):
- patient id
- signal name
- time_channel_0_value
- ...
- time_channel_i_value
- val_channel_0_value
- ......
- val_channel_i_value
- Any additional columns are ignored
General commnets:
- A single file can contain multiple signals - different value in column s "signal name".
- The rows should be sorted by patient id and first time channel if the signal has time channels
- The time channels and value channels that will be used, will be determined by the signal type. For example, if out singal has 2 time channels and 1 value channel. Columns 3-4 will be time channels and column 5 will be value. The rest are ignored
- If the value column is categorical - the column can be used as string. We will need to define a suitable dictionary toi convert those values to numerics. Please don't use spaces in the strings (confusing) and use "_" instead
Example:
**Blood pressure signal (1 time channel, 2 value channels, the rest are ignored. They exists for debugging)**
 Expand source
```
5000001 BP 20030324 60.0 100.0 246..00-1005010500 null value
5000001 BP 20061218 60.0 90.0 246..00-1005010500 null value
5000001 BP 20071008 60.0 90.0 246..00-1005010500 null value
5000001 BP 20090309 60.0 90.0 246..00-1005010500 null value
5000001 BP 20100802 60.0 90.0 246..00-1005010500 null value
5000001 BP 20120125 67.0 90.0 246..00-1005010500 null value
```
