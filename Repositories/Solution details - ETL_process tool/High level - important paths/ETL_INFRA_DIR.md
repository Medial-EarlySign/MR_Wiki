# ETL_INFRA_DIR
The git repository of tools, can be found under $MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra.
It's standalone and can be copies to remote machine and work, no external dependencies.

- FILE - **etl_process.py** - The main file to import as python module to your specific ETL code by calling "from etl_process import *" after adding the ETL_INFRA_DIR into the path by using sys.insert(0, ETL_INFRA_DIR).
- FOLDER - **dicts** - contains dictionaries from known medical ontologies and their mapping between each other. It's just a resource for the usage of the infrastructure. Edit this folder only if you want to update the global dictionaries/mappings for all future work.
- FOLDER - **examples ** - contains examples for loading process in several repository. The THIN example is fully implemented.** **
- FOLDER - **rep_signals** - contains global information about known/standard signals. The definitions can be override in your specific ETL code, but this is a "start" that in almost all cases, can and should remain as is. Edit this folder only if you want to update the signal definitions for all future work.
    - FILE - **general.signals** - signals file with definitions of all known/standard signals - type of each signal, unit, is categorical, "tags" etc. Note that "Tags" sets the processing logic and tests to be executed for each signal. For instance, signal "Hemoglobin" has two tags - "labs, cbc":
        - For uploading the signal, the most specific code would be used - Hemoglobin.py if exists, else labs.cy if exists, else cbc.py if exist, else new code is needed.
        - For tests, all existing tests under hemoglobin, labs and cbc will be executed.
File format is the same as in in the repository and described here: [Repository Signals file format](../../Repository%20Signals%20file%20format.md). When adding a new lab signal here, do not forget adding quantiles values in the next file.  - FILE - **signals_prctile.cfg **- A file that contains quantile information for each and every signal from general.signals. Quantile information are tested for all labs signals.
    - FILE - **lab_zero_value_allowed.txt** - list of signals that are allowed to have 0-value. If 0-value are not allowed, above defined rate (see labs/test_no_nulls.py), an error is raised. 
- FOLDER - **tests** - when loading a signal, the ETL process tests signal's structure according to its definitions - does the signal have all the time channels, and/or values channels? does input type (e.g. numeric) match the definitions? This folder contains additional specific tests.
    - FOLDER - **TAG_NAME** (e.g. "labs"). Each file inside the folder is a different test. Every test will be executed for all signal with the tag. For guide on how to write/add tests see [ETL_process dynamic testing of signals](../Howto%20guide%20to%20some%20ETL%20elements/ETL_process%20dynamic%20testing%20of%20signals.md) . 
- FOLDER - **data_fetcher** - A library folder with helper functions for the parsing phase. The parsing process data from database or files, and as example for an helper, is a function for batching of large files/databases. For guide on how to write parser using this library see [Data Fetcher](../Howto%20guide%20to%20some%20ETL%20elements/Data%20Fetcher.md)
 
