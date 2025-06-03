# ETL process unit
example of labs.py for Mayo_AS loading
```python
null_date_cnt=len(df[df['time_0'].isnull()])
print('There are %d missing dates for signal %s'%(null_date_cnt, df['signal'].iloc[0]))
if null_date_cnt/len(df)>0.01:
    print('There are too many missing dates in this signal, more than 1%%'%(null_date_cnt))
    raise NameError('Too many missing dates, please resolve by yourself')
df=df[df['time_0'].notnull()].reset_index(drop=True)
#Conversion of date column in this dataset
df['time_0']=df['time_0'].astype(str).map(lambda x: int(x.split('/')[-1])*10000 + int(x.split('/')[0])*100 + int(x.split('/')[1]) )
 
```
That's it, this code block will be executed on all labs signals, very easy to follow, change, locate, what was done in the ETL process. In most cases, it's very simple code.
Guess what? hemoglobin was failed under global tests of distribution (defined globally and not in labs.py), you will be prompt to write code for "Hemoglobin.py".
In the ETL process, the most specific code for your signal processing will get executed (in this case Hemoglobin.py) The hierarchy is defined in the "signals definition file" column number 5 with comma separated.
You will be prompt with interactive shell to "play" and write code to fix the error in the signal.
 
Hemoglobin distribution in first run (that got failed).
<img src="/attachments/13402330/13402328.png"/>
After the fix, by creating this code in Hemoglobin.py:
```python
df=df[df['time_0'].notnull()].reset_index(drop=True)
df['time_0']=df['time_0'].astype(str).map(lambda x: int(x.split('/')[-1] )*10000 + int(x.split('/')[0])*100 + int(x.split('/')[1]) )
df=df[df['Units']!='%'].reset_index(drop=True) #Remove of "%" units which is other signal , maybe Hematocrit? Also after checking the mapping, discovered that is mapped wrong, typo
```
 
 
<img src="/attachments/13402330/13402329.png"/>
The real problem and the better solution was to go over the "map.tsv" file and than I discovered Hematocrit was mapped to Hemoglobin.
But this it's not just theoretical, in IBM loading some of the hemoglobin signals with "%" were hematocrit under the same loinc cod and the mixing in cbc tests, happened in many signals.
## Example of "full" usage:
```python
import sys, os
sys.path.insert(0, os.path.join(os.environ['MR_ROOT'], 'Tools/RepoLoadUtils/common/ETL_Infra')) #Add common to path
import pandas as pd
from etl_process import *
#END of imports
WORK_DIR='/nas1/Work/Users/Alon/ETL/demo_mayo2' # where we are going to work
#Read data - your specific code of reading part of data - to be improved to have an ability/API to fetch batch from the data, wrapper to file system, DB, etc.
#For BIG data or to read in batches please refer to data_fetcher and return data_fetcher to fetch dataframes in batches
df=pd.read_csv('/nas1/Data/Mayo_AS/AS_labs.csv').rename(columns={'id':'pid', 'Lab_Date':'time_0', 'TestDesc':'signal', 'Resultn': 'value_0'})
#Process signal type
prepare_final_signals(df, WORK_DIR, None, editor = '/home/apps/thonny/bin/thonny', override='n')
```
