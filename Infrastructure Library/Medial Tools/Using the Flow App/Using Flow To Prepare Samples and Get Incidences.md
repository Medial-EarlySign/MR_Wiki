
# Using Flow to Prepare Samples and Calculate Incidences

The Flow app provides powerful tools for selecting, filtering, and matching samples based on a cohort. These tools are essential for preparing sample files for training/validation or for matching populations on specific parameters. Flow also supports incidence estimation and generating incidence files for later analysis (e.g., bootstrap). The instructions below are primarily for date-based cases, but can be adapted for other variables.

## Cohort Files

A cohort file defines the patients to use for training/testing, including their entry/exit times and outcome information. Format:

- Tab-delimited
- Lines starting with `#` are comments
- Each line contains 5 fields:
    1. `pid`: Patient ID (one line per pid)
    2. Entry date to cohort
    3. End date in cohort
    4. Outcome date: For controls (outcome=0), same as end date; for cases (outcome=1), the event date (must be ≤ end date)
    5. Outcome: Typically 0/1 (control/case), but can be regression or multicategory (currently only a single value is supported)

**Example cohort file:**
```
# pid 5000009 entered on 20060505, left on 20091023, and had a case outcome at 20091023
5000009 20060505        20091023        20060605        1.000000
# pid 5000014 is a control (0.0 outcome), entered 20150107, left 20160929
5000014 20150107        20160929        20160929        0.000000
5000017 20110826        20160819        20160819        0.000000
```

## Creating a Sample File from a Cohort File

Use Flow to generate a sample file:

```bash
Flow --rep <repository> --seed <random seed> --cohort_fname <cohort file> --cohort_sampling <sampling parameters> --out_samples <output samples file>
```

All parameters are self-explanatory except `cohort_sampling`, which controls how samples are created (for both controls and cases). Key options (with defaults):

- `min_control_years` (0): Minimum years before outcome for controls
- `max_control_years` (10): Maximum years before outcome for controls
- `min_case_years` (0): Minimum years before outcome for cases
- `max_case_years` (1): Maximum years before outcome for cases
- `is_continous` (1): Continuous sampling (1) or on-test (0)
- `min_days_from_outcome` (30): Minimum days before outcome to sample
- `jump_days` (180): Days between sampling periods
- `min_year` (1900), `max_year` (2100): Year range for sampling
- `gender_mask` (3): 1=male, 2=female, 3=both
- `train_mask` (7): Mask for TRAIN value (bits for TRAIN=1,2,3)
- `min_age` (0), `max_age` (200): Age range for sampling
- `stick_to_sigs`: Comma-separated list of signals; only use time points with at least one of these signals
- `take_closest` (0): Take sample with stick signal closest to each target date
- `take_all` (0): Take all samples with stick signal in each period
- `max_samples_per_id` (2^31-1): Max samples per ID
- `max_samples_per_id_method` ('last'): 'last' or 'rand' (choose last or random samples)

**Sample usage:**

```bash
# Continuous sampling, random sample every 180 days
# Controls: 1–10 years before end; Cases: up to 2 years before outcome
# Only TRAIN=1, ages 35–90
SAMPLING_PARAMS1="min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=1;min_age=35;max_age=90"

# As above, but on-test and only at Glucose or HbA1C test dates
SAMPLING_PARAMS1="min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=1;min_age=35;max_age=90;is_continous=0;stick_to_sigs=Glucose,HbA1C"

# Run Flow (replace SAMPLING_PARAMS as needed)
Flow --rep /home/Repositories/THIN/thin_mar2017/thin.repository --seed 123 --cohort_fname ./pre2d.cohort --cohort_sampling ${SAMPLING_PARAMS} --out_samples ./temp.samples
```

## Filtering and Matching Samples

You can filter and/or match samples from an existing samples file (typically created as above):

```bash
Flow --rep <rep> --seed <random_seed> --filter_and_match --in_samples <input samples file> --out_samples <output samples file> --filter_params <filter params> --match_params <match params>
```
Filtering is applied first (if specified), then matching (if specified).

### Filter Parameters

Filtering allows you to select samples within a date range or based on signal values in a window before the sample time (e.g., only samples with Creatinine < 1.1 in the last 2 years).

