# RepProcessor
### [RepProcessor ](https://Medial-EarlySign.github.io/MR_LIBS/classRepProcessor)applies in-place processing to the information held for a single patient-id (a DynamicPidRec)
The main functionalities of a RepProcessor include learning the processing parameters from (a subset of) a repository, and applying to a single patient Id (DynamicPidRec) at selected time-points. A processor may act differently at different time points (e.g. a predictor that looks at a range of times, must not consider points after the sample-time) - this is achieved by generating different versions of the affected signals in the DynamicPidRec (a version per time point). If the DynamicPidRec already has different versions in the required signals (i.e. it has been processed by other rep_processors), the correct version should be used when learning and applying the processor.
RepProcessor is a virtual class. See below for the list of implemeted children classes
### Include file is - *H:/MR/Libs/Internal/MedUtils/MedProcessTools/RepProcess.h*
 
****RepProcessorTypes****
[RepBasicRangeCleaner](RepBasicRangeCleaner.md)
<table><tbody>
<tr>
<th><strong>Name</strong></th>
<th>Value</th>
<th>Class</th>
<th>Note</th>
</tr>
<tr>
<td>multi, multi_processor</td>
<td>REP_PROCESS_MULTI</td>
<td>RepMultiProcessor</td>
<td>A container for a set of processors that can be learned simultanously (e.g. cleaneds of different signals)</td>
</tr>
<tr>
<td>basic_cln, basic_outlier_cleaner</td>
<td>REP_PROCESS_BASIC_OUTLIER_CLEANER</td>
<td><a href="RepBasicOutlierCleaner.html">RepBasicOutlierCleaner</a></td>
<td>Outliers cleaning (removing and trimming) working on single-values</td>
</tr>
<tr>
<td>nbrs_cln, nbrs_outlier_cleaner</td>
<td>REP_PROCESS_NBRS_OUTLIER_CLEANER</td>
<td>RepNbrsOutlierCleaner</td>
<td>Outliers cleaning (removing and trimming) working on values and their neighborhoods</td>
</tr>
<tr>
<td>configured_outlier_cleaner, conf_cln</td>
<td>REP_PROCESS_CONFIGURED_OUTLIER_CLEANER</td>
<td><a href="RepConfiguredOutlierCleaner.html">RepConfiguredOutlierCleaner</a></td>
<td>Uses configuration file for learning borders from statistics , or just set border according to hard coded values</td>
</tr>
<tr>
<td>rulebased_outlier_cleaner, rule_cln</td>
<td>REP_PROCESS_RULEBASED_OUTLIER_CLEANER</td>
<td><a href="RepRulebasedOutlierCleaner.html">RepRuleBasedOutlierCleaner</a></td>
<td>Uses set of coded rules about relation among signals taken simulatneously, and if rule is not met all measurements are removed.</td>
</tr>
<tr>
<td>aggregation_period</td>
<td>REP_PROCESS_AGGREGATION_PERIOD</td>
<td><a href="RepAggregationPeriod.html" rel="nofollow">RepAggregationPeriod</a></td>
<td>Creates a virtual signal containing the 'treatment period' for the input signal</td>
</tr>
<tr>
<td>basic_range_cleaner, range_cln</td>
<td>REP_PROCESS_BASIC_RANGE_CLEANER</td>
<td><a href="RepBasicRangeCleaner.html" rel="nofollow">RepBasicRangeCleaner</a></td>
<td>Creates a virtual signal containing only instances of the signal that fall within some instance of the range signal.</td>
</tr>
</tbody></table>
