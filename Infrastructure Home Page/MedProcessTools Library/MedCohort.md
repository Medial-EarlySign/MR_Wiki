# MedCohort
### [MedCohort ](https://Medial-EarlySign.github.io/MR_LIBS/classMedCohort)is a data structure with helpers to deal with a cohort, a list of individuals with (dated) outcomes and followup times.
MedCohort contatins a vector of basic records ([CohortRec](https://Medial-EarlySign.github.io/MR_LIBS/structCohortRec)), each representing a single period for a specific id (with a corresponding outcome) information.
A MedCohort can be sampled to generate MedSamples files according to [SamplingParams](https://Medial-EarlySign.github.io/MR_LIBS/structSamplingParams) using one of two fuctions:
- *int create_sampling_file(SamplingParams &s_params, string out_sample_file)* : Generate samples within cohort times that fit SampleingParams criteria and windows. **Sample dates are selected randomly for each window of s_params.jump_days in the legal period.** 
- *int create_sampling_file_sticked(SamplingParams &s_params, string out_sample_file)* : Generate samples within cohort times that fit SampleingParams criteria and windows. **Sample dates are those with the required signals for each window of s_params.jump_days in the legal period (if existing).**
A MedCohort can also be used to estimate the age and gender dependent incidence rate. Estimation is done using the following function which according to [IncidenceParams](https://Medial-EarlySign.github.io/MR_LIBS/structIncidenceParams):
- *int create_incidence_file(IncidenceParams &i_params, string out_file) : *Generate an incidence file from cohort + incidence-params. Check all patient-years within cohort that fit IncidenceParams and count positive outcomes within the incidence_years_window.
**IncidenceParams initialization:**
<table><tbody>
<tr>
<th>Parameter Name</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td><span>incidence_years_window</span></td>
<td>how many years ahead do we consider an outcome?</td>
<td>1</td>
</tr>
<tr>
<td>rep</td>
<td>Repository configration file</td>
<td>None</td>
</tr>
<tr>
<td>from_year</td>
<td>first year to consider in calculating incidence</td>
<td>2007</td>
</tr>
<tr>
<td>to_year</td>
<td>last year to consider in calculating incidence</td>
<td>2013</td>
</tr>
<tr>
<td>gender_mask</td>
<td>mask for gender specification (rightmost bit on for male, second for female)</td>
<td>0x3</td>
</tr>
<tr>
<td>train_mask</td>
<td>mask for TRAIN-value specification (three rightmost bits for TRAIN = 1,2,3)</td>
<td>0x7</td>
</tr>
<tr>
<td>from_age</td>
<td>minimal age to consider</td>
<td>30</td>
</tr>
<tr>
<td>to_age</td>
<td>maximal age to consider</td>
<td>90</td>
</tr>
<tr>
<td><span>age_bin</span></td>
<td>binning of ages</td>
<td>5</td>
</tr>
<tr>
<td><span>min_samples_in_bin</span></td>
<td>minimal required samples to estimate incidence per bin</td>
<td>20</td>
</tr>
</tbody></table>
****
**SamplingParams initialization:**
<table><tbody>
<tr>
<th><span>Parameter Name</span></th>
<th><span>Description</span></th>
<th>Default Value</th>
</tr>
<tr>
<td>is_continous</td>
<td>continous mode of sampling vs. stick to signal (0 = stick)</td>
<td>1</td>
</tr>
<tr>
<td><span>stick_to, stick_to_sigs </span></td>
<td>comma separated list of signals required at sampling times</td>
<td>None</td>
</tr>
<tr>
<td>take_all</td>
<td><span>in 'stick' mode - </span>take all samples with requrired-signal within each sampling period is selected</td>
<td>0</td>
</tr>
<tr>
<td>take_closest</td>
<td><p>in 'stick' mode - take the sample with requrired-signals that is closest to each target sampling-date</p><p>if none of take_all and take_closest is given, a random sample with requrired-signal within each sampling period is selected</p></td>
<td>0</td>
</tr>
<tr>
<td><span>rep</span></td>
<td>Repository configration file</td>
<td>None</td>
</tr>
<tr>
<td>min_age</td>
<td>minimum age for sampling</td>
<td>0</td>
</tr>
<tr>
<td>max_age</td>
<td>maximum age for sampling</td>
<td>200</td>
</tr>
<tr>
<td>gender_mask</td>
<td>mask for gender specification (rightmost bit on for male, second for female)</td>
<td>0x3</td>
</tr>
<tr>
<td>train_mask</td>
<td>mask for TRAIN-value specification (three rightmost bits for TRAIN = 1,2,3)</td>
<td>0x7</td>
</tr>
<tr>
<td>min_year</td>
<td>first year for sampling</td>
<td>1900</td>
</tr>
<tr>
<td>max_year</td>
<td>last year for sampling</td>
<td>2100</td>
</tr>
<tr>
<td>jump_days</td>
<td>days to jump between sampling periods</td>
<td>180</td>
</tr>
<tr>
<td>min_days, min_days_from_outcome</td>
<td>minimal number of days before outcome for sampling</td>
<td>30</td>
</tr>
<tr>
<td>min_case, min_case_years</td>
<td>minimal number of years before outcome for cases</td>
<td>0</td>
</tr>
<tr>
<td>max_case, max_case_years</td>
<td>maximal number of years before outcome for cases</td>
<td>1</td>
</tr>
<tr>
<td>min_control, min_control_years</td>
<td>minimal number of years before outcome for controls</td>
<td>0</td>
</tr>
<tr>
<td>max_control, max_control_years</td>
<td>maximal number of years before outcome for controls</td>
<td>10</td>
</tr>
</tbody></table>
****
### Include file is - *H:/MR/Libs/Internal/MedUtils/MedUtils/MedCohort.h*
 
 
