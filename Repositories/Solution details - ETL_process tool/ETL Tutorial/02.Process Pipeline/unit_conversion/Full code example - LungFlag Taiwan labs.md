# Full code example
 
The scripts does:

1. Renaming of columns
2. date columns conversion
3. mapping of LABLOINC codes to signals using $CODE_DIR/configs/map.tsv file
4. Removing rows without "numeric" results 
5. Filtering null columns
6. removing "ignored" signal list that was mapped, but we don't need/want to load 
7. Cleaning prefix for "value" columns suffix like "(Manual checked)"
8. numeric conversion of values - removal of non numeric values
9. Transforming "unit" column and taking lowercase for unit
10. Calling unit conversion functions: `generate_labs_mapping_and_units_config`, map_and_fix_units

**$CODE_DIR/signal_processings/labs.py**
```python
 #You have dataframe called "df". Please process it to generare signal/s of class "labs"
#Example signal from this class might be BP
#The target dataframe should have those columns:
#    pid
#    signal
#    time_0 - type i
#    value_0 - string categorical (rep channel type s)
#    value_1 - string categorical (rep channel type s)
#Source Dataframe - df.head() output:
#     pid ACCOUNTIDSE2    ORDERTASKIDSE HOSPITALCODE EXEHOSPITALCODE DEPTCODE  ...    SPECIMENNO     SAMPLINGDATETIME SPECIMENTYPECODE RESULTUNIT                      REGULAREXPRESSIONDEFINEDRANGE  signal
#0   4728    A00015780  201301020010156           T0              T0      NaN  ...  130102903195  2013-01-02 10:31:04              BLO       g/dL  [0-14d]12.0-20.0 [15-30d]10.0-15.3 [31d-0.5y]8...    None
#1  39977    A00028394  201301310013839           T0              T0      NaN  ...  130131904446  2013-01-31 10:42:04              BLO         pg  [0-14d]31.1-35.9 [15-30d]29.9-35.3 [31d-0.5y]2...    None
#2  67616    A00036755  201302110003945           T0              T0      NaN  ...  130211062196  2013-02-11 14:49:22              BLO       g/dL  [0-14d]12.0-20.0 [15-30d]10.0-15.3 [31d-0.5y]8...    None
#3  23150    A00041791  201302220023413           T0              T0      NaN  ...  130222001672  2013-02-22 15:56:49              BLO          %  [0-14d]36.0-60.0 [15-30d]30.5-45.0 [31d-0.5y]2...    None
#4  11117    A00045620  201303040026380           T0              T0      NaN  ...  130304908805  2013-03-04 15:35:12              BLO          %                                                NaN    None
#
#[5 rows x 22 columns]
def clean_suffix(df, suffix):
    df['value_0']=df['value_0'].apply(lambda x: x.strip()[:-len(suffix)] if x.strip().endswith(suffix) else x)
    return df
df=df.rename(columns={'SAMPLINGDATETIME': 'time_0', 'CONFIRMRESULT': 'value_0'})
df['time_0']=df['time_0'].map(lambda x: x.split()[0].replace('-','')).astype(int)
df=df[['pid', 'time_0', 'value_0', 'RESULTUNIT', 'LABLOINC', 'ORIGINALLABORDERFULLNAME']]
#df[['LABLOINC', 'ORIGINALLABORDERFULLNAME']].groupby('LABLOINC').agg(['count','min']).reset_index().sort_values(('ORIGINALLABORDERFULLNAME', 'count'), ascending=False).to_csv('configs/maps.tsv', index=False, sep='\t')
map_labs=pd.read_csv(os.path.join('configs', 'map.tsv'), sep='\t', usecols=['LABLOINC', 'target']).set_index('LABLOINC')
df=df.set_index('LABLOINC').join(map_labs, how='left').reset_index().rename(columns={'target':'signal'}) #.drop(columns=['ORIGINALLABORDERFULLNAME'])
missing_map=len(df[df['signal'].isnull()])
if missing_map >0:
    print(f'missing codes {missing_map}')
df=df[['pid', 'signal', 'time_0', 'value_0', 'RESULTUNIT', 'LABLOINC']]
before_nana=len(df)
df=df[df['value_0'].notnull()].reset_index(drop=True)
if len(df)!=before_nana:
    print(f'Removed empty values. size was {before_nana}, now {len(df)}. Excluded {before_nana-len(df)}')
before_nana=len(df)
df=df[df.signal.notnull()].reset_index(drop=True)
if len(df)!=before_nana:
    print(f'Removed unmapped signals. size was {before_nana}, now {len(df)}. Excluded {before_nana-len(df)}')
before_nana=len(df)
ignore_labs=set(['CK-MB', 'Normobl', 'INR', 'IGNORE', 'PT', 'PTT', 'CK-isoenzyme'])
df=df[(~df.signal.isin(ignore_labs))].reset_index(drop=True)
if len(df)!=before_nana:
    print(f'Removed IGNORE signal. size was {before_nana}, now {len(df)}. Excluded {before_nana-len(df)}')
#Covert number
df=clean_suffix(df, '(Manual checked)')
df=clean_suffix(df, '(NRBC excluded)')
#extract number:
df['value_00']=pd.to_numeric(df.value_0.apply(lambda x: re.compile('^([0-9]+(\.[0-9]+)?)(\s.*)').sub(r'\1', x).strip()) ,errors='coerce')
    
df['has_num']=df['value_0'].apply(lambda x: len(re.compile('[0-9]').findall(x))>0)
print('Excluded values:')
print(df[~df['has_num']].value_0.value_counts())
before_nana=len(df)
df=df[df['has_num']].reset_index(drop=True)
if len(df)!=before_nana:
    print(f'Removed non numeric size was {before_nana}, now {len(df)}. Excluded {before_nana-len(df)}')
df=df.drop(columns=['has_num'])
    
print('Excluded more non numeric values:')
print(df[df['value_00'].isnull()].value_0.value_counts())
before_nana=len(df)
df=df[df['value_00'].notnull()].reset_index(drop=True)
if len(df)!=before_nana:
    print(f'Removed bad values size was {before_nana}, now {len(df)}. Excluded {before_nana-len(df)}')
df['value_0']=df['value_00']
df=df.drop(columns=['value_00'])
#Now handle units = > All looks good and in the same unit
df['RESULTUNIT']=df['RESULTUNIT'].astype(str).apply(lambda x: x.lower())
df=df.rename(columns={'RESULTUNIT': 'unit'})
#generate_labs_mapping_and_units_config(df, 5)
#Please edit the file "/mnt/earlysign/workspace/LungFlag/ETL/configs/map_units_stats.cfg" and then comment out previous line for speedup in next run
df=map_and_fix_units(df)
df=df.drop(columns=['signal.original', 'mapped'])
```
 
 
 
