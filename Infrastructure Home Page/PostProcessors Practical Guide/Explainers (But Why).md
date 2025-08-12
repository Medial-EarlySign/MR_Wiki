# Explainers (But Why)
[ModelExplainer (code doc)](https://Medial-EarlySign.github.io/MR_LIBS/classModelExplainer)
ModelExplainer API:
<img src="/attachments/11206683/11206684.png"/>
 
## ModelExplainer Types:
- [TreeExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classTreeExplainer)  – explains model with SHAPLEY implementation for trees (it has 2 additional flags – do interaction calculation for shap values or use approximate calculation which is faster):
    -  If tree model has its own implementation for shapley (like XGboost, LightGBM) – will use those methods directly
    - If the model is based on ensemble trees (like QRF) it will convert the model into generic tree model in learn. Than in Apply it will run SHAP algorithm for trees with the given flags. I made the function parallel
    - If it's other MedPredictor – it will learn other ensemble trees model (for example XGBoost) based on parameters for the predictor. The model will  be "proxy model" for our model and will learn the original model output (regression problem) and will run SHAP algorithm for trees for the proxy model to explain scores It's just backup algorithm for models that are not ensemble trees…
- [ShapleyExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classShapleyExplainer) - Agnostic SHAP algorithm, may use Gibbs, GAN as generators for the process. It also has sampling parameters for the mask to speed up the calculation. Still very slow implementation – it's here because we already written it and maybe in the future for some specific research problems it may be useful. Maybe to compare with other methods
- [LimeExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classLimeExplainer) -  Agnostic SHAP algorithm, may use Gibbs, GAN as generators for the process. It has sampling parameters for the mask to speed up the calculation and fits linear model to the random masks. It's faster the Shapley because the runtime is O(Number_of_masks)*generate_samples. In Shapley we do this for each feature again, with and without the specific feature. so Shapley with the same sampling args is slower by 2*number of features. the linear fit time is very fast
- [MissingShapExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classMissingShapExplainer) – Agnostic SHAP algorithm that doesn't use Gibbs or GAN and is much faster… the Algorithm trains proxy model (with same parameters as original model) on the outcome with added masked samples. masked samples are samples where feature values were removed on the mask and replaced with missing value. It reweights all training samples to match SHAP weights for each mask. The results on the simulated data(which are very simple) looks good for lightGBM model, the runtime is also very good. The idea is that the proxy model can now handle much better missing values and we can just feed the model with missing values instead of generating "real" samples. Theoretically for linear\polynomial kernel it's should work(and works) very good
- [LinearExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classLinearExplainer) - Simple Explainer for linear models to return feature_value*coeff. The implementation is generic for all models - for each feature\group of features, the contribution is calculated as the difference between the model score with the original feature value versus the model score with the feature value set to 0. It's similar to Shapley but much faster - taking mask of all 1's so no need to generate values with Gibbs\GAN. Very similar implementation to MissingShapExplainer but without proxy model
- [KNNExplainer](https://Medial-EarlySign.github.io/MR_LIBS/classKNN__Explainer) -An explainer that calculates average score for neighbours of sample in training data,  when  neighborhood is calculatesd with and without the tested feature, and the ratio between the two is returned.


<table><tbody>
<tr>
<th>Explainer</th>
<th>type string to put in json</th>
<th>internal support for grouping of features</th>
<th>Additional options</th>
<th>Advantages</th>
<th>run_time</th>
</tr>
<tr>
<td>TreeExplainer</td>
<td>"tree_shap"</td>
<td>NO</td>
<td>Support for Interaction values<br/>Supoprt for approximate alg - Saabas alg which is faster</td>
<td>Accurate</td>
<td>very fast!!</td>
</tr>
<tr>
<td>ShapleyExplainer</td>
<td>"<span style="color: rgb(0,0,0);">shapley</span>"</td>
<td>YES</td>
<td> </td>
<td><p><span><span>Accurate (when not sampling)</span></span></p><p><span>Model Agnostic</span></p></td>
<td>Very Slow, depend heavily in the number of features</td>
</tr>
<tr>
<td>LimeExplainer </td>
<td>"<span style="color: rgb(0,0,0);">lime_shap</span>"</td>
<td>YES</td>
<td> </td>
<td><p>Accurate (when not sampling)</p><p>Model Agnostic</p></td>
<td>Slow, but can be feasible</td>
</tr>
<tr>
<td>MissingShapExplainer </td>
<td>"missing_shap"</td>
<td>YES</td>
<td> </td>
<td><span>Model Agnostic</span></td>
<td>very fast!!</td>
</tr>
<tr>
<td>LinearExplainer </td>
<td>"<span style="color: rgb(0,0,0);">linear</span>"</td>
<td>YES</td>
<td> </td>
<td> </td>
<td>fastest!!</td>
</tr>
<tr>
<td>KNNExplainer</td>
<td>"knn"</td>
<td>NO</td>
<td><p>May use raw score or thresholded score.</p><p>May set a threshold ifnot given.</p></td>
<td>Model agnostic.</td>
<td>fast</td>
</tr>
</tbody></table>
 

## Global Arguments for all explainers:
- [filters](https://Medial-EarlySign.github.io/MR_LIBS/classExplainFilters)
    - max_count - maximal number of features\groups to keep for explaining 
    - sum_ratio - the maximal number of features\groups to keep for explaining when considering the sum of top features contributions as ratio from the total contributions . in range 0-1, 1 - means take all
    - sort_mode - 0 sort feature contributions by applying ABS (no importance for sign), +1 - sort only positive contributions , -1 - sort only negative contributions 
- [processing](https://Medial-EarlySign.github.io/MR_LIBS/classExplainProcessings)
    - learn_cov_matrix - If turned on will use the train_matrix to calculated Covarince matrix and will aggregate the contributions for all correlated features\groups according to covariance 
    - cov_features - covarince matrix path, If we want to use extrernal covariance matrix instead of calculating on train matrix
    - group_by_sum - If turned on will use External grouping to calculate group contribution using sum of each feature in the group. for example in TreeExplainer this is the only way to calculate contribution for group, the other explainers has specific special implementation for grouping
    - grouping - a file path for grouping or the keyword "BY_SIGNAL" to group each feature by it's signal. If file path is provided the file format is tab-delimited with 2 fields: feature_name_to_search_in_features, group_name
