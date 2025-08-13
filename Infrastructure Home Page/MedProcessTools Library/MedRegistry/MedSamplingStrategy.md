# MedSamplingStrategy
A Class that controls how to create [MedSamples ](../MedSamples.md)from [MedRegistry ](/Infrastructure%20Home%20Page/MedProcessTools%20Library/MedRegistry)by sampling methods.
it has several subclasses, each has it's own parameters and logic to sample the samples form registry:
<img src="/attachments/9765342/10911920.png"/>
Code is documented [here](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamplingStrategy).
do_sample aruments in MedSamplingRegistry:

- const vector<[MedRegistryRecord](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistryRecord)> &registry - the registry for the labeling the samples by the sampler (already initialized with sampling params)
- [MedSamples](/Infrastructure%20Home%20Page/MedProcessTools%20Library/MedRegistry) &samples - the samples result
- const vector< [MedRegistryRecord](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistryRecord) > *censor_registry - optional arg for specifying censoring times for the sampling
### Important Samplers:
**** - can be used by specifying MedSamplingRegistry::make_sampler("time_window"). from the updated documentition reffer to [doxygen](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamplingTimeWindow)
Used to sample for each registry record randomly withing a specific time window.
It can define diffrent time windows for cases/controls.
Parameters:
<table><tbody>
<tr>
<th>Parmeter Name</th>
<th>Type</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>sample_count</td>
<td>int</td>
<td>how many samples to sample from each registry record.</td>
<td>1</td>
</tr>
<tr>
<td><span style="color: rgb(85,85,85);">minimal_time_case</span></td>
<td>int</td>
<td><span style="color: rgb(85,85,85);">the minimal time to give prediciton before the case outcomeTime</span></td>
<td>0</td>
</tr>
<tr>
<td><span style="color: rgb(85,85,85);">maximal_time_case</span></td>
<td>int</td>
<td>the maximal time to give predicition before the case outcomeTime</td>
<td>0</td>
</tr>
<tr>
<td><span style="color: rgb(85,85,85);">minimal_time_control</span></td>
<td>int</td>
<td><span style="color: rgb(85,85,85);">the minimal time to give prediciton before the control outcomeTime (which marks the last time we know the patient is control)</span></td>
<td>0</td>
</tr>
<tr>
<td>maximal_time_control</td>
<td>int</td>
<td><span style="color: rgb(85,85,85);">the maximal time to give prediciton before the control outcomeTime (which marks the last time we know the patient is control)</span></td>
<td>0</td>
</tr>
<tr>
<td>take_max</td>
<td>bool</td>
<td>If True will take maximal time window for case/control</td>
<td>0</td>
</tr>
</tbody></table>
**MedSamplingYearly** - can be used by specifying MedSamplingRegistry::make_sampler("yearly"). from the updated documentition reffer to [doxygen](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamplingYearly) 
Used to sample from year to year by jumping periodically between sample times for each patient. for sampling in ICU (more generic sampler for sampling in Fixed time, please reffer to [MedSamplingFixedTime](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamplingFixedTime))
The arguments: time_from, time_to, conflict_method, outcome_interaction_mode, censor_interaction_mode - are common in almost all samplers.
<table><tbody>
<tr>
<th>Parmeter Name</th>
<th>Type</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>start_year</td>
<td>int</td>
<td>the start year to sample from</td>
<td>0 - Must be provided</td>
</tr>
<tr>
<td>end_year</td>
<td>int</td>
<td><span style="color: rgb(85,85,85);">The end year to sample from</span></td>
<td>0 <span>- Must be provided</span></td>
</tr>
<tr>
<td>prediction_month_day</td>
<td>int</td>
<td>the prediction date for the first year to start sampling</td>
<td>101 - mean 01/01</td>
</tr>
<tr>
<td>day_jump</td>
<td>int</td>
<td>the period of days to jump between each sampling date</td>
<td>0 <span>- Must be provided, the common value should be 365 to jump yearly between sample times</span></td>
</tr>
<tr>
<td>back_random_duration</td>
<td>int</td>
<td>random time to sample backward from the prediction date - adds ability to sample in random times in the year</td>
<td>0</td>
</tr>
</tbody></table>
**MedSamplingDates** - Provides way to list all sampling options for each patient (or general options list) in a text file and sample randomly from those options
**MedSamplingStick** - can sample on sticked signal times (fetches the signal times and uses MedSamplingDates to do the sampling)
<table><tbody>
<tr>
<th>Parmeter Name</th>
<th>Type</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>signal_list</td>
<td>string</td>
<td>a comma <span>","</span> delimeted list with signals to list all possible sampling times for patient to stick to</td>
<td><span>"" Must be provided</span></td>
</tr>
<tr>
<td>take_count</td>
<td>int</td>
<td>how many samples to sample for each patient (inherited from MedSamplingDates). 0 - means take all samples</td>
<td>1</td>
</tr>
<tr>
<td>sample_with_filters</td>
<td>bool</td>
<td>Whether to use the filters as constraints and sample only when valid (may cause bais) or sample totally random and filter later</td>
<td>True</td>
</tr>
</tbody></table>
