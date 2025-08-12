# model_signals_importance
# Goal
Compare model performance with\without passing group os signals to input the model.

- --skip_list  comma deliimited list that contorls which signals to skip - mainly passed Age,Gender. We always have those values and don't/can't check those
- --no_filtering_of_existence - If passed, will not filter each cohort to a one that we have the signal exists in certain time window controlled by --time_windows
- --features_groups - 2 columns tab delimeted or ButWhy grouping format like "BY_SIGNAL". It mapps feature to a group name/signal
- --group2signal - can map the "groups" of features_groups into list of signals to exclude when handling this group. Tab delimeted, 2 columns: group name as in features_groups and list of signal, comma delimited

1. features_groups - Taking but why group names and maping feature to names, just to count how many features are effected, but we are going to use only the "group names" of this 
2. if name matches in group2signal => take the mapped value, list of signals to use, otherwise it assume the name of the group is already a valid signal name
So groups are determined by features_groups values.  group2signal, help to remap those groups to lists of signals.
