# Examples
 

## Import Medial's API in Python  
   ```python
   import med
   # Optional set to use stdout, usually I'm not running this:
   med.logger_use_stdout()
   ```

## Which MedPython module am I using

```python
print(med.__file__) # Shows file path
if hasattr(med.Global, 'version_info'):
    print(med.Global.version_info) # Shows compilation date and git commit hash when compliled "version"
```

## Inspect Available Functions

Documentation is a work in progress.  
To inspect available methods:

```python
help(med)
help(med.PidRepository)
```

## Load a Repository

```python
rep = med.PidRepository()
rep.read_all(
    '/nas1/Work/CancerData/Repositories/THIN/thin_2021/thin.repository',
    [],
    ['GENDER', 'DEATH', 'BDATE', 'Albumin']
)
print(med.cerr())
```

## Iterating over a Signal

```python
## This is not the proper way to work with Python, since Python loops are very slow, however, it's nice as a poc.
## Don't do this, using python loops is slow - use get_sig to retrieve dataframe

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


## Useful functions to fix signal types

```python
def fix_ts_m1900(df, col):
    import datetime as dt
    df[col] = dt.datetime(1900,1,1)+pd.TimedeltaIndex(df[col], unit='m')
def fix_date_ymd(df, col): df[col] = pd.to_datetime(df[col], format='%Y%m%d')
```
## Load some signals

When using "get_sig" function, there is no need to call "read_all" before, "init" is enough. get_sig, loads the signal automatically from disk if needed and not loaded

```python
albumin = rep.get_sig('Albumin')
albumin = albumin[albumin['date'] % 100 != 0]
albumin.rename(columns={'val': 'Albumin'}, inplace=True)
fix_date_ymd(albumin, 'date')
gender = rep.get_sig('GENDER')
gender.rename(columns={'val': 'Gender'}, inplace=True)
bdate = rep.get_sig('BDATE')
bdate['val'] = bdate['val'] + 1
fix_date_ymd(bdate, 'val')
bdate.rename(columns={'val': 'BDate'}, inplace=True)
 
mortality = rep.get_sig('DEATH')
mortality = mortality[(mortality['val'] % 100 <= 31) & (mortality['val'] % 100 > 0)]
fix_date_ymd(mortality, 'val')
mortality.rename(columns={'val': 'MortDate'}, inplace=True)
 
```

## Using Lookup table in python

* When using "get_sig" function, there is no need to call "read_all" before, "init" is enough. get_sig, loads the signal automatically from disk if needed and not loaded.
* We can use dictionaries to query specific categorical codes and their hierarchies. 
    - For example, by defining "ICD10_CODE:J00-J99", we'll capture all codes within this group based on the dictionary's definition of ICD10. 
    - This method relies on predefined parent-child pairs for hierarchy and does not use regular expressions. 
    - It is not limited to ICD10, ICD9 or specific known code system, but you will need to define the dictionaries correctly and their hierarchies.

```python
# readmissions is data frame with readmitted patients
rep = med.PidRepository()
rep.read_all(FLAGS.rep, readmissions.pid.values.astype('int32'), ['ADMISSION','DIAGNOSIS_IP','DIAGNOSIS_OP'])
admissions = rep.get_sig('ADMISSION').rename(columns = {'time0':'outcomeTime'})
readmissions = readmissions.merge(admissions,on = ['pid','outcomeTime'],how='outer')
# Handle missing admissions
readmissions.loc[((readmissions.outcome==1) | (readmissions.outcome==2) | (readmissions.outcome==3)) & (readmissions.time1.isna()),'time1'] = readmissions.loc[((readmissions.outcome==1) | (readmissions.outcome==2) | (readmissions.outcome==3)) & (readmissions.time1.isna()),'outcomeTime']
# Read Relevant Codes
icd9 = pd.read_csv(FLAGS.icd9,header=None,names=['code']).code.values
# Add Adverse Events for each ICD9 code in icd9 dataframe. It also uses hierarchy defined in the dictionary, for example using "487" includes: 487.0, 487.1, 487.8, etc.
lut = rep.dict.prep_sets_lookup_table(rep.dict.section_id('DIAGNOSIS_IP'),['ICD9_CODE:'+str(x) for x in icd9])
ip_diagnosis = rep.get_sig('DIAGNOSIS_IP',translate=False)
ip_diagnosis = ip_diagnosis[(lut[ip_diagnosis.val0]!=0)]
op_diagnosis = rep.get_sig('DIAGNOSIS_OP',translate=False)
op_diagnosis = op_diagnosis[(lut[op_diagnosis.val0]!=0)]
```



## Load MedModel and apply (predict) on sample

```python
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

## Learn model from json to generate matrix

```python
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
## Bootstrap analysis

```python
import pandas as pd
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
## Bootstrap analysis on samples

```python
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
## print errors in medPython

```python
print(med.cerr())
```
 
## Additional Examples

- See `$MR_LIBS/Internal/MedPyExport/examples/MedProcUtils/` for more Python implementations. [MR_LIBS](https://github.com/Medial-EarlySign/MR_libs) is git repository