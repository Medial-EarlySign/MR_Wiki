# ETL Manager Process
In this tutorial, we will cover the ETL manager process, which includes loading and preparing final signals, handling special client dictionaries, and finishing the preparation for data loading into the repository.
We will walk through the steps required to use the three main API calls: 
```
, 
```
, and 
```
.
## Overview of the manager process:
<img src="/attachments/13402629/14811579.png"/>
## Step-by-Step Guide
### 1. Setting Up the Environment and Imports
First, ensure that you have the necessary imports and environment setup for your ETL process.
#### Code:
```
import sys
import os
import pandas as pd
from ETL_Infra.etl_process import *
# Import data_fetcher for specific data sources (example: THIN), that we wrote in step 1
import thin_ahd_data_fetcher, thin_patient_data_fetcher
```
### 2. Preparing Final Signals
The [
```
 ](http://node-01/ETL_Infra/ETL_Infra.html#etl_process.prepare_final_signals)function is called for each data type to process the signals, test them, and handle batching if necessary.
#### Example Code:
```
WORK_DIR = '/nas1/Work/Users/Alon/ETL/demo_thin'
batch_size = 1  # Process files 1 by 1 in each batch
sig_name_or_group_name = 'demographic'
# Prepare final signals for each data type
prepare_final_signals(thin_patient_data_fetcher, WORK_DIR, sig_name_or_group_name, batch_size, override='n')
prepare_final_signals(thin_ahd_data_fetcher, WORK_DIR, 'labs', batch_size, override='n')
# Add additional data types as needed
```
 
### 3. Preparing Special Client Dictionaries
The [
```
 ](http://node-01/ETL_Infra/ETL_Infra.html#etl_process.prepare_dicts)function is used to prepare dictionaries for specific signals when there are special client dictionaries involved.
This function constructs mapping dictionaries from the provided DataFrames.
#### Example Code:
```
# Example definition dictionary DataFrame
def_dict = pd.DataFrame({
    'internal_client_code': ['A123', 'B456'],
    'description': ['Description A', 'Description B']
})
# Example set dictionary DataFrame
set_dict = pd.DataFrame({
    'parent': ['ICD10_1', 'ICD10_2'],
    'child': ['A123', 'B456']
})
# Prepare dictionaries for the 'DIAGNOSIS' signal based on internal_client_code and their description
prepare_dicts(WORK_DIR, 'DIAGNOSIS', def_dict, set_dict)
# A new dictionary value with "A123" and "Description A" will be added to dictionary with the same value
```
more details about categorical signals and how to create custom dictionaries when needed, can be found here: [Categorical signal/ Custom dictionaries](../Categorical%20signal_%20Custom%20dictionaries)
### 4. Finishing the Preparation and Loading
The [
```
 ](http://node-01/ETL_Infra/ETL_Infra.html#etl_process.finish_prepare_load)function completes the preparation of dictionaries, generates signals, converts the configuration, and scripts to load the repository with Flow.
**Example Code:**
```python
# Finish preparation and load the repository
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```
### Full Template Example
Here is a full example that combines all the steps:
#### Full Example Code:
```python
import sys
import os
import pandas as pd
from ETL_Infra.etl_process import *
# Import data_fetcher for specific data sources (example: THIN)
from examples.thin_example.thin_parser import thin_ahd_data_fetcher, thin_patient_data_fetcher
# Define work directory and batch size
WORK_DIR = '/nas1/Work/Users/Alon/ETL/demo_thin'
batch_size = 1  # Process file by file
sig_name_or_group_name = 'demographic'
# Prepare final signals for each data type
prepare_final_signals(thin_patient_data_fetcher, WORK_DIR, sig_name_or_group_name, batch_size, override='n')
prepare_final_signals(thin_ahd_data_fetcher, WORK_DIR, 'labs', batch_size, override='n')
# Add additional data types as needed
# Example definition dictionary DataFrame
def_dict = pd.DataFrame({
    'internal_client_code': ['A123', 'B456'],
    'description': ['Description A', 'Description B']
})
# Example set dictionary DataFrame
set_dict = pd.DataFrame({
    'parent': ['ICD10_1', 'ICD10_2'],
    'child': ['A123', 'B456']
})
# Prepare dictionaries for the 'RC' signal
prepare_dicts(WORK_DIR, 'RC', def_dict, set_dict)
# Finish preparation and load the repository
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```
 
 
 
## OLD Documentation for reference with more details on functions
The loading process is based on 3 API calls (you might use just 2 on them in most cases).
1. prepare_final_signals - This function call will be called for each data type. The input might be given in multiple files/tables/sources - and there is different handling for each data source. This function will be called on each data type and process the signals to FinalSignals + Test them. It can also handle "batches".Inputs:
  - data_frame/data_fetcher - First argument is dataframe or data_fetcher (if you will need to process the data with batches when it's too big)
  - workdir - Second argument is string with folderpath to process and prepare loading, tests outputs and more...
  - signal_type - third argument is string with signal name or signal type and only needed if you use data_fetcher - this will be used to classify this data type in order to provide specific tests for it + when finished to mark it as completed to skip it later. When you provide dataframe, it's not used since you can extract the signal name directly from the dataframe
  - batch_size - integer to control batch size, only used with data_fetcher. 0 means on batching, read all and unite
  - override - string to specify if to do override on existing signals or skip (y/n). UJsefull to keep the code as is without commenting out lines, it will skip already completed signals
0. prepare_dicts - this function prepare dictionaries for specific signal. This is needed only when there are special client dictionaries. When the Client is using ICD10_CODE, or known codes, it is not needed and will be handle automatically later. You will need to use and call this funciton on every signal with additional special client dictionariesInputs:
  - workdir - First argument is string with folderpath to process and prepare loading files and in this case the dictionaries
  - signal - Second argument is string that specify the signal name
  - def_dict - Dataframe with 2 columns, First column is the "internal client code" and the second column is the description of this code. The name of the columns doesn't matter. This function construct DEF dictionary from this dataframe and gives 2 line for each internal category medial ID. The first row is the "internal client code" second line is the description. When you will use this code, you will get both aliases. The function also removes illegal dictionary characters for you. (THIS argument is optional and can be given as None if no description for internal client codes)
  - set_dict - Dataframe with 2 columns, first is "parent" in known ontology (ICD10, ATC, depends on the signal type) and the second column is "child" in "cleint internal coding system". This will construct the mapping between client codes and known ontology. 
0. finish_prepare_load - Will finish preparation of dictionaries, will generate signals, convert config and script to load the repository with Flow + print the Flow command to screen.Inputs:
  - workdir - First argument is string with folderpath to process and prepare loading files and in this case the signals file and convert config + script to run Flow to start loading
  - dest_folder - Second argument is string to specify where to store final repository
  - dest_rep - Third argument is string to specify repository name. For example "thin", "KP" this will be the prefix for .repository file
  - to_remove - OPTIONAL argument to provide list of strings with signal names to comment out from loading
  - load_only - OPTIONAL argument to provide list of strings with signal names to LOAD_ONLY
 
