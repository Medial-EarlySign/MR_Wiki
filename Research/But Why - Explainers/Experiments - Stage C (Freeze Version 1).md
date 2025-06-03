# Experiments - Stage C (Freeze Version 1)

After some discussions and ideas to improve the covariance fix in order to better handle with similar and dependent features.

As you probably remember, Shapley Values should split the contribution equally to features that are the same,

so if important features has many similar features, it may result in a wrong ButWhy report.

This method is used togheter with the "iterative" method.

 

The current method is to calculate the covariance matrix of the features and multiply it by the contributions. The problem arises when you have groups.

When using groups those are the new options (the first option is what we had in the last experiment):

In all options these are the definitions:

Let's mark the features covariance matrix as F(i,j) is size NxN (N is the number of features). Build "covariance matrix" for groups (if we have G groups, the matrix size is GxG), lets mark it C matrix. C(i,i)=1. C(i,j)=C(j,i) the matrix is symmetric

1. C(i,j) := max{ F(k,l) | k is feature in group i, l is feature in group j }

2. Let's mark feature contribution for the prediction as vector T in size N as the number of features (taking the contribution of the features without iterations) .C(i,j) := Sigma( k is feature in group i, l is feature in group j) { F(k,l)*T(k)*T(l) } / Sigma( k is feature in group i, l is feature in group j) { 1*T(k)*T(l) }

The advantage in equation #2 is that it should maybe better since it's not taking "max" and using specific feature contributions.

 

Added another options to the calculation of the "covariance" matrix of features differently by using mutual information between features instead of correlation. The idea is to catch better non-linear behaviors like BMI and some other and more complicate feature dependencies that linear model can miss.

Used normalization factor to control the values to be between 0-1. 0 - the features are independent, 1 - you can determine the second feature from the first feature.

The equation for mutual information is KLD between the joint features distribution and calculation of the joint probability assuming they are independent (you measure the information gain between the assumption of in-dependency to what you observe in the data). Normalization is done by dividing with the entropy of the joint distribution. The normalization causes all number to be between 0-1 as we want and duplicate features will get 1.

 

The following file has 4 methods to compare (covariance or mutual information and equation 1 or equation 2) W:\Users\Alon\But_Why\outputs\Stage_B\explainers\crc\reports\compare_new_cov_fix\compare_all.xlsx.

I did it for CRC which is the most challenging problems since we have many features and similar once.

## Results

Alon Results [compare_all.Alon.xlsx](attachments/11207625/11207623.xlsx)

<table><tbody>

<tr>

<th>Method/score</th>

<th>1</th>

<th>2</th>

<th>3</th>

<th>4</th>

<th>5</th>

<th>Average</th>

<th>Average_0.5</th>

</tr>

<tr>

<td>Tree_iterative_covariance(New equation)</td>

<td>0</td>

<td>0</td>

<td>0</td>

<td>2</td>

<td>20</td>

<td>4.909091</td>

<td>2.214607252</td>

</tr>

<tr>

<td>Tree_iterative_mutual_information(New equation)</td>

<td>0</td>

<td>0</td>

<td>0</td>

<td>3</td>

<td>19</td>

<td>4.863636</td>

<td>2.20387689</td>

</tr>

<tr>

<td>Tree_iterative_mutual_information(MAX)</td>

<td>0</td>

<td>0</td>

<td>0</td>

<td>10</td>

<td>12</td>

<td>4.545455</td>

<td>2.128764351</td>

</tr>

<tr>

<td>Tree_iterative_covariance(MAX)</td>

<td>0</td>

<td>0</td>

<td>7</td>

<td>9</td>

<td>6</td>

<td>3.954545</td>

<td>1.979125614</td>

</tr>

</tbody></table>

Coby results [compare_all - Coby.xlsx](attachments/11207625/11207634.xlsx):

<table><tbody>

<tr>

<th>Method/score</th>

<th>1</th>

<th>2</th>

<th>3</th>

<th>4</th>

<th>5</th>

<th>Average</th>

<th>Average_0.5</th>

</tr>

<tr>

<td>Tree_iterative_covariance(New equation)</td>

<td>0</td>

<td>0</td>

<td>3</td>

<td>11</td>

<td>7</td>

<td>4.19047619</td>

<td>2.04041087</td>

</tr>

<tr>

<td>Tree_iterative_mutual_information(New equation)</td>

<td>0</td>

<td>0</td>

<td>8</td>

<td>10</td>

<td>3</td>

<td>3.761904762</td>

<td>1.931648114</td>

</tr>

<tr>

<td>Tree_iterative_mutual_information(MAX)</td>

<td>0</td>

<td>1</td>

<td>5</td>

<td>5</td>

<td>3</td>

<td>3.714285714</td>

<td>1.913047967</td>

</tr>

<tr>

<td>Tree_iterative_covariance(MAX)</td>

<td>0</td>

<td>6</td>

<td>10</td>

<td>4</td>

<td>0</td>

<td>2.9</td>

<td>1.690289472</td>

</tr>

</tbody></table>

## Conclusions

- The new equation seem to improve the results. Use it instead of max, that's the default in ExplainProcessings (use_max_cov=0)

- The mutual information might improve the results. I can't see it when using the new equations since the average score is in saturation (almost all recieved 5 out of 5). Coby and I noticed a huge improvement for the mutual information compared to the covariance when using MAX instead of new equation. Yet, we both got that the best results for CRC are new equations with covaraince.Waiting for [Avi Shoshan](http://confluence:8090/display/~avi-internal) and [yaron](http://confluence:8090/display/~yaron-internal) to review the file and grade the results themselves if they want (maybe they will see different things). **Currently my recommandation is to use the new equation with covaraince (also faster learning).** 

 

To create a nice ButWhy report, you might use:

1. adjust model app to add post_processor with explainer to the model. Later you can change some parameters if needed using change_model (without relearn)

2. CreateExplainnReport app to generate a nice report

 

