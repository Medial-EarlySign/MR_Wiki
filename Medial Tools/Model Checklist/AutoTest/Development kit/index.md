# Development kit

## Motivation
This test kit is used to test a NEW developed model before wrapping it to AlgoMarker.
It will make sure the model has cleaners, imputers, bootstrap results and some other test.
This will support the validation of a model on the same dataset used to train the model. External validation tests is in different kit.

## Configuration
We will call our test kit code folder as TEST_KIT.
The main configuration file can be found under current TEST_KIT/config/env.sh
Parameters:

- REPOSITORY_PATH - A path to the repository use to develop the mode - train (& test)
- TRAIN_SAMPLES_BEFORE_MATCHING - Path to raw train samples before matching
- TEST_SAMPLES/PREDS_CV - path to test samples that we can apply the model on without over-fitting (a different set of patient). Or use PREDS_CV to prediction files collection in cross validation manner (fir example by cv or Optimizer)
- MODEL_PATH - Path of the model
- WORK_DIR - Output of the KIT
- CALIBRATED_MODEL - path to calibrated model if applicable calibration tests. It's by default referenced to the same MODEL_PATH. "CALIBRATED_MODEL=${MODEL_PATH}"
- EXPLAINABLE_MODEL - path to model with explainability if applicable (recommended to create one). It's by default referenced to the same MODEL_PATH.
- TEST_SAMPLES_CALIBRATION - set of test samples to test model calibration. It's by default referenced to the same TEST_SAMPLES
- BT_JSON - bootstrap json path. It is reference by default to the current config folder /bootstrap/bootstrap.json. We will use this json to generate features for bootstrap analysis.
    - bootstrap/bootstrap.json - a bootstrap json file to run bootstrap_app
- BT_COHORT - bootstrap cohorts definition file for bootstrap analysis. It is reference by default to the current config folder /bootstrap/bt.params
    - bootstrap/bt.params - a bootstrap cohorts file for bootstrap_app
- NOISER_JSON - a json that defines rep processors to "noise" the inputs and test model sensitivity to noise. It references a file in current folder named: noiser_base.json. Please refer to [Noiser](../../../../Infrastructure%20C%20Library/01.Rep%20Processors%20Practical%20Guide/Noiser.md) page for more details.
- TIME_NOISES - vector of values to control the noise in dates. The unit is days, so "30" means uniform randomly shifting dates between 0-30 days backward of all signals in NOISER_JSON.
- VAL_NOISES - vector of values to control the noise in signal values. The unit is standard deviation multiply by 10 - so "1" means "0.1" * signal std. This will control normal random noise standard deviation based on signal std.
- DROP_NOISES - vector of values to control the probability to "drop" tests/values. The unit is probability multiply by 10 - so "1" mean "0.1"/10% chances to drop a lab test value in certain date.
- BT_JSON_CALIBRATION - bootstrap json to control calibration cohorts if they are different than regular cohorts. By default it is the same as regular bootstrap: BT_JSON_CALIBRATION=${BT_JSON}
- BT_COHORT_CALIBRATION - bootstrap cohort definitions for calibration. By default it is the same as regular bootstrap
- EXPLAIN_JSON - bootstrap json to control explainability cohorts if they are different than regular cohorts. By default it is the same as regular bootstrap: EXPLAIN_JSON=${BT_JSON}
- EXPLAIN_COHORT - bootstrap cohort definitions for explainability. By default it is the same as regular bootstrap
- BT_JSON_FAIRNESS - bootstrap json to control fairness cohorts if they are different than regular cohorts. By default it is the same as regular bootstrap: BT_JSON_FAIRNESS=${BT_JSON}
- FAIRNESS_BT_PREFIX - A single cohort to filter samples to test fairness. The syntax is the same as bootstrap cohort. [bootstrap_app](../../../bootstrap_app)
    - "configs/fairness_groups.cfg" - more info in [Test_12 - fairness](Test_12%20-%20fairness.md)
- FAIRNESS_MATCHING_PARAMS - Control How to do matching between groups if fairness isn't met. The default is to do the matching by age - 10 years bin.
- BASELINE_MODEL_PATH - A path to baseline model to compare with
- BASELINE_COMPARE_TOP - compare top X% to compare our model with baseline model. van diagram and more...
We have 2 additional files:
- coverage_groups.py - which defines with python pandas special high risk groups by rules - for example old patients, etc. That we want to see that the model flags/selects them more than random as sanity test. more into in [Test_09 - coverage](Test_09%20-%20coverage.md)
- feat_resolution.tsv - controls feature resolution when plotting to html the graphs. more info in [Test_10 - test matrix features](Test_10%20-%20test%20matrix%20features.md)
