# AlgoMarker Configuration & Eligibility

The MedialInfra AlgoMarker allows you to use any model that was trained using the MedProcessTools infrastructure. It provides robust configuration options for testing the eligibility of input data before generating a prediction.

## Configuration File

When loading a new MedialInfra AlgoMarker, a configuration file (`.amconfig`) is required. This file defines the model, repository, and any eligibility filters.

```txt title="Configuration File Example"
#################################################################################
# MedialInfra AlgoMarker config example file
#################################################################################
# comment lines start with #
# all (non comments) separators are tab
# type of AlgoMarker
# should be MEDIAL_INFRA for a MedialInfra AlgoMarker, otherwise will fail loading
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
# if the model has Glucose_nRem attributes we can create the following rule by testing it directly.
FILTER	attr|attr_name=Glucose_nRem;max=0|ERROR|ACC=0|321|321|Too many glucose outliers

# max outliers allowed when summing over all the ACC=1 filters
MAX_OVERLALL_OUTLIERS	1
```

## Eligibility Rules Configuration

Each filter enforces a rule on the data. The format for a filter is: 
`FILTER <filter type>|<filter params>|<warning_or_error>|<use_for_max_outliers_flag>|<external_rc>|<internal_rc>|<err_msg>`

* **`<filter type>`**: `simple` or `attr`
* **`<filter params>`**: see examples above and definitions below
* **`<warning_or_error>`**: `WARNING` or `ERROR`. A warning will run the test and report the problem if found, but will not fail the prediction entirely.
* **`<use_for_max_outliers_flag>`**: `ACC=1` or `ACC=0`. Dictates whether to accumulate the overall number of outliers (`MAX_OVERLALL_OUTLIERS`).
* **`<external_rc>`** & **`<internal_rc>`**: Error return codes to provide in the API response message.
* **`<err_msg>`**: A free-text string returned as the error message if the test does not pass.

### Parameters for `simple` filter type

Parameters are separated by `;` without any spaces/tabs.
* `sig`: Name of the signal to test.
* `time_ch`, `val_ch`: Time and value channels (default is 0 and 0).
* `win_from`, `win_to`: A time window before and relative to the sample. (Default is infinite).
* `min_val`, `max_val`: Min and max allowed values (`>= min`, `<= max`).
* `min_Nvals`, `max_Nvals`: Test minimum or maximum total number of values inside the given window.
* `max_outliers`: Maximal allowed number of outliers for the signal in the given time window.
* `allowed_values`: Comma-separated list (e.g. `allowed_values=1,3`). Test verifies that all values match these.
* `values_in_dictionary`: Set to `1` to test that all values of the signal exist in the repository dictionary (useful for categorical data like Drugs).

### Parameters for `attr` filter type

`attr` filters rely on attributes created by the model and injected into the predictions. You must configure the model's JSON definition to create these attributes.
* `name`: The name of the attribute to test (e.g., `nrem_attr: "nRem"` from `basic_cln` in the model json).
* `max`: The maximal value allowed. An error or warning will be thrown for any value strictly larger than this.
