# AlgoMarker Testing
## The new way to generate JSON:
The tool AMApiTester can now generate request/response JSON files which can be used by the AlgoAnalyzer.
It is done by providing --json-reqfile and --json-resfile in the commandline. These options currently work only with the --single testing mode. 
To use it you should execute the command normally and provide req/req file names to output the JSON data to, for example:

```bash
./AMApiTester \
  --amfile /nas1/Products/LGI-ColonFlag-3.0/QA_Versions/LGI_3.1.0.0/libdyn_AlgoMarker.25102018_1.so \
  --single --print_msgs \
  --rep $REP \
  --samples ./samples/LastHg.samples \
  --model /nas1/Products/LGI-ColonFlag-3.0/QA_Versions/LGI_3.1.0.0/LGI-Flag-3.1.model \
  --amconfig /nas1/Products/LGI-ColonFlag-3.0/QA_Versions/LGI_3.1.0.0/LGI-Flag-3.1.amconfig \
  --am_res_file ./res/LGI_test_am.preds \
  --med_res_file ./res/LGI_test_med.preds \
  --json-reqfile ./res/LGI_test_req.json \
  --json-resfile ./res/LGI_test_res.json
```
The JSON generating is done in a library project called AlgoMarker/CommonTestingTools.
## ApplyTool
ApplyTool is another tool with JSON capabilities. This toold is the result from the work with ShareCare. it can:

```bash
# 1. Convert JSON reqfile to a tab-separated repository data file:
/nas1/UsersData/shlomi/MR/Libs/Internal/AlgoMarker/Linux/Release/ApplyTool --convert_reqfile_to_data --convert_reqfile_to_data_infile ./long_req.json --convert_reqfile_to_data_outfile ./long_req.data
 
# 2. Drectly feed JSON request data directly into a given AlgoMarker and get the results (.preds)
/nas1/UsersData/shlomi/MR/Libs/Internal/AlgoMarker/Linux/Release/ApplyTool \
--rep /nas1/Work/CancerData/Repositories/KP/kp.repository \
--model /nas1/Products/LungCancer/QA_Versions/lc_2_300719/lungcancer.model \
--apply \
--apply_repdata_jsonreq ./long_req.json \
--apply_dates_to_score ./long_req.samples.tsv \
--apply_outfile ./long_req_from_json.pred
```
 
## The old way (–msgs_file + python scripts)
The old way to create and test JSON req files involved using AMApiTester with additional commands --print_msgs --msgs_file TSV_Codes_file.The AMApiTester is being ran as usual but the error codes that the Algomarker emits will be saved into the file specified by --msgs_file . for example:

```bash
./Linux/Release/AMAPITester 
  --rep /home/Repositories/THIN/thin_jun2017/thin.repository 
  --samples /nas1/Work/Shared/notebooks/shlomi-internal/AATester/pre2d_validate_OnTest_2-10k.samples 
  --model /server/Products/Pre2D/QA_Versions/1.0.0.10/pre2d.model 
  --amconfig /server/Products/Pre2D/QA_Versions/1.0.0.10/pre2d.amconfig 
  --print_msgs 
  --msgs_file /nas1/Work/Shared/notebooks/shlomi-internal/AATester/pre2d_validate_OnTest_2-10k.codes.tsv 
  --ignore_sig Drug 
  --single 
  --am_res_file /nas1/Work/Shared/notebooks/shlomi-internal/AATester/pre2d_validate_OnTest_2-10k.preds.tsv
```

 Then we will use a python script as follows to convert the codes+preds files into json:
