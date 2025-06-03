# ETL Tutorial
# What is this?
This is  not a regular tutorial for using library.
This is tutorial for using a library consist of 5 functions + best practice usage.
You can use the library functions differently but I encourage you to use it as described here, or if you have better ideas, we can improve the best practice instructions for everyone and create a better standard.
# Where to start?
First, create an empty directory to store the code of your specific ETL - [CODE_DIR ](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/CODE_DIR)
The final [CODE_DIR ](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/CODE_DIR)will look like this:
[<img src="/attachments/14811356/14811417.png"/>](#)
To perform the load, you only need to run "python load.py". Simple and easy convention to understand the full flow of the loading process.
I don't recommend creating multiple "load.py" files or name it differently and the reason is convention and to have 1 entry point for the full loading process. No multiple steps of running this script and then that script, etc! 
The "configs" + "signal_processing",can and should start empty. Don't even need to create those folders. The ETL process will create them for you when you will be needed to configure things.
 
## ETL Architecture Explanation 
**Anything** that can be automated is automated and reused between different ETL loads. That's what we aim to and I think we are in a good position.
 
Your job is to write just the specific loading logic for your specific input data format.
No, it is not a "solution" of defining "input" + "output", since the "input" has undefined format and you need to transform it to our defined format. You can't escape from this problem that you start from undefined format.
Any tries to create a "standard" input as entry point will fail and not solve most of the problem. Our final loading format is quite simple, so there is no need in "intermediate" data format to transform the data into.
You could just define the ETL input as: convert your undefined input structure to the final output format as entry point for the ETL library and do nothing in the ETL infrastructure.
I have discovered that there are many things that can be reused, simplified, better arranged if you used this ETL library to process the undefined input data to our desired output for loading.
The drawback is that you need to understand how to use this and it's more complicated since there is no defined input format.
 
****Motivation:**** The OLD THIN loading code had **~4 times** more lines of codes compared to the new ETL process.
In the old ELT, There is no single step to rerun the ETL, and there are many "manual" step like copying files, running commands one after another in certain order. There are no tests for the output, etc. 
## The ETL Process is divided into 3 parts:
1. **[Data fetching](Data%20Fetching%20step)** - The main idea, is to write code specific to "read" data into DataFrame - this code can't/should be reused and specific to your ETL. There are helper functions described in "data fetching" section. It suppose to be short and easy code, no complex manipulation - reading raw data as is to dataframe.  It can be as simple as pd.read_csv(), or fetching from database, etc. Explains how to write the equivalent "thin_parser.py" in the CODE_DIR example.
2. **[Data processing](ETL%20Processing%20Code%20Unit%20Tutorial)**  - The main idea is to do the manipulations in the raw input DataFrame here (fetched from previous step) and to fit the the final signal structure. Each signal\group of signals will get a section and it will maintain readability of the processing step. It's not suppose to be very long code in most cases, but it is also very specific to your data. Not suppose to be code reuse between ETLs. It can be as simple as "renaming" columns if everything is good, or a bit more complicated.labs+units: There is a helper function to convert units for lab signals if needed. Not always needed, and also when needed you want to control when to call this - for example, you first want to filter null dates, null values and then just call the unit conversion.It is a library and your call how to process the data. This part will explain how to edit and write code in "signal_processings" directory.
3. [Manager ](ETL%20Manager%20Process)-Explains how to write the main "load.py" program to control the data flow from "data fetching" into the data processing, connecting the 2 endpoints together. This script will be execute and will do the loading. It's suppose to be short code. It's hard to reuse between different ETLs and also maintain readability top-down of the whole process. Anyway, it's a simple and short code. 
 
## Code Documentation level:
There is [code documentation](http://node-01/ETL_Infra/) for each function using pydoc, to build the documentation:
****
 Expand source
```
pushd $ETL_LIB_PATH/docs && make html && popd
#The documentation is here:
$ETL_LIB_PATH/docs/build/html/index.html
```
No need to run this, in each git push to tools, the documentation is getting updated.
<img src="/attachments/14811356/14811411.png"/>
## Deeper dive
Reference to more information on what happens in the loading process:
[High level - important paths/structure](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths_structure)
In the external link to slide on our ETL: [ETL_infra.pptx](https://medial.sharepoint.com/:p:/r/sites/algoteam/Shared%20Documents/General/genericETL/ETL_infra.pptx?d=wd53c98071ab841049d0472b1178fcb6c&csf=1&web=1&e=yREHdL)
 
