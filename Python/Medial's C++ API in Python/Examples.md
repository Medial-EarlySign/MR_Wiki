# Examples
 
When using "get_sig" function, there is no need to call "read_all" before, "init" is enough. get_sig, loads the signal automatically from disk if needed and not loaded
 
**Using Lookup table in python**
 Expand source
```python
rep = med.PidRepository()
rep.read_all(FLAGS.rep, readmissions.pid.values.astype('int32'), ['ADMISSION','DIAGNOSIS_IP','DIAGNOSIS_OP'])
admissions = rep.get_sig('ADMISSION').rename(columns = {'time0':'outcomeTime'})
readmissions = readmissions.merge(admissions,on = ['pid','outcomeTime'],how='outer')
# Handle missing admissions
readmissions.loc[((readmissions.outcome==1) | (readmissions.outcome==2) | (readmissions.outcome==3)) & (readmissions.time1.isna()),'time1'] = readmissions.loc[((readmissions.outcome==1) | (readmissions.outcome==2) | (readmissions.outcome==3)) & (readmissions.time1.isna()),'outcomeTime']
# Read Relevant Codes
icd9 = pd.read_csv(FLAGS.icd9,header=None,names=['code']).code.values
# Add Adverse Events
lut = rep.dict.prep_sets_lookup_table(rep.dict.section_id('DIAGNOSIS_IP'),['ICD9_CODE:'+str(x) for x in icd9])
ip_diagnosis = rep.get_sig('DIAGNOSIS_IP',translate=False)
ip_diagnosis = ip_diagnosis[(lut[ip_diagnosis.val0]!=0)]
op_diagnosis = rep.get_sig('DIAGNOSIS_OP',translate=False)
op_diagnosis = op_diagnosis[(lut[op_diagnosis.val0]!=0)]
```
**Iterating over a Signal**

```python
## This is not the proper way to work with Python, since Python loops are very slow, however, it's nice as a poc.
## Doan't do this, using python loops is slow
 
import sys
#sys.path.insert(0,'/nas1/UsersData/shlomi/MR/Libs/Internal/MedPyExport/generate_binding/CMakeBuild/Linux/Release/MedPython')
import medpython as med
signame = 'Albumin'
rep = med.PidRepository()
rep.read_all('/home/Repositories/THIN/thin_jun2017/thin.repository',[],[signame])
print(med.cerr())
for pid in rep.pids[20:30]:
  usv = rep.uget(pid, rep.sig_id(signame))
  if len(usv)>0:
    print('\n\n')
    for rec in usv:
      print("Patient {} had {}={:.2} at {}".format(pid, signame, rec.val(), rec.date()))
```
**Setup **

```python
# py2/py3 compatiblity
from __future__ import print_function 
import numpy as np
import pandas as pd
# Not Needed anymore, but use it if you need to override
#import sys
#sys.path.insert(0,'/nas1/UsersData/USER/MR/Libs/Internal/MedPyExport/generate_binding/Release/medial-python36')
import med
med.logger_use_stdout()
rep = med.PidRepository()
rep.read_all('/home/Repositories/THIN/thin_final/thin.repository',[],['WBC','Cancer_Location',
                                                                          'GENDER','BYEAR',
                                                                          'Cancer_Location',
                                                                          'DEATH','ENDDATE',
                                                                          'Albumin','BDATE'])
print(med.cerr())
```
**Useful functions to fix signal types**

```python
def fix_ts_m1900(df, col):
    import datetime as dt
    df[col] = dt.datetime(1900,1,1)+pd.TimedeltaIndex(df[col], unit='m')
def fix_type(df, col, newtype): df[[col]] = df[[col]].astype(newtype, copy=False)
def fix_date_ymd(df, col): df[col] = pd.to_datetime(df[col], format='%Y%m%d')
def fix_name(df, old_col, new_col): df.rename(columns={old_col: new_col}, inplace=True)
```
**Load some signals**

```python
albumin = rep.get_sig('Albumin')
albumin = albumin[albumin['date'] % 100 != 0]
fix_name(albumin,'val','Albumin')
fix_date_ymd(albumin, 'date')
gender = rep.get_sig('GENDER')
fix_type(gender,'val', int)
fix_name(gender,'val','Gender')
bdate = rep.get_sig('BDATE')
fix_type(bdate,'val', int)
bdate['val'] = bdate['val'] + 1
fix_date_ymd(bdate, 'val')
fix_name(bdate,'val','BDate')
 
mortality = rep.get_sig('DEATH')
fix_type(mortality,'val', int)
mortality = mortality[(mortality['val'] % 100 <= 31) & (mortality['val'] % 100 > 0)]
fix_date_ymd(mortality, 'val')
fix_name(mortality,'val','MortDate')
 
```
**Merge signals into one dataframe**

