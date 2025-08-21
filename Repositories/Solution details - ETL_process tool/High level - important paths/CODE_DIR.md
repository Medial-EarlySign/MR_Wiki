# CODE_DIR
The code directory contains the specific ETL code for your loading.
<img src="/attachments/13402978/13402983.png"/>
We will usually contains 2 python files - a parser helper library for this ETL and "load.py' which is the entry point for executing the loading process. The load is the driver that calls all the pipeline and connects the "points" in the ETL.

- FOLDER - **configs** - a directory with specific configuration for this ETL. might also be empty if not needed, but will apparently contains some settings for unit and signal mapping.
    - FILE - **rep.signals** - This file will be created for you with empty content, just comments and instructions for easier usage if needed. In this file you can **OVERRIDE or ADD** new signals definitions that you are going to use in this repository. The file format is in the same format of : [Repository Signals file format](../../Repository%20Signals%20file%20format.md).  Please add new signals from ID >= 3000 
    - FILE - **map_units_stats.cfg** - if you are going to use signals mapping and unit conversions and call the API functions to help you with unit conversions as in : [unit_conversion](../../Solution%20details%20-%20ETL_process%20tool/ETL%20Tutorial/ETL%20Processing%20Code%20Unit%20Tutorial/unit_conversion) section. This file will be used to contains the configuration of the signals mapping + unit conversion. 
    - ... - Your call to add more "configuration" files as needed.
- FOLDER - **signal_processings** - A folder that will be created if not exists and contains the "logic" for processing the different signal / data types.
    - FILE - **XXXX.py** - Each file under this folder is a python file that contains specific code to process this data type. for example "labs.py" will process all signals with "labs" tag in their definition (if no more specific code exists, please refer to [ETL_INFRA_DIR](ETL_INFRA_DIR.md) for more info). For example, if we are loading "Hemoglobin" signal which has those tags "labs,cbc". If we have a file name "Hemoglobin.py" this code will be executed, than it will search for "cbc.py" and than for "labs.py". That way you can control and reuse the code easily for different signals. In most cases, just "labs.py" is enough for all numeric labs. In first time usage, if no file exists a "template" for this file will be created with the following format with instructions (it might help you better understand what to do):
```python
#You have dataframe called "df". Please process it to generare signal/s of class "smoking"
#Example signal from this class might be Smoking_Status
#The target dataframe should have those columns:
#    pid
#    signal
#    time_0 - type i
#    value_0 - string categorical (rep channel type i)
#Source Dataframe - df.head() output:
#     time_0     ahdcode ahdflag      data1   data2      data3 data4 data5 data6  medcode signal  pid
#0  19880705  1008050000       Y             INP001                N           Y  4K22.00   None    1
#1  19921209  1005010200       Y  81.000000          28.300000                    22A..00   None    1
#2  19921209  1003050000       Y          Y       2                               136..00   None    1
#3  19921209  1003040000       Y          N       0                               137L.00   None    1
#4  19930000  1001400086       Y                                                  537..00   None    1
```
And than you can write your code that process "df" object into the instructed format.
- FOLDER - **tests** - optional, used very rarely. To add more tests only for this ETL process. same format as in [ETL_INFRA_DIR](ETL_INFRA_DIR.md) tests folder. The code "merges" the folders.
