# Experiments - Stage B
We will preform an additional experiment (not blinded) and more focused to achieve those goals:

- Understand/decide about rules to clean the output.
    - For example: weird results like giving high contribution to missing value(we already have a parameter to zero it)
    - Check score for threshold and validate we have enough positive contributions or negative, if the patient wasn't flagged?
    - Use threshold for absolute and relative contribution scores - for example: patient with low score maybe should not see normal lab results with small contribution
- Understand/decide about the outputs - currently we have groups of features and we reveal top contributing feature with it. Also presenting the feature value and percentage from all contribution. Do we need to change it?
    - Presents top 10 groups by absolute values- maybe we should sort otherwise, depend on the score?currently we have decided to do it that way
    - Groups: will split each lab signal into 2 groups of : values, trends. categorical values are aggregated by time windows
    - Preventative feature in each group - present the most contributing feature in the group. what to do if it has opposite contribution sign?
- Complete the documentation of how much time it takes for LIME, trees to run.
    - CRC - 23.5 seconds for 120 samples. means 3-4 s sample in second (using parallel)...   A  little slow
out of scope: - how to present it in gui, separate into reason we can affect and not...
 
Will be done on CRC, Flu and with trees_with_covarinace_fix, LIME_GAN
 
Update!!!
Added new method: tree_iterative.
## Pre2D results:
The results on pre2d were already pretty good (with maybe some improvement over tree explainer without covariance fix). Just wanted to make sure the tree_iterative doesn't make things worse.
tree_iterative is similar (with maybe slightly improvement comapre to with_cov)
<table><tbody>
<tr>
<th>Explainer_name</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>5</th>
<th>&lt;EMPTY&gt;</th>
<th>Total exp</th>
<th>Average score</th>
<th>Average L^0.5</th>
</tr>
<tr>
<td>tree_iterative</td>
<td>21</td>
<td>46</td>
<td>46</td>
<td>25</td>
<td>2</td>
<td>138</td>
<td>3.543478261</td>
<td>1.864308126</td>
</tr>
<tr>
<td>tree_with_cov</td>
<td>16</td>
<td>54</td>
<td>51</td>
<td>17</td>
<td>2</td>
<td>138</td>
<td>3.5</td>
<td>1.856313886</td>
</tr>
</tbody></table>
*in pre2d the covariance fix made the results of but why a little worse in the first stage of experiments. 
## CRC results:
<table><tbody>
<tr>
<th>run</th>
<th>Explainer_name</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>5</th>
<th>&lt;EMPTY&gt;</th>
<th>Mean_Score</th>
<th>Mean_Score_0.5</th>
</tr>
<tr>
<td>first run</td>
<td>tree_iterative_cov</td>
<td>1</td>
<td>4</td>
<td>15</td>
<td>7</td>
<td>94</td>
<td>4.037037037</td>
<td>1.999810838</td>
</tr>
<tr>
<td>first run</td>
<td>tree_iterative</td>
<td>1</td>
<td>6</td>
<td>16</td>
<td>5</td>
<td>93</td>
<td>3.892857143</td>
<td>1.963816368</td>
</tr>
<tr>
<td>first run</td>
<td>tree_with_cov</td>
<td>5</td>
<td>10</td>
<td>10</td>
<td>2</td>
<td>94</td>
<td>3.333333333</td>
<td>1.809767105</td>
</tr>
</tbody></table>

## Comments:
- coby noticed that some missing value features are getting high contribution - we should use the flag to zero it? Coby Metzger - are you sure? maybe because of the groups some features in the group are not missing? - Coby thinks it's OK, the imputed value for example when the glucose is high and no HbA1C, the imputation for HbA1C is also high. He likes it. He gave more reasons...