```python
from functools import reduce
data = reduce(lambda left,right: pd.merge(left, right, on='pid', how="left", sort=False),[albumin,gender,bdate,mortality])
```
**Which Python med module am I using**

```python
import med
print(med.__file__)
if hasattr(med.Global, 'version_info'):
    print(med.Global.version_info)
```
**Bootstrap analysis**

```python
import pandas as pd
import med
df=pd.read_feather('/nas1/Work/Users/Ilya/Mayo/Feathers/predictions_073.feather')
df=df[['true_V', 'prob_V']]
#Example of Analyzing df with bootstrap
bt=med.Bootstrap()
res=bt.bootstrap(df['prob_V'], df['true_V'])
all_measurment_names=res.keys()
print('AUC: %2.3f [%2.3f - %2.3f]'%(res['AUC_Mean'], res['AUC_CI.Lower.95'], res['AUC_CI.Upper.95']))
#Can convert to dataframe with Measurement and Value columns:
res_df=res.to_df()
res_df[res_df['Measurement'].str.startswith('AUC')]
```
**Load MedModel and apply (predict) on sample**

```python
import med
rep_path='' #Path of repositroy
model_file ='' #Path of MedModel
samples_file = '' #path of samples or load samples from DataFrame using: samples.from_df(dataframe_object with the right columns)
print("Reading basic Repository structure for fitting model")
rep = med.PidRepository()
rep.init(rep_path) #init model for first proccesing of "model.fit_for_repository"
 
print("Reading Model")
model = med.Model()
model.read_from_file(model_file)
model.fit_for_repository(rep)
signalNamesSet = model.get_required_signal_names() #Get list of relevant signals the model needed to fetch from repository
 
print("Reading Samples")
samples = med.Samples()
samples.read_from_file(samples_file)
ids = samples.get_ids() #Fetch relevant ids from samples to read from repository
 
print("Reading Repository")
rep.read_all(rep_path, ids, signalNamesSet) #read needed repository data
 
#Apply model:
model.apply(rep, samples)
df = samples.to_df()
df.to_csv('output_file')
samples.write_to_file('write_to_samples_file')
 
#feature matrix exists in - model.features.to_df() . The "samples" object now has the scores
```
**Learn model from json to generate matrix**

```python
import med
rep_path='' #Path of repositroy
json_model ='' #Path of json
samples_file = '' #path of samples or load samples from DataFrame using: samples.from_df(dataframe_object with the right columns)
 
print("Reading basic Repository structure for fitting model")
rep = med.PidRepository()
rep.init(rep_path) #init model for first proccesing of "model.fit_for_repository"
  
print("Reading Model")
model = med.Model()
model.init_from_json_file(model_file)
model.fit_for_repository(rep)
signalNamesSet = model.get_required_signal_names() #Get list of relevant signals the model needed to fetch from repository
  
print("Reading Samples")
samples = med.Samples()
samples.read_from_file(samples_file)
ids = samples.get_ids() #Fetch relevant ids from samples to read from repository
  
print("Reading Repository")
rep.read_all(rep_path, ids, signalNamesSet) #read needed repository data
  
#Learn model:
model.learn(rep, samples)
model.features.to_df().write_to_file('write_to_matrix_file')
```
**Bootstrap analysis on samples**

```python
import med
samples=med.Samples()
samples.read_from_file('/nas1/Work/AlgoMarkers/Pre2D/pre2d_1_041219/Performance_no_drugs/OnTest/Partial_All_on_OnTest_2_no_drugs_filtered.preds')
REP_PATH='/nas1/Work/CancerData/Repositories/THIN/thin_jun2017/thin.repository'
JSON_TO_FILTER='/server/UsersData/alon/MR/Projects/Shared/Projects/configs/Diabetes/configs/bt_features.json'
COHORT_FILE='/server/UsersData/alon/MR/Projects/Shared/Projects/configs/Diabetes/configs/bt_params'
bt=med.Bootstrap()
res=bt.bootstrap_cohort(samples, REP_PATH,JSON_TO_FILTER, COHORT_FILE)
res_df=res.to_df()
res_df
```
**print errors in medPython**

```python
print(med.cerr())
```
 
 
 
 
 
 
 
 
 
 
 
 
