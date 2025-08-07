# MedLabels
A class the holds the information on how to label samples and outputs the outcome.
It uses the [MedRegistry](../MedRegistry)and internal parameters to define the "labeling" - for example the relevant time window for the outcome. So you can use the same MedRegistry and just change for example the time window for the outcome.
The parameters for the labeling are called [LabelParams](https://Medial-EarlySign.github.io/MR_LIBS/classLabelParams.html):
- time_from / time_to - the time window defintion for the outcome
- censor_time_from / censor_time_to - time window for the censor registry
- conflict_method - how to cop with conflicts. If the rules has more the one option:
  - drop - will drop sample. has conflict
  - all - will create a sample for each outcome. In binary usecase, the same sample will appear twice, once as a case and once as control
  - max - take maximal label. If both case/control rules are satisfied take max - which is case
  - last - takes the last matched record
- label_interaction_mode - please refer to [TimeWindowInteraction ](MedRegistry/TimeWindowInteraction)for more info. Defines the "rules" of matching between the patient registry records and the sample time window (defined by time_from, time_to on the MedSample time). If the rule is satsisfied, the registry outcome value is taken into account for labeling the sample. If there is only one matched record (of multiple but with the same vaalue), then this value is selected. Otherwise, uses "conflict_method" argument to resolve the conflict
- censor_interaction_mode - Same format as label_interaction_mode but just for censor registry
