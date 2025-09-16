# Using Flow To Prepare Samples and Get Incidences
The Flow app contains useful tools to choose samples for a problem given a cohort, to filter the samples, and to match them (say for calendar year). These are powerful and useful tools needed to be done before preparing samples files for training/validation , or when needing to match populations on some parameters.
It also contains options to estimate incidences and get incidence files that can be used later for bootstrap analysis.
At the moment these are written and verified for the date case... and should be generalized and tested for in patient modes and other time scales.

## Cohort Files
Cohort files contain one line per pid , and define the time the patient entered the cohort, the time it left it, and if it has an outcome also the the oucome time and its value. This is a full definition of all the patients we want to use for training and testing and the times they are eligible for using.
The format of a cohort file is:

- tab delimited
- lines starting with '#' are comments
- the following 5 fields in each line:
    - pid : (only one like per pid is supported at the moment)
    - entry date to cohort
    - end date in cohort
    - outcome date : in binary cases for 0 outcomes (controls) it will be the same as end date, and for 1 outcomes it will be the actual event date which must be <= the end date.
    - outcome : typically a 0/1 control/case outcome, but can be also a regression value, or a multicategory value, but currently only a single value (should be generalized to an outcome vector in the future).
Example for a few lines of a cohort file:
**Cohort file example**
```
# note in the following sample: pid 5000009 entered the cohort on 20060505, left on 20091023 , but got a 1.0 (case) outcome at 20091023
5000009 20060505        20091023        20060605        1.000000
# in the following sample: pid 5000014 is a control (0.0 outcome) that entered the cohort on 20150107 and left it on 20160929
5000014 20150107        20160929        20160929        0.000000
5000017 20110826        20160819        20160819        0.000000
5000020 20140731        20161117        20161117        0.000000
5000025 20141125        20160916        20160916        0.000000
5000027 20060914        20161115        20161115        0.000000
5000040 20080422        20160223        20160223        0.000000
5000042 20060522        20140910        20140910        0.000000
5000043 20080613        20100609        20100609        0.000000
5000044 20110114        20160510        20150109        1.000000
5000059 20120501        20120515        20120515        0.000000
5000061 20140408        20160425        20160425        0.000000
5000073 20100219        20160422        20160422        0.000000
5000077 20090915        20111109        20111109        0.000000
```
 
## Creating a Sample file given a cohort file
The Flow line to use is:
Flow --rep <repository> --seed <random seed> --cohort_fname <cohort file> --cohort_sampling <cohort sampling parameters> --out_samples <output samples file>
All parameters are self explanatory except cohort_sampling , which we explain below:
cohort_sampling contains a rich list of parameters to decide how to create samples (for control and cases) using the cohort: which dates to sample, continous or on-test, frequency of sampling, time window relative to end date and/or outcome date, and more. Follows is a description of the options and their defaults

- min_control_years : (0) : minimal number of years for sampling before outcome for controls , controls are always those for which outcome == 0 , can be a float number (0.5 year etc)
- max_control_years : (10) : maximal number of years for sampling before outcome for controls
- min_case_years : (0) : minimal number of years for sampling before outcome for cases , cases are always those for which outcome != 0
- max_case_years : (1) : maximal number of years for sampling before outcome for cases
- is_continous : (1) : continous mode of sampling vs. stick to (0 = stick) (stick is on test)
- min_days_from_outcome : (30) : minimal number of days before outcome to sample
- jump_days : (180) : days to jump between sampling periods, meaning a sample will be randomly selected each jump_days period
- min_year : (1900) : min year for sampling
- max_year : (2100) : max year for sampling
- gender_mask : (3) : mask for gender specification (rightmost bit on for male, second for female) : 1 - only males , 2 - only females , 3 - both
- int train_mask : (7) : mask for TRAIN-value specification (three rightmost bits for TRAIN = 1,2,3)
- min_age : (0) : minimum age for sampling
- max_age : (200) : maximum age for sampling
- stick_to_sigs : : a list of signals (, separated) : only use time points with at least one of the given signals
- take_closest  : (0) : flag: take the sample with stick signals that is closest to each target sampling-date
- take_all : (0) : flag: take all samples with stick signal within each sampling period 
- max_samples_per_id : (2^31-1) : maximal number of samples per id
- max_samples_per_id_method : ('last') : 'last' or 'rand'. 'last' picks the last  max_samples_per_id samples, while 'rand' chooses them randomly
 
