# ETL_process dynamic testing of signals
We can add both global test for all ETL processes and local/specific ETL process. We can also override global tests when specifying the same name in the local path.
- The global tests can be found under this location $MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra/tests. The local tests are under $CODE_DIR/tests.
- The code runs from "$MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra" - so if you want to search for config files, dictionaries or something you can use relative path.
- Under each path (global or local), there is additional directory for each group of tests. The name of the directory can be either name of signal or name of group of signals (for example "labs" or "cbc") and by this name, only the relevant signals are being tested.
- Each test file code should contain a function called "Test" with 4 arguments: dataframe, signal_info, codedir and workdir. The dataframe is the input data frame with the signal for testing, codedir - is the path of the ETL code (might be usefull if you want to use "config" folder in your code dir). workdir is path of workdir to store outputs if wanted. function returns True if test passes and False if it should fail. signal_info contains information about the signal Example of full test path under $MR_ROOT/Tools/RepoLoadUtils/common/tests:
  - labs
    - 
test_non_nulls.py
```python
import pandas as pd
def Test(df: pd.DataFrame, si, codedir: str, workdir: str):
    if len(df)==0:
        return True
    cols=[x for x in df.columns if x=='pid' or 'value' in x or 'time' in x]
    sig_name=df['signal'].iloc[0]
	#si.t_ch - contains array of each time channel type (for example "i" is integer, "f" float). v_ch is the same for value channels.
    signal_columns=[ 'time_%d'%(i) for i in range (len(si.t_ch))] + [ 'value_%d'%(i) for i in range (len(si.v_ch))]
    signal_columns.append('pid')
    for col in cols:
        if col not in signal_columns:
            print(f'Skip columns {col} which is not needed in signal {sig_name}')
            continue
        null_date_cnt=len(df[df[col].isnull()])
        if null_date_cnt/len(df)>0.001:
            print('Failed! There are %d(%2.3f%%) missing values for signal %s in col %s'%(null_date_cnt, 100*null_date_cnt/len(df), sig_name, col))
            return False
        if null_date_cnt > 0:
            print('There are %d(%2.3f%%) missing values for signal %s in col %s'%(null_date_cnt, 100*null_date_cnt/len(df), sig_name, col))
        df.drop(df.loc[df[col].isnull()].index, inplace=True) #clean nulls
        df.reset_index(drop=True, inplace=True)
    print('Done testing nulls in signal %s'%(sig_name))
    return True
```
This test will be executed against all labs signals and test that there are no more than 1% nulls in pid,time_0,value_0. You can copy the test into local directory and change the threshold for example...
 
To plot graph into html you can use plot_graph funtion, please import is with:
****
 Expand source
```python
import sys, os
from ETL_Infra.plot_graph import plot_graph
```
The function accepts dataframe with 2 columns - or dictionary with name and dataframe of 2 cols to plot multiple series
 
You can also re/run test on signals using:
```
python  $MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra/run_test_on_sig.py --workdir $WORKDIR --codedir $CODEDIR --signal $SIGNAL
```
signal might be several signals comma seperated.
