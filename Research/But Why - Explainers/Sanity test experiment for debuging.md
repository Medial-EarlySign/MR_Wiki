# Sanity test experiment for debuging
Date: 18.11.2019It looks like all our methods are tuned (without a major bug). The results of all the methods look reasonable.Coby passed over 8 samples (out of 140 available) for diabetes predictor (grouped by signals into 11 groups from 69 features) and scored them from 1-4 (the higher the better).We can see the distribution of the scores for each method and the average score:
 
<table><tbody>
<tr>
<th style="text-align: center;">Explainer_name</th>
<th style="text-align: center;">1</th>
<th style="text-align: center;">2</th>
<th style="text-align: center;">3</th>
<th style="text-align: center;">4</th>
<th style="text-align: center;">&lt;EMPTY&gt;</th>
<th style="text-align: center;">Average Score</th>
</tr>
<tr>
<td style="text-align: center;">Tree</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">3.25</td>
</tr>
<tr>
<td style="text-align: center;">missing_shap</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">3.25</td>
</tr>
<tr>
<td style="text-align: center;">LIME_GAN</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">3.125</td>
</tr>
<tr>
<td style="text-align: center;">SHAP_GAN</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">3.125</td>
</tr>
<tr>
<td style="text-align: center;">Tree_with_cov</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">3.125</td>
</tr>
<tr>
<td style="text-align: center;">knn_with_th</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">2.625</td>
</tr>
<tr>
<td style="text-align: center;">knn</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">5</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">132</td>
<td style="text-align: center;">2.5</td>
</tr>
</tbody></table>

 
* Tree = regular tree shapley implementation
* missing_shap - shapley algorithm with 500 random masks. but instead of using GAN or gibbs to generate samples, we use additional predictor (xgboost regression model) to predict the diabetes model scores when seeing random masks of missing values.  the grouping is calculated internally.
* LIME_GAN - LIME algorithm with GAN - sampling random masks and fitting a model - the grouping is calculated internally.
* SHAP_GAN - Shapley algorithm with GAN. sampling random masks and not an exact calculation - the grouping is calculated internally.* Tree_with_cov - the tree implementation with covariance fix
* knn_with_th - the KNN algorithm with threshold of 5% to explainknn - the KNN algorithm without threshold