**Creating samples from cohort examples**
```bash
# choose continous sampling, a random sample in each 180 days window, 
# for controls choose from 1 year before end of cohort up to 10 years before
# for cases choose from outcome date up to 2 years before
# choose only for cases with TRAIN=1 , and in ages 35-90 at the time of sampling
SAMPLING_PARAMS1="min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=1;min_age=35;max_age=90"
 
# same as the above but on-test case and taking only samples at the days either a Glucose or HbA1C test was made
SAMPLING_PARAMS1="min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=1;min_age=35;max_age=90;is_continous=0;stick_to_sigs=Glucose,HbA1C"
 
# actual command line : replace SAMPLING_PARAMS with one of the options above
Flow --rep /home/Repositories/THIN/thin_mar2017/thin.repository --seed 123 --cohort_fname ./pre2d.cohort --cohort_sampling ${SAMPLING_PARAMS} --out_samples ./temp.samples
```
 
## Filter and Match options
This Flow option allows one to start from a samples file (typically one that was created using the cohort_sampling method explained above) , apply filters and/or matching procedures on it and create a new samples file.
The Flow line to use is:
Flow --rep <rep> --seed <random_seed> --filter_and_match --in_samples <input samples file> --out_samples <output samples file> --filter_params <filter params> --match_params <match params>
This run will run first the filtering (if given), and then the matching (if given)
Again : all params are obvious besides filter and match params, explained below:
### Filter params
Filtering options allow for taking samples only within a defined dates range, and also filter using ranges of signals in a window before the time point (say take only time points with Creatinine values below 1.1 in the 2 years before the time point, etc...)

