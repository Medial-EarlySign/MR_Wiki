# SampleFilter
### [SampleFilter ](http://node-04/Libs/html/classSampleFilter)filters a set of samples
SampleFIlter takes a MedSamples object and generates a new one (optionally in-place) which contains a subset of the original samples. SampleFilters may (optinally) require a MedRepository to apply the filtering
SampleFilter is a virtual class. See below for the list of implemeted children classes
### Include file is - *H:/MR/Libs/Internal/MedUtils/MedProcessTools/SampleFliter.h*
****
<table style="line-height: 1.4285715;"><tbody>
<tr>
<th><strong>Name</strong></th>
<th>Value</th>
<th>Class</th>
<th>Note</th>
</tr>
<tr>
<td>train</td>
<td>SMPL_FILTER_TRN</td>
<td><a href="BasicTrainFilter_8781943.html">BasicTrainFilter</a></td>
<td>Generate a training set</td>
</tr>
<tr>
<td>test</td>
<td>SMPL_FILTER_TST</td>
<td><a href="BasicTestFilter_8781945.html">BasicTestFilter</a></td>
<td>Generate a test set</td>
</tr>
<tr>
<td>outliers</td>
<td>SMPL_FILTER_OUTLIERS</td>
<td><a href="OutlierSampleFilter_8781947.html">OutlierSampleFilter</a></td>
<td>Remove outlying outcomes</td>
</tr>
<tr>
<td>match</td>
<td>SMPL_FILTER_MATCH</td>
<td><a href="MatchingSampleFilter_8781949.html">MatchingSampleFilter</a></td>
<td>Perform matching</td>
</tr>
<tr>
<td>required</td>
<td>SMPL_FILTER_REQ_SIGNAL</td>
<td>RequiredSignalFilter</td>
<td>OBSOLETE, replaced by 'basic'</td>
</tr>
<tr>
<td>basic</td>
<td><span>SMPL_FILTER_BASIC</span></td>
<td><a href="BasicSampleFilter_8781951.html">BasicSampleFilter</a></td>
<td>A range of filtering options</td>
</tr>
</tbody></table>
