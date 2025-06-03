# Machine Learning Algorithms - Parameter Tuning (C++ Code)
****QRF Regression Tree:****
To Initialize MedQRF predictor you can use MedQRF object. You MUST initialize params.type = QRF_TreeType::QRF_REGRESSION_TREE.
there are 5 different parameters for regression random forest:
1. params.ntrees - which controls the number of trees created in the forest. when this value is big enougth it not suppose to have a big impact making it bigger. the prediction value is the mean average of all trees. theoritically it suppose to converge in big numbers (> 100's)
2. params.maxq- controls how many bins a signal would be divided into (if there are less unique values than this number, it won't do a thing). will be used later for choosing threshold to decide where to split the tree in the signal node. there is a linear shrinkage between min to max value of signal divide by maxq number. if bigger number than the runnint time increases, not suppose to increase overfitting  because it's only searches for split threshold in smaller bin jumps.
3. params.ntry - how many random tries to select signal to split node in the tree .default value is sqrt(number_of_features)
4. params.min_node - split node condition - how many samples should be in node, less than this will not split  node. default is 100
5. params.spread  - split node condition - the minimum diff between min and max in signal to split node. for example, if all the signal values in the the tree node only changes(max_value-min_value) less than spread , it will not split the node. default value is 0.1. depends on the signal resulotion sometime 0.1 has big meaning and sometime it has small meaning
 
Missing Parameters:
1. spliting function creteria - Gini, info gain? other measures
2. configure special params for special signals. for example in some signals you would like to choose diffrent spread
 
****SGD:****
********these are the parameters which effects learning_rate in SGD:
1. B - Blocking Value for W in L2 norm - you need to search for a solution in blocked space. esstimate the L2 norm of your parameter optimal solution (W are the parameters of the model)
2. P - max change in derivate. more specificcly maximal change in (f(x+h)-f(x) )/ h. f(x) can be also not diffrential. you can calculate max diff in each signal maximum value- minimum value and divide with h_size which can be small and not important (0.01, 0.1)
3. h_size - the numeric step for calculating derivate
4. T_Steps - the number of steps the SGD will do
5. sample_size - the sample_size for stochastic gradient decend to calculate derievate, need to be not too small (50, 100 are ok to have enougth samples to calculate gradient) - not very important param and it's not effecting learning rate.There is a simple equation that takes all those params into account in yield the learning_rate and esstimate eppsilon error from optimal solution with a good confidence levelIn my code you can ran:learner.set_blocking(B); //for projection step when solution is outside boundleaner.set_gradient_params(sample_size, h_size);learner.set_learning_rate(B, P, T_Steps);leaner.output_num = T_Steps / 5; // If you want the SGD to output each T_steps/5 rounds the error. if set to 0 which is default won't output anything
