# create_registry
A tool to create MedRegistry and if provided sampling startegy parameters to create MedSamples.
The program steps:

- Creates or load from text file [MedRegistry](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry). Can provide file path or config file to generate MedRegistry
- Creates or load from text file [MedRegistry](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry) for censoring (a time periods where that marks the patients "Membership" period, it's also in format of MedRegistry) - OPTIONAL, if not given, assume the patient has full membership
- Creates [MedLabel](https://Medial-EarlySign.github.io/MR_LIBS/classMedLabels) from registry and censor_registry with problem definition arguments - time window argument + labeling policy arguments. This object knows how to "label" the outcome for a sample in a given time or decide to exclude it based on MedRegistry and the LabelParams.
- Creates [MedSamples ](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedSamples.md)from [MedSamplingStrategy ](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry/MedSamplingStrategy.md)arguments of how to sample + additional filtering arguments you may provide to restrict sampling (Age, Years...)
## Create samples from MedRegistry
```bash
create_registry --rep $REP_PATH --registry_load $PATH_TO_MED_REGISTRY_FILE --registry_active_periods_complete_controls_sig MEMBERSHIP \
 --labeling_params $LABELING_PARAMS --sampler_type $SAMPER_TYPE --sampler_args $SAMPLER_ARGS --samples_save $OUTPUT_PATH_FOR_MEDSAMPLES \
--filtering_params $OPTIONAL_FILTERING_PARAMS_LIKE_AGE
#Can also provide additional MedRegistry for Membership if it is not a signal, by passing "--censor_load".
```

- LABELING_PARAMS - defines how to label the sample - is it case/control or other outcome value?- The initialization text for [MedLabels](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedLabels.md)
- SAMPER_TYPE - type of sampler. The options are in [here](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamplingStrategy.html#a161f9af97fe2dd90bff67a5ac58679ff) (code documentation make_sampler) or can look for informaiton here: [MedSamplingStrategy](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry/MedSamplingStrategy.md)
- SAMPLER_ARGS - for the specific Sampler, the arguments for it. [MedSamplingStrategy](../../Infrastructure%20C%20Library/MedProcessTools%20Library/MedRegistry/MedSamplingStrategy.md) or browse the arguments of the specifc sampler
- OPTIONAL_FILTERING_PARAMS_LIKE_AGE - parameters to filter the samples like age. [FilterParams](https://Medial-EarlySign.github.io/MR_LIBS/classFilterParams). For example "min_age=0;max_age=90;min_time=20120101;max_time=20180101"
The SAMPLER_TYPE, SAMPLER_ARGS are independent of the labeing - they define just when to give score or try to give score.
 
Example:
We have Influenza MedRegistry where the patient is marked and control when he has Membership and not influenza. In influenza events we have a 1 day time window of influenza.
We want to see which patient will have flu within 1 year. The censor registry is the membership signal - we require no gaps in the whole year.
The labeling params:
"time_from=0;time_to=365;censor_time_from=0;censor_time_to=365;conflict_method=max;censor_interaction_mode=all:within:within;label_interaction_mode=0:within,within|1:before_start,after_start" 
The sampling:
`--sampler_type yearly --sampler_args "start_year=2016;end_year=2018;prediction_month_day=901;day_jump=365"`
Which predicts in 1st of September in each year from 2016 to 2017, is can give score within the specific time for the patient (has a match for a certain registry record)
## Create MedRegistry from command
```bash
create_registry --rep $REP_PATH --registry_type $REGISTRY_TYPE --registry_init  $REGISTRY_ARGS --registry_save $OUTPUT_PATH_FOR_MEDREGISTRY 
# --use_active_for_reg_outcome can pass this argument with censor registry, whether with "--registry_active_periods_complete_controls_sig" or "--registry_active_periods_complete_controls"
```
Needs to explain and give some examples on how to create MedRegistry

- REGISTRY_TYPE : either "binary" for binary problems , "categories" (for outcome with more than case/controls states). and "keep_alive" that is mostly used to generate membership period based on patients activity
- REGISTRY_ARGS : the arguments for the registry type. For example "binary" has those options:
    -  max_repo_date - the maximal repoistory date to cut registry date. in format YYYYMMDD
    - start_buffer_duration - buffer duration from first "rule" start. Mostly, set to 0
    - end_buffer_duration - buffer duration from last "rule" end duration. In case we want to "trim" the last period. Mostly, set to 0
    - allow_prediciton_in_case - if true will continue to process rules even if in "case" time period
    - seperate_cases - will allow more than one time period of case. Might be useful fot influenza events that may occur several times.
    - config_signals_rules - file path to registry rules to define the MedRegistry records
        - Tab delimted file with 2 columns: [RegistrySignalType](https://Medial-EarlySign.github.io/MR_LIBS/classRegistrySignal.html)and it's arguments
Example config_signals_rules  file for CKD from 2 to 3 and up:
```
#Definition of controls- if CKD_State is less than 2, mark it as 0 for at least 1 year if not contradicted or contiuned:
range	signalName=CKD_State;duration_flag=365;take_only_first=0;outcome_value=0;min_value=0;max_value=2
#Definition of cases - if CKD_State is 3 and more, mark it as 1 for at least 1 year if not contradicted or contiuned:
range	signalName=CKD_State;duration_flag=365;take_only_first=0;outcome_value=1;min_value=3;max_value=9
```
