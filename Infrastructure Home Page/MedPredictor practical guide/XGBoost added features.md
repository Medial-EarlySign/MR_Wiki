# XGBoost added features
- **S**
  - When using gbtree::updater_colmaker::spit_evaluator==ElasticNet, it is possible to add feature specific additive penalties
    - Parameter format - a string "fid:valfid:val,..."
    - When spliting according to id fid, loss-change is decreased by val
    - if a given feature-id is not given in the string, the corresponding penalty is 0
    - In MedXGB intialization, give "feature-name:valfeature-name:val,..."
 
- ****
  - It is actually XGB standard constraint, but we need some translation to reach the required format
  - Our parameter format: monotone_constraints=f1:d1#f2:d2#...
  - Where:
    - f is part of a unique feature name, and
    - d is a direction: 1 for up and -1 for down
  - Currently NO defense against raw values/format, and
  - Bad outcome (feature format not recognized by XGB) yield all predictions = 0.5 without warning
