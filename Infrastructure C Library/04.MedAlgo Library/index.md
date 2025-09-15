# MedAlgo Library
## General
 
The MedAlgo library (together with its accompanying algorithm libraries) is a general wrapper for several ML algorithms allowing learn , predict and parameters configuration.
 
 
General Usage Example:
 
**Using MedPredictor**
```c++
#include <MedAlgo/MedAlgo/MedAlgo.h>
 
// .... create your train and test matrices ...
MedMat<float> Xtrain,Ytrain,Xtest,Ytest;
 
// define a MedPredictor pointer
MedPredicor *predictor;
 
// Create model of choice (here in example linear model)
predictor = MedPredictor::make_predictor("linear_model");
 
// Initialize parameters for this model (here in example putting rfactor , the 1-ridge , to be 0.9)
predictor->init_from_string("rfactor=0.9");
 
// Learn on Train , this will build a model. Here we use MedMat<float> matrices for X and Y
// There are other API's as well - for example c like API's , please look at the MedPredictor class for more options
predictor->learn(Xtrain,Ytrain);
 
// Predict on Test , here we use an API that uses an Xtest MedMat<float> for test, and a vector<float> for predictions
// There are other API's as well - for example c like API's , please look at the MedPredictor class for more options
vector<float> preds;
predictor->predict(Xtest,preds);
 
// That's it ... now you have the predictions and can test the performance.
// More on options to test performance and serialize and save models below.
 
 
```

## Predictors and their parameters
 
### Linear Model
- Use MedPredictor::make_predictor("linear_model")
- Parameters:
    - rfactor - 1.0: no ridge , closer to 0.0 - stronger ridge. Reccomended: 0.9 for regular runs, 0.3 for highly regularaized runs.
**Linear Model example**
```c++
MedPredicor *predictor;
predictor = MedPredictor::make_predictor("linear_model");
predictor->init_from_string("rfactor=0.9");
predictor->learn(Xtrain,Ytrain);
```
 
### XGBoost
- Use MedPredictor::make_predictor("xgb")
- Parameters
    - seed
    - booster
    - objective
    - eta - step size in each iteration , should be slow enough to avoid overfitting, and fast enough to get somewhere. If num_round is large, use a small eta and vice versa.
    - num_round - how many trees to build. Running time is linear with this parameter.
    - gamma
    - max_depth - of trees
    - min_child_weight - limiting size of leaves (larger = more regularization)
    - missing_value - you can sign the algorithm what are the missing values (if there are any) in your matrix.
    - lambda
    - alpha
    - scale_pos_weight - allows to fix imbalances in data
    - tree_method
 
**XGBoost example**
```
MedPredicor *predictor;
predictor = MedPredictor::make_predictor("xgb");
predictor->init_from_string("booster=gbtree;objective=binary:logistic;eta=0.05;gamma=1;max_depth=5;num_round=50;min_child_weight=6");
predictor->learn(Xtrain,Ytrain);
```
### QRF
- Use MedPredictor::make_predictor("qrf")
- Parameters:
    - ntrees - number of trees to build
    - maxq - max number of quantized cells for a parameter
    - type - one of: binary , regression , categorical_chi2 , categorical_entropy
    - min_node - split only nodes of size above this (larger = more regularization)
    - ntry - how many random features to test in each node. -1 (or 0) is default and means sqrt(num_features), a specific number is the actual requested ntry. (smaller = more regularization)
    - max_samp - how many samples to bag for each tree (total neg+pos). 0 means - bag at the number of input and is default. (smaller = more regularization)
    - n_categ - number of categories. 0/1 for regression , 2 for binary problems, 3 and more for multicategorical data
    - spread - in regression trees nodes with difference from max to min below spread will not split.
    - sampsize - a vector (with , delimeter) stating how many samples to take for each tree from each category. example: sampsize=5000,1000 for a binary problem means bag 5000 neg and 1000 pos for each tree.
    - get_count - 
        - 0 : avg majority of nodes (less recommended)
        - 1 : avg probabilities in nodes (in regression = weighted average of nodes , taking their size into account) - recommended
        - 2:  avg counts in nodes - recommended
    - get_only_this_categ - 
        - -1 : get predictions for all categories one after the other (output size is nsamples*n_categ)
        - 0...n_categ-1 : get only the predictions for this categ (output size is nsamples)
    - learn_nthreads - how many threads to use in learn (use 8 for windows, and 24 for linux servers)
    - predict_nthreads - how many threads to use in predict (use 8 for windows, and 24 for linux servers)
 
**QRF example**
```c++
MedPredicor *predictor;
predictor = MedPredictor::make_predictor("qrf");
 
// classification example
predictor->init_from_string("type=categorical_entropy;ntrees=200;min_node=30;n_categ=2;get_only_this_categ=1;sampsize=15000,5000;learn_nthreads=24;predict_nthreads=24");
predictor->learn(Xtrain,Ytrain);
 
// regression example
predictor->init_from_string("type=regression;ntrees=200;min_node=100;n_categ=1;spread=0.1;learn_nthreads=24;predict_nthreads=24");
predictor->learn(Xtrain,Ytrain);
```
 
### **GDLM**
The gdlm package provides algorithms for linear and logistic regression with ridge and lasso regularizations. The solution is via gradient descent.

- use "gdlm" as the name for the predictor.
- Parameters:
    - method: one of full , sgd or logistic_sgd
        - full : full exact solution to the linear regression problem. Can be slow on huge matrices. Less recommended, but works. Not supporting lasso.
        - sgd : gradient descent solution to the linear problem with least square loss and optional ridge and/or lasso regularizers.
        - logistic_sgd : gradient descent solution to the logistic loss function with optional ridge and/or lasso regularizers.
    - normalize : 0/1 : use 1 if you want the algorithm to normalize the matrix before the optimization. Note that the algorithms converge only when data is normalized, so use this if data was not prepared normalized.
    - l_ridge : the ridge gamma
    - l_lasso : the lasso gamma (you'll have to play and find the gamma value that works for you. Typically very small values are needed (0.01, 0.001 , etc).
    - max_iter : maximal number of iterations (an iteration is a full epoch through all the data)
    - err_freq : print summary and check stop condition each err_freq iterations
    - batch_size : the batch size for the gradient descent (coefficients are updated after every batch of course)
    - rate : learning rate
    - rate_decay : allow rate to slowly decrease (or stay constant if decay is 1).
    - momentum : for gradient descent
    - stop_at_err : once the relative improvement in loss falls below this value, the optimazation will stop.
    - last_is_bias : leave 0 usually, is there for cases where a bias is given with the x values.
    - nthreads : number of threads for matrix operations. Number of cores (12 in our nodes) is typically a good choice.
**MedGDLM init examples**
```c++
MedPredictor *predictor;
predictor = MedPredictor::make_predictor("gdlm");
 
// classification example with logistic regression , lasso of 0.01 , learning rate of 0.001 and normalization pre running
predictor->init_from_string("method=logistic_sgd;last_is_bias=0;stop_at_err=1e-4;batch_size=2048;momentum=0.95;rate=0.001;rate_decay=1;l_ridge=0;l_lasso=0.01;err_freq=10;nthreads=12;normalize=1");
predictor->learn(Xtrain,Ytrain);
 
// same but regression example with least squares and lasso
predictor->init_from_string("method=sgd;last_is_bias=0;stop_at_err=1e-4;batch_size=2048;momentum=0.95;rate=0.001;rate_decay=1;l_ridge=0;l_lasso=0.01;err_freq=10;nthreads=12;normalize=1");
predictor->learn(Xtrain,Ytrain);
```
 