(also available as notebook in here: [http://node-04:9000/user/shlomi-internal/notebooks/shlomi-internal/AATester/Phase1.ipynb](http://node-04:9000/user/shlomi-internal/notebooks/shlomi-internal/AATester/Phase1.ipynb))
Note: the conf object contains script configuration you may change for your specific settings.

```python
import json
import med
import pandas as pd
import numpy as np
test_tag = '800k'
conf= {
    'x_api_key': 'NzlldZ#QwZGVmNTY4ZmUwZjczZT1MTl2',
    'customer_id':'Earlysign',
    'aa_version': '1.1.2.2',
    'calculator_name': 'Pre2D',
    'calculator_result_unit': None,
    'repository' : '/home/Repositories/THIN/thin_jun2017/thin.repository',
#    'preds_infile' : 'pre2d-oldmodel-{}.preds.tsv'.format(test_tag),
#    'codes_infile' : 'pre2d-oldmodel-{}.codes.tsv'.format(test_tag),
#    'preds_infile' : 'pre2d_validate_OnTest_2-{}.preds.tsv'.format(test_tag),
#    'codes_infile' : 'pre2d_validate_OnTest_2-{}.codes.tsv'.format(test_tag),
    'preds_infile' : './data_files2/pre2d_validate-{}.preds.tsv'.format(test_tag),
    'codes_infile' : './data_files2/pre2d_validate-{}.codes.tsv'.format(test_tag),
    'skipped_outfile' : './data_files2/pre2d_validate-{}.skipped.tsv'.format(test_tag),
#    'requests_outfile' : 'pre2d_validate_OnTest_2-requests-{}.json'.format(test_tag),
#    'responses_outfile' : 'pre2d_validate_OnTest_2-responses-{}.json'.format(test_tag),
    'requests_outfile' : './data_files2/pre2d_validate-requests-{}.json'.format(test_tag),
    'responses_outfile' : './data_files2/pre2d_validate-responses-{}.json'.format(test_tag),
    'signals' : 'GENDER HDL BYEAR ALT Triglycerides WBC HbA1C BMI Glucose'.split(' ')  # no Drug sig for now
    # signals for lgi : 'Monocytes# Basophils% Eosinophils% RDW Platelets Eosinophils# MCHC-M MCH MCV MPV RBC Hematocrit Basophils# GENDER Neutrophils# Hemoglobin Neutrophils% BYEAR Lymphocytes% Lymphocytes# WBC Monocytes%'.split(' ')
}
code_to_status_tbl = {
    300:2,
    301:2,
    310:2,
    311:2,
    320:1,
    321:2,
    390:0,
    391:1,
    392:2
}
units_tbl = {
    'BMI' : 'kg/m^2',
    'Glucose' : 'mg/dL',
    'HbA1C' : '%',
    'HDL' : 'mg/dL',
    'Triglycerides' : 'mg/dL',
    'ALT' : 'U/L',
    'RBC' : '10^6/uL',
    'Na' : 'mmol/L',
    'Weight' : 'Kg',
    'WBC' : '10^3/uL',
    'Basophils#' : '#',
    'Basophils%' : '%',
    'Eosinophils#' : '#',
    'Eosinophils%' : '%',
    'Hematocrit' : '%',
    'Hemoglobin' : 'g/dL',
    'Lymphocytes#' : '#',
    'Lymphocytes%' : '%',
    'MCH' : 'pg/cell',
    'MCHC-M' : 'g/dL',
    'MCV' : 'fL',
    'Monocytes#' : '#',
    'Monocytes%' : '%',
    'MPV' : 'mic*3',
    'Neutrophils#' : '#',
    'Neutrophils%' : '%',
    'Platelets' : '10^3/uL',
    'RDW' : '%',
    'MSG' : '#'
}
def encode_pid_signal_data(signame, unit='', datapoints=[]):
    data = {}
    data['code'] = signame
    if unit=='' and signame in units_tbl:
        unit = units_tbl[signame]
    data['unit'] = unit
    data['data'] = datapoints;
    return data
def encode_signal_datapoint(timestamps, values):
    return {'timestamp' : timestamps, 'value' : values}
def req_excapsulate(orig_req, x_api_key):
    return {
        'body': orig_req,
        'header': {
            "Accept": "application/json",
#            "x-api-key": x_api_key,
            "Content-Type": "application/json"
        }
    }
def encode_request(request_id='',customer_id='Earlysign',pid=None,calculator='',signals=[], x_api_key=''):
    req = {}
    req['requestId'] = request_id
    req['customerId'] = customer_id
    if pid!=None: req['patientId'] = pid
    req['calculator'] = calculator
    req['signals'] = signals
    return req_excapsulate(req, x_api_key)
def now_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d%H%M%S")
#generate results
def encode_response(request_id='', version='1.1.0', calculator='', customer_id='Earlysign',
                    status=0, result=None, calculation_time_stamp="", messages=[], accountId="TestAccount"):
    return {
        "requestId": request_id,
        "version": version,
        "calculator": calculator,
        "customerId": customer_id,
        "accountId": accountId,
        "status": status,
        "result": result,
        "calculationTimeStamp": str(calculation_time_stamp),
        "messages": messages
    }
def result_value_format(fval):
    if '.' in str(fval) and str(fval).replace('.','',1).isdigit(): 
        return ("%.4f" % float(fval)).rstrip('0').rstrip('.')
    else: return fval
def encode_result(date, value, result_type='Numeric', unit=None, status=0):
    if status == 2: return None
    return { 
        "resultType": result_type,
        "unit": unit,
        "value": str(result_value_format(value)),
        "validTime": date*1000000
    }
def encode_messages(code, text, status):
    return {
        "code" : code,
        "text": text,
        "status" : status
    }
def value_format(fval):
    if '.' in str(fval) and str(fval).replace('.','',1).isdigit(): 
        return ("%.3f" % float(fval)).rstrip('0').rstrip('.')
    else: return fval
 
# Load Repository
rep = med.PidRepository()
rep.read_all(conf['repository'],[],['GENDER'])
print(med.cerr())
 
#load preds
preds_df = pd.read_table(conf['preds_infile'])
preds_df = preds_df.drop(['EVENT_FIELDS','outcome','outcomeTime','split'],axis=1) #.set_index(['id'])
preds_df = preds_df.rename(columns={'pred_0':'result'})  
#load codes
codes_df = pd.read_table(conf['codes_infile'])
codes_df.columns = ['msg_type','pid','date','i','j','k','code','msg_text']
codes_df = codes_df[codes_df['msg_type'] != 'SharedMessages']
codes_df = codes_df.drop(['msg_type','i','j','k'], axis=1)
 
pids = preds_df['id'].unique().astype(np.int32)
 
#load signals
signals={}
for signal_name in conf['signals']:
    signals[signal_name] = rep.get_sig(signal_name, pids=pids).set_index('pid')
 
req_data = []
resp_data = []
req_id_count=0
now_ts = now_timestamp()
resp_file = open(conf['responses_outfile'], 'w')
req_file = open(conf['requests_outfile'], 'w')
resp_file.write('[\n')
req_file.write('[\n')
skipped_samples=[]
for pred_index,pred_row in preds_df.iterrows():
    pid, pred_time, pred_result = int(pred_row['id']), int(pred_row['time']), pred_row['result']
    if pred_time % 100 == 0: 
        skipped_samples.append([pid,pred_time])
        continue;
    skip_cur_pid = False
    pid_signals_data = []
    #pid_data = []
    request_id='req_{}_{}_{}'.format(req_id_count, pid, pred_time)
    #generate request
    for sig_name,sig_df in signals.items():
        if pid in sig_df.index:
            datapoints = []
            for index, row in sig_df.loc[pid:pid].iterrows():
                values = []
                timestamps = []
                row_is_future = False
                for col_name,col_val in  row.iteritems():
                    if 'val' in col_name: values.append(value_format(col_val))
                    elif 'date' in col_name or 'time' in col_name:
                        if int(col_val) > pred_time: 
                            row_is_future = True
                            break
                        if int(col_val) % 100 == 0:
                            skip_cur_pid = True
                            skipped_samples.append([pid,pred_time])
                            break
                        timestamps.append(int(col_val))
                    else: raise Exception("unknown column name '{}'".format(col_name))
                if not row_is_future: datapoints.append(encode_signal_datapoint(timestamps=timestamps, values=values))
                if skip_cur_pid: break
            pid_signals_data.append(encode_pid_signal_data(signame=sig_name, datapoints=datapoints))
        if skip_cur_pid: break
    if skip_cur_pid: continue;
    #pid_signals_data.append(pid_data)
    pid_req = encode_request(request_id=request_id,
                             customer_id=conf['customer_id'],calculator=conf['calculator_name'],
                             signals=pid_signals_data,x_api_key=conf['x_api_key'])
    #generate resoponse
    messages = []
    status = 0
    for row in codes_df[(codes_df['pid']==pid) & (codes_df['date']==pred_time)].iterrows():
        row = dict(row[1])  
        msg_status = code_to_status_tbl[row['code']]
        status = max(status, msg_status)
        messages.append(encode_messages(code=row['code'], text=row['msg_text'], status=msg_status))
    resp_data = encode_response(request_id=request_id, calculator=conf['calculator_name'],
                    result=encode_result(date=pred_time, value=pred_result, result_type='Numeric', unit=conf['calculator_result_unit'], status=status),
                    messages=messages, status=status, calculation_time_stamp=now_ts,version=conf['aa_version']
                   )
    if req_id_count != 0:
        resp_file.write('\n,\n')
        req_file.write('\n,\n')
    #req_data.append(pid_req)
    json.dump(pid_req, req_file, sort_keys=False, indent=1)
    json.dump(resp_data, resp_file, sort_keys=False, indent=1)
    req_id_count += 1
    if req_id_count % 1000 == 0:
        print("request # {}".format(req_id_count))
resp_file.write('\n]')
req_file.write('\n]')
resp_file.close()
req_file.close()
print("skipped {} samples".format(len(skipped_samples)))
 
```
 
## Insert JSON req files into the DB to be used by AA
Once you have JSON req/res files you may want to insert them into a SQL DB so it can be used by AA. The following python script takes the JSON files and stores then in the DB:
(also available here: [http://node-04:9000/user/shlomi-internal/notebooks/shlomi-internal/AATester/Phase1-DB-insert.ipynb](http://node-04:9000/user/shlomi-internal/notebooks/shlomi-internal/AATester/Phase1-DB-insert.ipynb))
Note: the conf object contains script configuration you may change for your specific settings.

```python
import json
import med
import pandas as pd
import numpy as np
import sqlalchemy as sa
test_tag = '800k'
conf= {
#    'requests_infile' : 'pre2d_validate_OnTest_2-requests-{}.json'.format(test_tag),
#    'responses_infile' : 'pre2d_validate_OnTest_2-responses-{}.json'.format(test_tag),
    'requests_infile' : './data_files2/pre2d_validate-requests-{}.json'.format(test_tag),
    'responses_infile' : './data_files2/pre2d_validate-responses-{}.json'.format(test_tag),
    'db_name':'ObjectStore',
    'db_user':'postgres',
    'db_table':'Test',
    'epic_flag': 'avi800k'
}
resp_file = open(conf['responses_infile'], 'r')
req_file = open(conf['requests_infile'], 'r')
dummy = req_file.readline()
dummy = resp_file.readline()
 
def get_sql_engine(SQL_SERVER, DBNAME,  username='', password=''):
    if SQL_SERVER == 'MSSQL':
        return create_mssql_engine(DBNAME, username, password)
    elif SQL_SERVER == 'POSTGRESSQL':
        return create_postgres_engine(DBNAME, username, password)
    elif SQL_SERVER == 'D6_POSTGRESSQL':
        return create_postgres_url(DBNAME, username, password)
    print(SQL_SERVER + ' Unkowen source')

def load_json_obj(jsonfile):
    jstr=''
    line=jsonfile.readline().rstrip()
    if not line or line == ']': return None
    while line and line != ',' and line != ']':
        jstr += line + '\n'
        line=jsonfile.readline().rstrip()
    try:
        return json.loads(jstr)
    except:
        print(jstr)
        raise
def create_postgres_engine(dbname, username, password):
    engine = sa.create_engine('postgresql://'+username+':'+password+'@node-03:5432/'+dbname)
    return engine
 
engine = get_sql_engine('POSTGRESSQL',DBNAME=conf['db_name'],username=conf['db_user'])
# create table
meta = sa.MetaData(engine)
table = sa.Table(conf['db_table'], meta,
    sa.Column('Id', sa.String),
    sa.Column('TestId', sa.String),
    sa.Column('ExpectedHTTPStatus', sa.Integer),
    sa.Column('Request', sa.String),   #sa.dialects.postgresql.JSON),
    sa.Column('ExpectedResponseBody', sa.String)) #, sa.dialects.postgresql.JSON))
conn = engine.connect()
 
def req_excapsulate(orig_req, x_api_key='NzlldZ#QwZGVmNTY4ZmUwZjczZT1MTl2'):
    return orig_req
    return {
        'body': orig_req,
        'header': {
            "Accept": "application/json",
#            "x-api-key": x_api_key,
            "Content-Type": "application/json"
        }
    }
req, resp = req_excapsulate(load_json_obj(req_file)) , load_json_obj(resp_file)
i=0
data=[]
while req!=None and resp != None:
    #print(i,req['requestId'])
    i += 1
    if req['body']['requestId'] != resp['requestId']:
        raise Exception('Error - NON MATCHING REQ IDs {} != {}'.format(req['body']['requestId'],resp['requestId']))
    requestId = req['body']['requestId']

    data.append({
        'Id':requestId,
        'TestId':requestId,
        'ExpectedHTTPStatus':200,
        "Request" : json.dumps(req, sort_keys=False, indent=0).replace('\n',''),
        "ExpectedResponseBody" : json.dumps(resp, sort_keys=False, indent=0).replace('\n',''),
        "Epic" : conf['epic_flag']
    })

    if len(data)>=1000:
        res = conn.execute(table.insert(),data)
        print('{} rows inserted (+{})'.format(i, res.rowcount))
        data=[]

    req, resp = req_excapsulate(load_json_obj(req_file)) , load_json_obj(resp_file)
if len(data)>0:
    res = conn.execute(table.insert(),data)
    print('{} rows inserted (+{})'.format(i, res.rowcount))
    data=[]
```
 
 
 
 
 