- `min_sample_time` (0): Minimum allowed time (in sample's time unit, usually date)
- `max_sample_time` ((1<<30)): Maximum allowed time
- `win_time_unit` ("Days"): Time unit for bfilter windows
- `bfilter`: Filter on a signal; multiple filters allowed. Parameters (comma-separated):
    - `sig_name`: Signal name
    - `win_from` (0): Window start (relative to sample time, backwards)
    - `win_to` ((1<<30)): Window end
    - `min_val` (-1e10): Minimum allowed value
    - `max_val` (1e10): Maximum allowed value
    - `min_Nvals` (1): Minimum number of signal instances in window
    - `time_channel` (0), `val_channel` (0): Channels to consider
- `min_bfilter`: How many bfilters must pass (default: all)

**Examples:**

```bash
# Only samples between 20070101 and 20150101
FILTER1="min_sample_time=20070101;max_sample_time=20150101"

# At least 1 Creatinine test in last 2 years
FILTER2="bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1"

# As above, but all Creatinine < 0.9
FILTER3="bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1,min_val=0,max_val=0.9"

# Combined: date range, at least one Glucose in last 2Y, all Glucose < 100 in last 5Y, all HbA1C < 5.7 in last 5Y
FILTER4="min_sample_time=20070101;max_sample_time=20101201;bfilter=sig,Creatinine,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,Creatinine,win_from,0,win_to,1825,min_val,0,max_val,100;bfilter=sig,HbA1C,win_from,0,win_to,1825,min_val,0,max_val,5.7"
```

### Matching Parameters

Matching ensures the ratio of cases to controls is balanced within defined strata (e.g., by year, gender, age, or signal value). The algorithm tries to maximize the number of samples kept, with a weight parameter to prioritize keeping cases when they are rare.
The goal is to control and remove information related directly to those variables. A common case is to match by years to remove temporal information the model might gian from difference in cases, controls ratio in certain years.

- `priceRatio` (100.0): How many controls to lose per case (suggested: n_controls/n_cases)
- `maxRatio` (10.0): If optimal ratio > maxRatio, sample less (enrich cases)
- `verbose` (0): More output
- `match_to_prior`: Specify target prior directly
- `strata`: Define stratification (':'-delimited for multiple strata, ','-delimited for parameters):
    - `type`: time, age, gender, or signal
    - `signalName`: For time: year/month/days; for signal: name; for age/gender: none
    - `resolution`: Bin size

**Examples:**

```bash
# Match and stratify by year
MATCH1="priceRatio=10;maxRatio=4.5;verbose=1;strata=time,year,1"
# Match by year to a prior of 0.1 (10%)
MATCH1="match_to_prior=0.1;maxRatio=4.5;verbose=1;strata=time,year,1"
# Match by gender
MATCH2="priceRatio=10;maxRatio=4.5;verbose=1;strata=gender"
# Match by age (5-year bins)
MATCH3="priceRatio=10;maxRatio=4.5;verbose=1;strata=age,5"
# Match by age, year, and gender together
MATCH4="priceRatio=10;maxRatio=4.5;verbose=1;strata=age,5:time,year,1:gender"
# Match by Glucose (bin=10) and HbA1C (bin=1.0)
MATCH5="priceRatio=10;maxRatio=4.5;verbose=1;strata=signal,Glucose,10:signal,HbA1C,1.0"
```
For more details, see: [MatchingSampleFilter](../../../Infrastructure%20Library/MedProcessTools%20Library/SampleFilter/MatchingSampleFilter.md)

## Calculating Incidence for a Cohort

To generate an incidence file for a cohort, use:

```bash
Flow --rep <repository> --cohort_incidence "from_year=2007;to_year=2014;from_age=40;to_age=80;age_bin=40;incidence_days_win=1825" --cohort_fname <cohort file> --cohort_incidence <incidence parameters> --out_incidence <incidence file> --censor_reg <censor registry> --use_kaplan_meir 1
```
`cohort_fname` and `censor_reg` are MedRegistry objects. You can convert a MedCohort to MedRegistry using:

```bash
# Create MedRegistry from MedCohort
cat <cohort file> | awk '{ if ($NF > 0) { print $1 "\t" $2 "\t" $4 "\t" "0";  print $1 "\t" $4 "\t" $3 "\t" "1" } else { print $1 "\t" $2 "\t" $3  "\t" "0" } }'
# Create Censor registry from MedCohort
cat <cohort file> | awk '{ if ($NF > 0) { print $1 "\t" $2 "\t" $4 "\t" "1" } else { print $1 "\t" $2 "\t" $3  "\t" "1" } }'
```

### Incidence Parameters (in `cohort_incidence` argument, separated by `;`)

- `age_bin`: Size of age bins (e.g., 5)
- `min_samples_in_bin`: Small bins are merged with neighbors
- `from_year`, `to_year`: Year range
- `start_date`: Date in year to test (mmyy, e.g., 508=May 8, 1201=Dec 1)
- `gender_mask`, `train_mask`: As above
- `from_age`, `to_age`: Age range
- `incidence_years_window`: Years ahead to calculate incidence
- `incidence_days_win`: Days ahead to calculate incidence (overrides years if set)

**Example:**

```bash
# Incidence for 2007–2010 (annual), TRAIN=1, age bins of 5, test date June 2nd
INC_PARAMS="train_mask=1;age_bin=5;start_date=602;incidence_years_window=1;from_year=2007;to_year=2010"
```

You can also control sampling directly with `--sampler_params`:

- `start_year`, `end_year` or `start_time`, `end_time`: Full time/date
- `prediction_month_day`: Prediction date
- `time_jump`/`day_jump`: Interval between prediction dates
- `time_jump_unit`: Jump unit (e.g., Day, Year)
- `time_range_unit`: Time range unit (e.g., Date, Minutes)
 
