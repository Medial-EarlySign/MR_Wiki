## Goal
The goal is to optimize hyper parameters.
the options are main focused on MedPredictor parameters, but we can also specify weights and different samples for training
and combineing all those options.
Please use `Optimizer --help` compiles using AllTools

## **lightgbm_model.options**

```ini
verbose=0
silent=2
num_threads=15
num_trees=200
metric=auc
objective=binary
learning_rate=0.01,0.03,0.05
lambda_l2=0
metric_freq=1000
min_data_in_leaf=100,500,1000,2000
feature_fraction=0.8,1
bagging_fraction=0.8
bagging_freq=5
max_bin=250
boosting_type=gbdt
max_depth=0,5,6,7
min_data_in_bin=50
```