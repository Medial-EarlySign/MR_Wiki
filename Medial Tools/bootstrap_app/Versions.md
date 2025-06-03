# Versions
## Frozen Versions
### Frozen versions of the bootstrap app can be found here: **/server/Work/FrozenTools**
<table><tbody>
<tr>
<th>Version</th>
<th>Date</th>
<th>Windows/Linux</th>
<th>Git Branch Name</th>
<th>Git Tag Name</th>
<th>Changes</th>
</tr>
<tr>
<td><span>bootstrap_app_1.0.2</span></td>
<td><time class="date-past" datetime="2019-01-21">21 Jan 2019</time> </td>
<td>Linux</td>
<td>bootstrap_app_1.0</td>
<td><span>bootstrap_app_1.0.2</span></td>
<td><ul><li>bugfix in incidence calculation with kaplan-meier</li></ul></td>
</tr>
<tr>
<td>bootstrap_app_1.0</td>
<td><time class="date-past" datetime="2018-12-19">19 Dec 2018</time> </td>
<td>Linux</td>
<td><span>bootstrap_app_1.0</span></td>
<td><p>191218_01</p></td>
<td><ul><li>The MedRegistry format has changed, and the info is now passed by two inputs: registry and censor. See <a href="MedRegistry_9207878.html">MedRegistry</a> and <a href="MedSamplingStrategy_9765342.html">MedSamplingStrategy</a> for more info.</li></ul></td>
</tr>
</tbody></table>
 
## Releasing a new version
Before releasing a new version, the output of the new version should be compared to the outputs of the old one. Below is a benchmark test to compare to. If the outputs have changed, explain why.
**Test:**
1. Open a folder for the outputs of the tested version. E.g: /server/Work/FrozenVersions/test_benchmark/bootstrap_app_1.1
2. Run the following command (change the output to the folder you created in step 1)
tal@[node-01:/server/Work/FrozenTools/test_benchmark$](http://node-01/server/Work/FrozenTools/test_benchmark$) ../bootstrap_app_1.0 --input pre2d_continuous.preds --output *new_version_name*/Bootstrap.pre2d_continuous --rep /home/Repositories/THIN/thin_jun2017/thin.repository --registry_path pre2d.MedRegistry --censoring_registry_path pre2d.MedRegistry.censor --cohorts_file pre2d_main_cohorts.params --incidence_sampling_args "start_year=2007;end_year=2014;conflict_method=all;outcome_interaction_mode=0:after_start,before_end|1:before_start,after_start;censor_interaction_mode=all:within,all" --sample_min_year 2007 --sample_max_year 2015 --sim_time_window --do_kaplan_meir 1 --output_raw TRUE --debug | tee bootstrap_app_1.0/Bootstrap.pre2d_continuous.log
**Compare Results**:
<table><tbody>
<tr>
<th>Version</th>
<th>Cohort</th>
<th>NPOS_Obs</th>
<th>NNEG_Obs</th>
<th>AUC_Mean</th>
<th>AUC_CI.Lower.95</th>
<th> AUC_CI.Upper.95</th>
<th>Incidence (when supplying --registry_path)</th>
<th>sim_time_window</th>
<th>kaplan meier</th>
</tr>
<tr>
<td><span>bootstrap_app_1.0</span></td>
<td>TimeWindow_0_365_Age_40_80</td>
<td>9954</td>
<td>127834</td>
<td>0.850361</td>
<td><span>0.846586</span></td>
<td><span> 0.854049</span></td>
<td>3.2927%</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td><span>bootstrap_app_1.0</span></td>
<td>TimeWindow_0_365_Age_40_80</td>
<td>18406</td>
<td>118188</td>
<td>0.868676</td>
<td>0.866065</td>
<td>0.871808</td>
<td>3.2927%</td>
<td>0</td>
<td>1</td>
</tr>
</tbody></table>
**It is also strongly recommend to: **
- Add subcohorts which use the json file and make sure everything works (to do this, uncomment the second line in pre2d_main_cohorts.params and run the command above)
- Repeat test on other problems which are based on registries of different character (cancer, flu...)
**Freeze:**
Exit to branch and/or add tag at the repositories: Libs, Tools and Scripts. Compile and add the executable file to /server/Work/FrozenTools, and update this page.
 
 
