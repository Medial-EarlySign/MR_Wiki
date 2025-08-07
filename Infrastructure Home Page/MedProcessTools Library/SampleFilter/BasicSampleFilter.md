# BasicSampleFilter
### BasicSampleFilter applies one (or more) basic filters to the set
[BasicSampleFilter ](https://Medial-EarlySign.github.io/MR_LIBS/classBasicSampleFilter)filtering options include:
- Allowed time (date) range
- A list of filters per signal, each specified using [BasicFilteringParams](https://Medial-EarlySign.github.io/MR_LIBS/structBasicFilteringParams)
  - Allowed value-range of specific signals within a time-window
  - Requirement on availability of specific signals - number of values within a time-window
### Include file is - *H:/MR/Libs/Internal/MedUtils/MedProcessTools/SampleFliter.h*
### BasicFilteringParams initializing:
<table><tbody>
<tr>
<th>Parameter Name</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>sig</td>
<td>name of signal used for filtering</td>
<td>None</td>
</tr>
<tr>
<td>min_val</td>
<td>minimal allowed value</td>
<td>-1e10</td>
</tr>
<tr>
<td>max_val</td>
<td>maximal allowed value</td>
<td>1e10</td>
</tr>
<tr>
<td>min_Nvals</td>
<td>minimal required number of values</td>
<td>1</td>
</tr>
<tr>
<td>win_from</td>
<td>start of time window to check requirements</td>
<td>0</td>
</tr>
<tr>
<td>win_to</td>
<td><p>end of time window to check requirements</p><p>e.g. (win_from=30,win_to=60) means that we check the signal one to two months before sample date</p></td>
<td>2^30</td>
</tr>
<tr>
<td>time_ch</td>
<td>time-channel to consider</td>
<td>0</td>
</tr>
<tr>
<td>val_ch</td>
<td>value-channer to consider</td>
<td>0</td>
</tr>
</tbody></table>
### BasicSampleFilter initializing:
<table><tbody>
<tr>
<th>Parameter Name</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>min_sample_time</td>
<td>minimal allowed time (date)</td>
<td>0</td>
</tr>
<tr>
<td>max_sample_time</td>
<td>maximal allowed time (date)</td>
<td>2^30</td>
</tr>
<tr>
<td>win_time_unit</td>
<td>time-unit name (e.g. "date")</td>
<td>Days</td>
</tr>
<tr>
<td>bfilter</td>
<td><p>BasicFilterParams: list of plus-separated filters.</p><p>Each filter is defined by a ":="-separated initializer of BaiscFilteringParams</p></td>
<td>None</td>
</tr>
</tbody></table>
 
**
