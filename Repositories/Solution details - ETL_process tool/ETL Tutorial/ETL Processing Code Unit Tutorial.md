# ETL Processing Code Unit Tutorial
# In this section, we will cover the steps required to process the data retrieved in the previous section of our ETL (Extract, Transform, Load) pipeline.
# The focus will be on transforming the data into the desired format and ensuring that it meets the necessary specifications for further analysis.
## Step-by-Step Guide
### 1. Understanding the ETL Processing Workflow
After data retrieval, the ETL processing involves several key steps:
1. PID Mapping: Convert non-numeric PID values to numeric. The mapping is stored under [WORK_DIR](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/WORK_DIR)/FinalSignals/ID2NR. The dictionary is created by demographic signals (each new PID with unknown mapping, is being added), and "inner joined" for all other signals. If patient is missing, it will be dropped with a message.
2. Signal Mapping: Map signals using the [CODE_DIR](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/CODE_DIR)/
```
 file if you have "signal" column in the dataframe. 
3. Data Transformation: Process the DataFrame to the final format.  -** WE ARE HERE, we are writing/customizing this part in the ETL.**
4. Testing: Implement and run tests to validate the processed data.
5. Storing: Sort and store the processed data in the designated directory - [WORK_DIR](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/WORK_DIR)/FinalSignals.
 
<img src="/attachments/14811382/14811576.png"/>
### 2. Processing the DataFrame
We will start with a DataFrame called 
```
 and transform it to include necessary columns and format. For this example, we will process demographic signals, such as GENDER.
You also have variable called "code_dir" of string type the points to the current ETL code path - for example if you want to access "configs" folder or some other resources.
#### Example Source DataFrame
```
   dup  index_dato  LC  date_LCdiagnosis  outpatientclinic_date  Age  FEV1  height  weight   BMI   Sex Smokingstatus  stage  NSCLC  pathology signal  pid
0    0  12mar2013   0              NaN             12mar2013     85   NaN     NaN    NaN    23.0  male  Formersmoker   NaN    NaN        NaN   None    1
1    1  04jun2021   0              NaN             04jun2021     92  0.89   164.0   50.0     NaN  male  Formersmoker   NaN    NaN        NaN   None    2
2    2  26oct2022   0              NaN             26oct2022     93  0.88   164.0   48.0     NaN  male  Formersmoker   NaN    NaN        NaN   None    2
3    0  04nov2015   0              NaN             04nov2015     81   NaN     NaN    NaN    26.0  male  Formersmoker   NaN    NaN        NaN   None    3
4    0  08dec2016   0              NaN             08dec2016     81   NaN     NaN    NaN    18.0  male  Formersmoker   NaN    NaN        NaN   None    4
```
### 3. Transforming the DataFrame
Here’s the code to transform the input DataFrame 
```
 into the required format:
#### Code:
```python
#You have dataframe called "df". Please process it to generare signal/s of class "demographic"
#Example signal from this class might be GENDER
#The target dataframe should have those columns:
#    pid
#    signal
#    value_0 - string categorical (rep channel type i)
 
# Extract relevant columns and rename 'Sex' to 'value_0'
df = df[['pid', 'Sex']].rename(columns={'Sex': 'value_0'})
# Create a new 'signal' column with the value 'GENDER'
df['signal'] = 'GENDER'
# Standardize values in 'value_0' column
df.loc[df['value_0'] == 'male', 'value_0'] = 'Male'
df.loc[df['value_0'] == 'female', 'value_0'] = 'Female'
# Select final columns and remove duplicates, per patient. Otherwise the a test will fail later, since patient can have only one sex value.
df = df[['pid', 'signal', 'value_0']].drop_duplicates().reset_index(drop=True)
```
 
****Some notes:****
1. The ETL infrastructures knows the signal type, so if something is missing, a test will fail and you will be asked to fix the test.
2. When you call "print" in the code block the output will be collected and stored in log files
3. The first part of the comments is part of the "template" the ETL constructs if the code file is missing with instructions to help you to complete the code under  
```
.
4. If you want to "import" a helper function/module, your path is $[CODE_DIR](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/CODE_DIR) for running. So use for example: "from signal_processings.process_helper import *" 
### 4. Code File Organization - which code will be executed?
The order of code execution decision is ordered by:
1. If DataFrame has "signal" column which is not None, it will use the name under "signal" to identify the signal name, otherwise it will use the name passed to "prepare_finall_signals" sigs argument. If the DataFrame contains multiple signal names, it will be divided into each name.rows with "None" in "signal" column willl be treated as "sigs" argument from "prepare_final_signals"
2. For the "signal" - the most specific logic exists in [CODE_DIR](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/CODE_DIR)/signal_processings/$SIGNAL_NAME_OR_PROCESSING_UNIT_NAME_OR_TAG.py will be executed. If there is a specific code with excat signal name, this logic will be executed, if not it will use "tags" in the [global signal definitions](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/ETL_INFRA_DIR) under "**rep_signals/**". The order of the tags is from most specific to less specifc. For example: Hemoglobin has those tags: "cbc,labs". So it will first look for cbc.py and if not exists will look for "labs.py" 
Example Directory Structure:
- 
```
- 
```
- 
```
 
