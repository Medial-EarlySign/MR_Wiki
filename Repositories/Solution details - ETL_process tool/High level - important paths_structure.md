# High level - important paths/structure
## The ETL file structure:
- [ETL_INFRA_DIR ](High%20level%20-%20important%20paths/structure/ETL_INFRA_DIR)- directory containing the ETL infrastructure, currently located at "$MR_ROOT\Tools\RepoLoadUtils\common\ETL_Infra". It can be copied to a remote machine and is standalone, meaning no other files are required to utilize the infrastructure.  
- [CODE_DIR ](High%20level%20-%20important%20paths/structure/CODE_DIR)-  directory designated for writing a specific ETL code
- [WORK_DIR ](High%20level%20-%20important%20paths/structure/WORK_DIR)- output directory
Click on each part to understand its structure, important files, and more details.
## What happens in the ETL:
1. 
The CODE_DIR must have load.py file to manage the loading process. This script runs several instances of the prepare_final_signals function (see [ETL Manager Process](ETL%20Tutorial/ETL%20Manager%20Process)) - each initiates a "parser" to connect raw data to a "processing unit" (split into batches, when necessary).
2. In general, prepare_final_signals checks the status of the required signal:
  
1. If override is specified in the call - load the signal from the start.
  
2. Else, if the signal is loaded - skip.
  
3. Else, load the signal from the start, or from the batch where the loading process was interrupted
3. pid is a mandatory column in the raw data, and the parser dataframe output:
  
1. No pid => ERROR and STOP.
  
2. If the pid column is a string and not numeric, a mapping is generated from the strings to numeric values:
    
1. Mapping is done only with demographic signals (BDATE, GENDER). Thus, a pid in another signal file (say for instance DIAGNOSIS), that was not seen before in a demographic signal, would be excluded.
    
2. Therefore it is crucial to process the demographic signals first.
1. Before processing a signal - we first check whether it is needed:
  
1. When the dataframe includes all the parameters the signal needs, i.e. the dataframe includes columns with signal name and columns as needed with the corresponding attributes defined in rep_signals/general.signals, and the data passes all the tests (see description below), then no further processing is needed. 
  
2. If no further processing is indeed not required, the data is sorted and the process of the signal is done.
  
3. Otherwise see next.
3. Determining the right "processing unit":
  
1. When the parser output dataframe has a signal column:
    
1. Locate the signal in the general signal file (ETL_INFRA_DIR rep_signals/general.signals) or the additional signals added in CODE_DIR (does not exist => ERROR, please define the signal).
    
2. List by order signal_name and classifications (tags) as defined in the signal file.
    
3. Execute the most specific code for this signal.
    
4. For example, signal "BDATE" is classified as "demographic" and "singleton". The code would search for "BDATE.py", then "demographic.py", and finally "singleton.py". 
  
4. When the parser output dataframe has no signal column the code uses the parameter passed to the prepare_final_signals function, and follow the same phases.
    
1. Comment: it is even possible to pass more than one signal name, e.g. "BDATE,GENDER". In this case, the code would search for the most specific code for every signal.
0. When no relevant "processing unit" is found:A new "processing unit" with the signal name is created with comments and instructions.When interactive mode turned on - A python environment is opened so one can process the dataframe, inspect it, and define the required logic. When no interactive mode - it will fail and wait for you to fill in the code of the processing unit.
1. After the "processing unit" return the signal file:
  
1. A general test is performed on all signals - does it contains all the required time/value channels? Are values channel numeric? Is the date valid? Does the string contains illegal chars.
  
2. Next specific tests, per signal name and its classifications, are perfumed:
    
1. If the signal has more than one classification - tests associated with every tag are performed.
    
2. These tests can, for instance, compare signal distribution to references, count number of outliers etc.
    
3. More specific tests can be added globally under the [ETL infrastructure folder](High%20level%20-%20important%20paths/structure/ETL_INFRA_DIR) for all future ETLs or locally just in the [current ETL process](High%20level%20-%20important%20paths/structure/CODE_DIR)
2. Once the signal passes the tests, the file is organized by arranging the columns in the correct order, sorting them, and storing them in the appropriate location. Statistics about values for categorical signals are collected for building and testing dictionaries more efficiently later on.
3. The batch state or signal state is updated to indicate the successful completion of the current batch.
If your data includes specific dictionaries, you can call "prepare_dicts" ([ETL Manager Process](ETL%20Tutorial/ETL%20Manager%20Process)) to generate a corresponding dictionary.
Some of the categorical features do not require special treatment, e.g. "Drug", "PROCEDURES" and "DIAGNOSIS. For every categorical signal, the code tests the values based on the categorical prefix. For example, if you have a new signal called "DIAGNOSIS_Inpatient" with values starting with "ICD10_CODE:*," the code automatically recognizes this, use the right ICD-10 ontology, add missing codes and map them back to known codes if possible (since ICD, ATC are hierarchal by truncating the string). For example, a new ICD10_CODE:J20.X that doesn't exists, will be added and set as a child of "ICD10_CODE:J20" that exists in our ontology. You only need to use the correct prefix in the "prepare_final_signals" function. Statistics regarding these steps will be collected and printed during the final step. The code also prioritizes the "ATC" coding system for example, so if your drugs include "RX_CODES," the corresponding dictionary mapping RX_CODES to ATC codes will be loaded as well.
The finishing step involves calling the "finish_prepare_load" ([ETL Manager Process](ETL%20Tutorial/ETL%20Manager%20Process)) - This step involves processing the dictionaries for all categorical signals, generating a merged "signals" file from global and local changes, creating a convert_config file, and preparing the Flow command to execute the loading process.
 
