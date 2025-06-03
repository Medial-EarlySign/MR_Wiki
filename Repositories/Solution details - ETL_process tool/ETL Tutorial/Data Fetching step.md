# Data Fetching step
# Data Fetching Tutorial for Internal Library
This tutorial will guide you through the process of data fetching in our internal library.
We will cover the steps required to retrieve and parse data into a DataFrame using helper libraries.
There is 1 helper library to access files and the other one is for accessing data from database, you will want to use only one of them most cases. 
We will demonstrate how to write fetcher from files.
## Step-by-Step Guide
Open a file, for this example "thin_parser.py" 
### 1. Setup and Imports
First, we need to import necessary libraries and set up the environment to include our ETL infrastructure.
**python imports**
```python
import os
import sys
import pandas as pd
# Import helpers from data_fetcher
from ETL_Infra.data_fetcher.files_fetcher import files_fetcher, list_directory_files
```
### 2. Helper Function to List Files
Next, we will create a helper function to list the relevant files from the raw data directory or directories.
This function helps in managing file paths and retrieving a list of files based on a specific prefix.
```python
def list_files(file_prefix):
    base_path = '/nas1/Data/Roche_Denmark/Roche/Population2'
    return list_directory_files(base_path, file_prefix)
```
 
****Explanation + tips:**** We use a simple helper function "list_directory_files" which receives a directory and regex and lists all files inside the directory that matches this regex.
The goal is to not repeat the "base_path" of the raw data and have a simple function to retrieve list of files for our loading process.
A good practice is to use this to function to retrieve files that are all of the same type/format and not to combine multiple types together.
Each file type will be read independently to load specific signal or group of signals in the next steps and here we just want to combine each type separately.
### 3. File Path Parsing Function
After listing the files, we need to write a function to read and parse each file into a DataFrame. This example shows how to parse lab results files.
The only constraint in this step is to return dataframe with "pid" column:
```python
def labs_file_parser(filepath):
    # Read the file into a DataFrame
    df = pd.read_csv(filepath, names=['pid', 'index_date', 'lab_date', 'lab_name', 'value_0', 'lab_name_unfiltered'])
    
    # Create a 'signal' column by concatenating 'lab_name' and 'lab_name_unfiltered'
    df['signal'] = df['lab_name'] + '::' + df['lab_name_unfiltered']
    df.loc[df['signal'].isnull(), 'signal'] = df['lab_name_unfiltered']
    
    return df
```
### 4. Lazy Data Fetcher
The final step is to create a lazy data fetcher function. This function will fetch data in batches, allowing for efficient data handling and memory usage.
 
```python
def labs_data_fetcher(batch_size, start_batch):
    files = list_files('pop2_datasetB_labresults_firstvisit_for_controls_LCdate_for_cases')
    return files_fetcher(files, batch_size, labs_file_parser, start_batch)
```
 
****Explanation** **: This step combines steps 2+3 together as we can see.
The final result is a function that receives 2 arguments:  batch_size, start_batch.
The batch_size  is how big is a single batch and "start_batch" means from where we start to retrieve the data - 0 means from the start. x - means skip the first "x" batches.  
What does it mean "lazy", it means that this function only fetches the data when called with "next" with for loop and not pre ahead. 
We will only use this "**labs_data_fetcher**" in the next steps of the ETL.
### Example Usage
Let's see an example of how to use the lazy data fetcher. We will fetch data in small batches and demonstrate how to iterate through the data.
```
# Create a data fetcher
data_fetcher = labs_data_fetcher(batch_size=100, start_batch=0)
# Fetch the first batch of data
batch1 = next(data_fetcher)
print(batch1)
# Fetch the next batch of data
batch2 = next(data_fetcher)
print(batch2)
```
We wouldn't need to use the data_fetcher directly, we will pass it as argument to a function in next step, but this is just a demonstration of how we can debug/fetch the data in batches.
### Dummy example
Another dummy example of writing a data fetcher directly, but without helper functions in step 2+3.
```python
def dummy_data_fethcer_of_fake_data(batch_size, start_batch):
	#In this simple funtion, we ignore the "batch_size, start_batch" and returns lazy iterator with 2 DataFrames
	yield pd.DataFrame({'pid':[1,2,3], 'data':['A','B', 'C']})
	yield pd.DataFrame({'pid':[4,5,6], 'data':['D','E', 'F']})
```
This will result in lazy iterator with 2 batches of dataframe.
### Handling big files
A more complex example of doing batches on multiple BIG files where batch_size is how many records to read from current file till closing the buffer also exists with helper function "big_files_fetcher".
This will require to write a bit more complex "labs_file_parser" that will also receives the batch_size and how many rows to skip and will need to respect those parameters.
Please refer to examples/denmark_examples/etl_demonstration.py"
 
