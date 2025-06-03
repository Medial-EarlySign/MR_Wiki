# AlgoMarkers
## AlgoMarkers are wrappers to models or calculators that are able to "talk" to the AlgoAnalyzer via the API defined in AlgoMarker.h (the api funcs start with AM_API_... ). Since the AlgoAnalyzer uses the AlgoMarker as a DLL from a c# code, it is written is "C" style bare bones to allow for the integration.
This page describes the following:
- How to write a new AlgoMarker
- Compile the AlgoMarker DLL
- The MedialInfra AlgoMarker 
  - Configuration file
  - Eligibility rules configuration
- How to freeze a MedialInfra AlgoMarker
- How to test the AlgoMarker DLL
 
## How to write a new AlgoMarker
The AlgoMarker base class is in AlgoMarker.h in the AlgoMarker lib which is part of medial research libs git. So to work with it pull it from git first.
In order to write a new AlgoMarker one has to go through the following steps:
1. Write a new class that inherits from AlgoMarker (or from one of its derived classes), and make sure the following virtual functions are all filled:
  - virtual int Load(const char *config_f) : gets a config file (or NULL if you don't need one), and gets the AlgoMarker into a working state.
  - virtual int Unload()  : releases all allocated memory and closes
  - virtual int AddData(int patient_id, const char *signalName,  int TimeStamps_len, long long* TimeStamps, int Values_len, float* Values)
    - Adds data to the AlgoMarker which later could be used to ask scores for
    - Data is added per pid, for a specific signalName, and then 2 arrays giving the time and value channels. The order in each array is element by element and then each channel for each element.
  - virtual int ClearData() : Clear all data in the AlgoMarker
  - virtual int Calculate(AMRequest *request, AMResponses *responses)
    - Major API : once the AlgoMarker is loaded and has data, one can give it requests and get responses (=results).
    - To handle requests and responses one can check their classes and the example AlgoMarkers already implemented.
-1. Add a type to your new AlgoMarker in the enum AlgoMarkerType
0. Update the AlgoMarker::make_algomarker routine to support your new class
1. That's It !! compile and ready to go. NO NEED to touch any of the API routines - they only rely on the implementation of the 5 routines in (1).
 
## Compile The AlgoMarker DLL
The needed code is all inside the Libs git of Medial Research.
- For compilation to work one needs a correctly set up environment (visual studio version, paths, paths to statically compiled libraries, etc). These are defined elsewhere as these are not AlgoMarker specific.
- Pull the "Libs" git
- Compile all libs using the CompileLibs project
- Compile AlgoMarker as a DLL
- There are some direct unit tests in the AlgoMarker DLL project, one can compile and use them as well to test things (see below).
## The MedialInfra AlgoMarker
 
The MedialInfra AlgoMarker allows using any model that was trained using Medial MedProcessTools infrastructure. On top of that it allows also for some nice configuration of eligibility testing on input data, and is packaged with a configuration file that's easy to edit and work with.
### Configuration File
When Loading a new MedialInfra AlgoMarker a configuration file is given. The format of the general file is explained in the next example:
**Configuration File Example**
```
#################################################################################
# MedialInfra AlgoMarker config example file
#################################################################################
# comment lines start with #
# all (non comments) separators are tab
# type of AlgoMarker
# shoule be MEDIAL_INFRA for a MedialInfra AlgoMarker, otherwise will fail loading
TYPE	MEDIAL_INFRA
# name : One can get the name via the AM_API
NAME	PRE2D
# repository file configuration : to enable load of signal names and dictionaries, or optionally also data
REPOSITORY	thin.repository
# basic time unit for signals used in the specific marker (typically : Date for in patient, Minutes for out patient)
TIME_UNIT	Date
# model file for AlgoMarker , if name does not start with '/' the file position will be relative to the directory in which the config file was at
MODEL	pre2d.model
#################################################################################
# Eligibility
#################################################################################
# Following parts are optional: when defining eligibility rules
# if a file is given it will be used, if "." is the file name, then it means this config file contains also the filters definitions.
INPUT_TESTER_CONFIG	.
 
# each filter is in the following format:
# FILTER	<filter type>|<filter params>|<warning_or_error>|<use_for_max_outliers_flag>|<external_rc>|<internal_rc>|<err_msg>
# <filter type> : currently always 'simple' or 'attr'
# <filter params> : see examples below, and/or read documentation. Params should be separated with ';' .
# <warining_or_error>: values are WARNING or ERROR
# <use_for_max_outliers_flag>: ACC=1 or ACC=0 : state from which filters to accumulate the overall number of outliers
# <external_rc> : read code to return in the message case the test did not pass
# <internal_rc> : internal read code returned (another layer of error codes that is needed)
# <err_msg> : string - free text that will be returned as the error message in case the test did not pass.
# TESTER_NAME : mainly for debug prints etc...
TESTER_NAME	pre2d_tester
 
# example for a filter to force a minimal number of results in a certain time window (defualt given in days)
FILTER	simple|sig=Glucose;win_from=0;win_to=730;min_Nvals=2|ERROR|ACC=0|310|310|Not enough Glucose tests in the last 2 years
 
# example for a filter that forces also a maximal number of results for a signal
FILTER	simple|sig=GENDER;min_Nvals=1;max_Nvals=1|ERROR|ACC=0|310|310|Missing GENDER or more than 1 GENDER signal
 
# example for a filter that forces values to be in a given list (allowed_values)
FILTER	simple|sig=GENDER;allowed_values=1,3|WARNING|ACC=0|310|310|WARNING: GENDER Value Not 1 or 3
 
# example for an AGE filter (ages should be >= and <= the given range)
FILTER	simple|sig=AGE;min_val=50;max_val=60|WARNING|ACC=0|320|320|age not in range 50-60
 
# example for a filter that verifies that the values of a signal are defined in the repository dictionary (important for categorical signals)
FILTER	simple|sig=Drug;values_in_dictionary=1|ERROR|ACC=0|320|320|Drug code not in dictionary
 
# example for filters that check for a maximal number of outliers
FILTER	simple|sig=Glucose;win_from=0;win_to=3650;min_val=10;max_val=2000;max_outliers=3|ERROR|ACC=1|321|321|Too many glucose outliers
FILTER	simple|sig=HbA1C;win_from=0;win_to=3650;min_val=3;max_val=12;max_outliers=3|ERROR|ACC=1|321|321|Too many HbA1C outliers
# if the model has Glucose_nRem attributes we can create the following rule by testing it directly.
FILTER  attr|attr_name=Glucose_nRem;max=0|ERROR|ACC=0|321|321|Too many glucose outliers
 
# max outliers allowed when summing over all the ACC=1 filters
MAX_OVERLALL_OUTLIERS	1
```
 
## Eligibility rules configuration
Most of the options can be seen in the above example, here are the basics:
- Each filter is given in a line : FILTER <filter type>|<filter params>|<warning_or_error>|<use_for_max_outliers_flag>|<external_rc>|<internal_rc>|<err_msg>
- Currently <filter type> is always 'simple' or 'attr'
- <filter params> : see examples above and definitions below
- <warning_or_error> : one of WARNING or ERROR. A warning will run the test, report the problem if found, but not fail the example and still will give a score for it.
- 
<use_for_max_outliers_flag>: ACC=1 or ACC=0 : state from which filters to accumulate the overall number of outliers (MAX_OVERALL_OUTLIERS)
- 
<external_rc> : read code to return in the message case the test did not pass
- 
<internal_rc> : internal read code returned (another layer of error codes that is neededed
- 
<err_msg> : string - free text that will be returned as the error message in case the test did not pass.
 
Filter params is given in a string , separator is ';' and there should be no spaces/tabs. It has many options, see the class SanitySampleFilter to view them formally. 
## Parameters for simple filter type
- sig : name of the signal we want to test
- time_ch , val_ch : time and value channels to test signal with (defaults are 0 and 0)
- win_time_unit : default Days
- samples_time_unit: default Date
- min_val , max_val : min and max allowed values for a signal (>=min <=max) when testing for outliers.
- win_from, win_to : a time window before and relative to the sample in which we apply the test:
  - Each of the tests asked for will be done only on the signal results in the given time window.
  - Default is all the tests (infinite window to the past)
- min_Nvals, max_Nvals : test min or max number of values (ALL values not just those in a given range if one is given) for the given signal and window.
- max_outliers : maximal allowed number of outliers for the signal in the given time window
- min_left : minimal number of results left after throwing the outliers.
- allowed_values : list of values , seprated by comma (',') . Test verifies that all values (in the given window) are one of the given allowed values.
- values_in_dictionary : if =1 (default 0) , will test that all the values of the signal are valid values in the repository dictionary. Useful for categorical data such as Drug or RC.
A filter can be configured to do one simple test, or several. As explained above many filters can be defined. All filters defined will run on every point (pid,timepoint pair) , and all the filters that did not pass will push their error message into the relevant response messages. For cases in which the sample did not pass a filter defined as ERROR , the AlgoMarker will not generate a score. However for cases which only had warnings, it will.
 
## Parameters for attribute ('attr') filter type
To set this filter use 'attr' in filter type (see example above).
The use of this filters relies on the fact the model was built with an option to create those attributes and inject them into the resulted MedSamples object at prediction time. The classical use is to let cleaners and testers running in the model to report their results this way. Formally these actions will add an attribute to each prediction, and the filter defined here is able to create rules based on those attributes.
Parameters:
- name : the name of the attribute to test
- max : the maximal value allowed. An error or warning will be given for any value larger than this.
 
To make sure a model creates those attributes it is needed to make it do so in its json definition.
- To a basic cleaner ( "rp_type": "basic_cln" in json) add : "nrem_attr": "nRem","ntrim_attr": "nTrim",   in order to get an attribute of the number of removed signals, and/or trimmed ones. Note this counts the total number and not in a specific time window....
- To force a panel use for example:
  - {"action_type":"rep_processor","rp_type":"req","signals":"Hemoglobin,RBC,Hematocrit", "win_from": "0", "win_to": "365"},
  - this will count how many of the panel signals are missing in the given time window (relative to prediction point). Note that if placed AFTER cleaners (reccomended) it will test this on the cleaned data that may have some values removed.
## How to freeze a MedialInfra AlgoMarker Version
1. If using a non frozen libraries version:
  
1. Either create a branch with a suitable name for your freeze for the Libs git OR
  
2. Tag your version in the branch you want to work with.
  
3. It is reccomended to freeze also code for Tools git, and code for releavant projects (for example the Diabetes git project for a diabetes algomarker, etc).
  
4. When freezing several different gits, make sure to tag all of them with the same tag.
  
5. Document your freeze and branches/tags names.
5. Make sure you have everything prepared:
  
1. A model file trained for the AlgoMarker. Better test this very algomarker gives the expected results on your test set, and runs with the frozen libraries version.
  
2. The repository files you were working with: main needed:
    
1. the .repository file
    
2. the .signals file
    
3. the dictionary files for the signals you are using.
2. Create a new directory, call it with the agreed upon algomarker+version name
3. Put there:
  
1. The algomarker model file
  
2. The repository files used
  
3. Prepare an algo marker config file as explained above
    
1. Make sure the eligibility rules are the ones you want.
  
1. Good time to run a small unit-test here to see it loads, runs and gives expected results on some prepared data set.
1. Zip directory.
 
## How to test the AlgoMarker DLL
The AlgoMarker project includes the DllAPITester, which can be used to test the DLL and compare its output to scores given by the Flow app. 
**DllAPITester Help**
```
> $MR_ROOT/Libs/Internal/AlgoMarker/Linux/Release/DllAPITester --h
Reading params
Program options:
  --help                                produce help message
  --rep arg (=/home/Repositories/THIN/thin_mar2017/thin.repository)
                                        repository file name
  --samples arg                         medsamples file to use
  --model arg                           model file to use
  --amconfig arg                        algo marker configuration file
  --direct_test                         split to a dedicated debug routine
  --test_data arg                       test data for --direct_test option
  --date arg (=20180101)                test date
  --egfr_test                           split to a debug routine for the simple
                                        egfr algomarker
```
After compiling, it can be used as follows:
**Example Run**
```
./Linux/Release/DllAPITester --rep /home/Repositories/THIN/thin_jun2017/thin.repository --samples /server/Work/Users/Tal/Temp/test.samples --model /server/Products/Pre2D/QA_Versions/1.0.0.1/pre2d.model --amconfig /server/Products/Pre2D/QA_Versions/1.0.0.1/pre2d.amconfig
```
The tester will compare the scores given by both methods and will return passed/failed. For example:
**Example Output**
```
...
#Res1 :: pid 5000529 time 20060308 pred 0.135475 #Res2 pid 5000529 time 20060308 pred 0.135475
#Res1 :: pid 5000529 time 20060315 pred 0.090177 #Res2 pid 5000529 time 20060315 pred 0.090177
#Res1 :: pid 5000529 time 20060818 pred 0.111277 #Res2 pid 5000529 time 20060818 pred 0.111277
#Res1 :: pid 5000529 time 20070907 pred 0.085166 #Res2 pid 5000529 time 20070907 pred 0.085166
#Res1 :: pid 5000529 time 20080225 pred 0.103451 #Res2 pid 5000529 time 20080225 pred 0.103451
#Res1 :: pid 5000529 time 20080411 pred 0.075562 #Res2 pid 5000529 time 20080411 pred 0.075562
#Res1 :: pid 5000529 time 20090324 pred 0.132835 #Res2 pid 5000529 time 20090324 pred 0.132835
#Res1 :: pid 5000529 time 20110124 pred 0.170343 #Res2 pid 5000529 time 20110124 pred 0.170343
Comparing 99 scores
>>>>>TEST1: test DLL API batch: total 99 : n_similar 81 : n_bad 0 : n_miss 18
PASSED
```
 
Another option is running a direct test (note the self explanatory test_data format):
**Testing a single example directly**
```
Linux/Release/DllAPITester --rep /home/Repositories/THIN/thin_jun2017/thin.repository --amconfig /nas1/Products/Pre2D/QA_Versions/dev/pre2d.amconfig --direct_test --test_data "Glucose:120:20171101;GENDER:1;BYEAR:1988" --date 20180520
```
and get the result :
**Single test result**
```
...
Algomarker Pre2D was loaded with config file /nas1/Products/Pre2D/QA_Versions/dev/pre2d.amconfig
Adding Data: sig Glucose :: vals: 120.000000,  times: 20171101,
Adding Data: sig GENDER :: vals: 1.000000,  times:
Adding Data: sig BYEAR :: vals: 1988.000000,  times:
Creating Request
Before Calculate
...
...
Shared Messages: 0
Got 1 responses
Getting response no. 0
Response Messages: 0
Score 0 Messages: 0
resp_rc = 0
i 0 , pid 1 ts 20180520 scr 0.272233
ptr for _scr_type 5288768
_scr_type Raw
Finished debug_me() test
```
 
 
 
 
