# Factorization Machines
 
## Rationale
 
Classifiers currently used in Medial make use of different types of features, in particular features based on e.g. RC (read codes) or ATC (drug codes).
Due to a large number of RC and ATC codes, the total number of RC/ATC features can be very high (200K in CKD Fast Progressors project).
In addition, these features are extremely sparse.
It would be computationally prohibitive to handle all this features in XGBoost.
In order to solve this problem, there exists a "[category_depend](/Infrastructure%20Home%20Page/02.Feature%20Generator%20Practical%20Guide)" mechanism, which reduces a number of RC/ATC features by keeping only features which are highly correlated to the outcome.
Therefore, information about some read codes or drugs is lost. 
 
This project was undertaken in order to check whether it is possible to retain this information by means of  "Factorization Machines" method,
which is suited to work with a large number  of extremely sparse features, and is widely used in Recommender System. 
 
## Factorization machines
 
Factorization Machines (FM) are generic supervised learning models that map arbitrary real-valued features into a low-dimensional latent factor space and can be applied naturally to a wide variety of prediction tasks including regression, classification, and ranking. FMs can estimate model parameters accurately under very sparse data and train with linear complexity, allowing them to scale to very large data sets. FMs are widely used for real-world recommendation problems.
FM model is described in details in the [article](https://www.csie.ntu.edu.tw/~b97053/paper/Rendle2010FM.pdf) by Steffen Rendle.
## libFM
 
[libFM is a software implementation for factorization machines that features stochastic gradient descent (SGD) and alternating least squares (ALS) optimization as well as Bayesian inference using Markov Chain Monte Carlo (MCMC).](http://www.libfm.org/)
Links to the source code and Windows executable can be found at [libfm.org](http://www.libfm.org/)
LibFM manual is available [here](http://www.libfm.org/libfm-1.42.manual.pdf).
## Workflow
 
We tested performance on libFM on a number of datasets, all based on the source dataset from the CKD Fast Progressors project.
We decided to omit all the lab test-based features, since these are dense, while libFM is more suited to work on sparse binary and categorical features.
Each subsequent set includes more features than the previous one, up to 200K+ features.
Where possible we compared results returned by libFM to those of XGBoost, trained on respective data (using the same configuration that was used in CKD Fast Progressors project)
## Datasets
 
1. Age, Gender columns only
2. Age,Gender and all RC-related and ATC-related columns of type "category set" used in CKD Fast Progressors project (not including features generated via "category_depend" mechanism)
3.  Age,Gender,RC-related and ATC-related columns of type "category set" and "category_depend" used in CKD Fast Progressors project 
4. Age,Gender and a sparse matrix of RC and ATC-related features generated using [Embeddings](/Infrastructure%20Home%20Page/03.FeatureProcessor%20practical%20guide/Embeddings) project (with some columns dropped using "shrinkage" mechanism, descibed in the Embeddings project documentation)  
5. Age,Gender and a sparse matrix of RC and ATC-related features generated using [Embeddings](/Infrastructure%20Home%20Page/03.FeatureProcessor%20practical%20guide/Embeddings) project (this time without using "shrinkage'). Resulting matrix has 200K+ columns.
## Results
1. Age, Gender columns only
2. 
Age,Gender and all RC-related and ATC-related columns of type "category set" used in CKD Fast Progressors project 
(not including features generated via "category_depend" mechanism)
Results produced by libFM are marginally better in this scenario
<table><tbody>
<tr>
<td>Classifier</td>
<td>AUC</td>
</tr>
<tr>
<td>Linear</td>
<td>0.541</td>
</tr>
<tr>
<td>XGBoost</td>
<td>0.573</td>
</tr>
<tr>
<td>libFM</td>
<td>0.581</td>
</tr>
</tbody></table>

3.  Age,Gender,RC-related and ATC-related columns of type "category set" and "category_depend" used in CKD Fast Progressors project 
4. Age,Gender and a sparse matrix of RC and ATC-related features generated using [Embeddings](/Infrastructure%20Home%20Page/03.FeatureProcessor%20practical%20guide/Embeddings) project (with some columns dropped using "shrinkage" mechanism, descibed in the Embeddings project documentation)  
5. Age,Gender and a sparse matrix of RC and ATC-related features generated using [Embeddings](/Infrastructure%20Home%20Page/03.FeatureProcessor%20practical%20guide/Embeddings) project (this time without using "shrinkage'). Resulting matrix has 200K+ columns.
 
 
 
 
 
