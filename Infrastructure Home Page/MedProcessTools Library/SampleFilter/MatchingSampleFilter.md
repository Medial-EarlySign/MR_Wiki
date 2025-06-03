# MatchingSampleFilter
### MatchingSampleFilter matches cases a control according to a combination of matching criteria.
MatchingSampleFilter can use the following matching criteria:
- Age
- Time (e.g. calendar year)
- Values of signals
- Gender
The optimal matching ratio is determined given a relative cost of losing a single cases versus losing a single controls sample.
### MatchingSampleFilter initialization:
<table><tbody>
<tr>
<th>Parameter Name</th>
<th>Description</th>
<th>Default Value</th>
</tr>
<tr>
<td>priceRatio</td>
<td>the relative cost of losing a single controls sample</td>
<td>100.0</td>
</tr>
<tr>
<td>match_to_prior</td>
<td>Given directly the prior to match to in each bin. If &lt; 0 won't be used</td>
<td>-1</td>
</tr>
<tr>
<td>maxRatio</td>
<td>the maximal allowed control/case matching ratio</td>
<td>10.0</td>
</tr>
<tr>
<td>verbose</td>
<td>a verbositry flag (set to &gt;0 to allow logging)</td>
<td>0</td>
</tr>
<tr>
<td>strata</td>
<td><p>Definition of a matching strata, possibly more than one, separated by a colon</p><p>Each stratum is comma-separated and can be one of:</p><ul><li>"age" or "age,1" which 1 stands for bin_size in age</li><li>"time,time-unit-name,time-resolution" (e.g. "time:year,1")</li><li>"signal,signal-name,resolution,TimeWindow (in days , takes the last)" (e.g. "signal,WBC,0.5,365")</li><li>"gender"</li></ul><p> </p></td>
<td>None</td>
</tr>
</tbody></table>
 