- min_sample_time : (0) :minimal allowed time (should always be given in the samples' time-unit, in our case typically date)
- max_sample_time : ((1<<30)) : maximal allowed time (should always be given in the samples' time-unit : in our case typically date)
- win_time_unit: ("Days") :  ///< time unit to be used in bfilter windows
- bfilter : : a filter that checks conditions on a signal. Several filters can be defined. Parameters for filters (',' separated rather than ';') are:
    - sig_name : : Name of signal to filter by
    - win_from : (0) : Time window for deciding on filtering - start (relative to sample time, and going backwards)
    - win_to : ((1<<30)) : Time window for deciding on filtering - end
    - min_val : (-1e10) : Allowed values range for signal - minimum
    - max_val : (1e10) : Allowed values range for signal - maximum
    - min_Nvals (1) : Required number of instances of signal within time window
    - time_channel (0) :  signal time-channel to consider
    - val_channel (0) : signal value channel to consider
- min_bfilter : how many bfilters need to pass in order to take sample (default : all) , this allows for example to define a choice of one out of several signals to be before the sample and not all of them.
 
**Filter params examples**
```bash
# take only samples in the range 20070101 - 20150101
FILTER1="min_sample_time=20070101;max_sample_time=20150101"
 
# take only samples that have at least 1 Creatinine test up to 2 years before
# note that we use , and not = when stating the bfilter params. The = is kept for the upper level.
FILTER2="bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1"
 
# same as FILTER2 but also force all Creatinine tests to be below 0.9
FILTER3="bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1,min_val=0,max_val=0.9"
 
# combined: range 20070101-20101201 , At least one Glucose in last 2Y, all Glucose tests in last 5Y below 100, all HbA1C tests in last 5Y below 5.7
FILTER4="min_sample_time=20070101;max_sample_time=20101201;bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,Creatinine,win_from,0,win_to,1825,min_val,0,max_val,100;bfilter=sig,HbA1C,win_from,0,win_to,1825,min_val,0,max_val,5.7"
```
 
### Matching params
The matching option allows to take a MedSamples , and apply matching methods that make sure that the ratio between case and control is kept in various stratas. For example: one could match for years, which means that in each calendar year we will seek to have the same ratio of cases to controls, this when given as a training samples file will make the predictor "blind" to the calendar year, and learn features not correlated with it. Another example : we could match for Gender, or Age, or a value of some signal , or a combination of those, which will define stratification bins, and we will seek to find a subset of the input samples that has the same ratio od cases vs controls in all those bins.
The algorithm used is trying to find an optimal solution in the sense of leaving the maximal number of samples possible after the match. However it does so in a weighted manner between cases and controls, we can give a weight W signaling that we are willing to seek the best solution under the assumption that we allow to throw W controls instead of a single case. This helps keeping the cases in the matched samples when we have a low proportion of cases.

- priceRatio : (100.0) : the weight ratio: how many controls are we willing to lose for each case (good guess for this number would be at the order of n_controls/n_cases in the input samples)
- maxRatio : (10.0) : if the optimal ratio found by the matching algorithm is larger than maxRatio, we will sample less (enriching cases vs. control even more)
- verbose: (0) : get more prints from algorithm (recommended...)
- match_to_prior - specify the target prior directly
- strata : : add stratification criterias (':' delimited between ), strata parameters (',' delimited) are:
    - type: one of time , age , gender , signal
    - signalName : 
        - for time type: year , month, days , etc
        - for age : none
        - for gender : none
        - for signal : the signal name (Creatinine, Glucose, etc)
    - resolution : size of bin to stratify with
**Match params examples**
```bash
# change price and max ratio, run verbose
# add matching and stratification by years
MATCH1="priceRatio=10;maxRatio=4.5;verbose=1;strata=time,year,1"
# add matching and stratification by years to certain prior - in this example 0.1 which is 10%
MATCH1="match_to_prior=0.1;maxRatio=4.5;verbose=1;strata=time,year,1"
# same with gender stratification
MATCH2="priceRatio=10;maxRatio=4.5;verbose=1;strata=gender"
 
# same with age in bins of 5 years
MATCH3="priceRatio=10;maxRatio=4.5;verbose=1;strata=age,5"
 
# same : combining all 3 previous stratas, matching for all of them together
MATCH4="priceRatio=10;maxRatio=4.5;verbose=1;strata=age,5:time,year,1:gender"
 
# same : match by Glucose values in bin of 10 and HbA1C values in bins of 1.0
MATCH5="priceRatio=10;maxRatio=4.5;verbose=1;strata=signal,Glucose,10:signal,HbA1C,1.0"
 
```
more details in here: [MatchingSampleFilter](../../Infrastructure%20C%20Library/MedProcessTools%20Library/SampleFilter/MatchingSampleFilter.md)
## Get Incidence for a cohort
In order to get an incidence file for a cohort one can use the following Flow line:
Flow --rep <repository> --cohort_incidence "from_year=2007;to_year=2014;from_age=40;to_age=80;age_bin=40;incidence_days_win=1825" --cohort_fname <cohort file> --cohort_incidence <incidence parameters> --out_incidence <incidence file created> --censor_reg <censor registry> --use_kaplan_meir 1 
The cohort_fname and censor_reg are MedRegistry Objects. there is simple convert command from MedCohort to MedRegistry/
convert command:
```bash
cat <cohort file> | awk '{ if ($NF > 0) { print $1 "\t" $2 "\t" $4 "\t" "0";  print $1 "\t" $4 "\t" $3 "\t" "1" } else { print $1 "\t" $2 "\t" $3  "\t" "0" } }' #Creates MedRegistry from MedCohort
cat <cohort file> | awk '{ if ($NF > 0) { print $1 "\t" $2 "\t" $4 "\t" "1" } else { print $1 "\t" $2 "\t" $3  "\t" "1" } }' #creates Censor registry from MedCohort
```
 
### Incidence parameters (provided in cohort_incidence argument with ";")
- age_bin : size of incidence age bins (typical: 5)
- min_samples_in_bin : too small bins will be unified with bins near them
- from_year : year to start collecting numbers from
- to_year : year to end collection
- start_date : date in year to test : mmyy without trailing 0 , for example 508 is may 8th , 1201 is December 1st
- gender_mask : as usual 2 bits
- train_mask : as usual 3 bits
- from_age : ages to start counting
- to_age : ages to end counting
- incidence_years_window : how many years a head to calculate incidence for
- incidence_days_win : if given trumps years : how many days ahead to calculate incidence for
 
**Incidence params example**
```bash
# calculate incidence on years 2007 to 2010 (averaged over years) , for 1 year ahead (annual) only on TRAIN=1, age bins of 5 and test date in each year : June 2nd
INC_PARAMS="train_mask=1;age_bin=5;start_date=602;incidence_years_window=1;from_year=2007;to_year=2010"
```
 
Control  Sampling Args directly by  providing "–sampler_params":

- start_year,end_year or start_time,end_time as full time/date
- prediction_month_day as prediction date
- time_jump/day_jump - jump between prediction dates
- time_jump_unit - the jump time unit. for example Day, Year
- time_range_unit - the time range unit - Date on Minutes
 
