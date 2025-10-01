# Development Kit

## Overview

The Development Kit validates newly developed models before integration with AlgoMarker. It ensures your model includes essential components (cleaners, imputers, bootstrap results, etc.) and passes a comprehensive suite of tests using the same dataset as training. For external validation, see the [External Silent Run kit](../External%20Silent%20Run).

## Goals

- Ensure model quality and completeness before deployment.
- Automate validation of key model components.
- Provide reproducible, standardized testing.

## How to Use

Please refere to [Creating a New TestKit for Your Model](../index.md#creating-a-new-testkit-for-your-model)

Review results in your configured output directory.

## Configuration

Set required parameters in `env.sh`. If a parameter is missing for a test, that test will be skipped.

- **REPOSITORY_PATH**: Path to your data repository.
- **MODEL_PATH**: Path to your trained model.
- **WORK_DIR**: Output directory for results.
- **CALIBRATED_MODEL**, **EXPLAINABLE_MODEL**: Optional, for calibration and explainability tests.
- **BT_JSON**, **BT_COHORT**: Bootstrap configuration files.
- **NOISER_JSON**, **TIME_NOISES**, **VAL_NOISES**, **DROP_NOISES**: For noise sensitivity analysis.
- **BASELINE_MODEL_PATH**, **BASELINE_COMPARE_TOP**: For baseline comparison.
- See full parameter list above for details.

## Additional Files

- **coverage_groups.py**: Defines high-risk groups for coverage tests.
- **feat_resolution.tsv**: Controls feature resolution for matrix feature tests.

## Test Descriptions

Each test in this kit is documented separately:

- [Test_01 - Train Samples Over Years](Test_01%20-%20test_train_samples_over_years.md)
- [Test_02 - Test Samples](Test_02%20-%20test%20samples.md)
- [Test_03 - Cleaners](Test_03%20-%20test%20cleaners.md)
- [Test_04 - Imputers](Test_04%20-%20test%20imputers.md)
- [Test_05 - But Why](Test_05%20-%20But%20why.md)
- [Test_06 - Bootstrap Results](Test_06%20-%20bootstrap%20results.md)
- [Test_07 - Feature Importance](Test_07%20-%20feature%20importance.md)
- [Test_08 - Calibration](Test_08%20-%20calibration.md)
- [Test_09 - Coverage](Test_09%20-%20coverage.md)
- [Test_10 - Matrix Features](Test_10%20-%20test%20matrix%20features.md)
- [Test_11 - Matrix Over Years](Test_11%20-%20test%20matrix%20over%20years.md)
- [Test_12 - Fairness](Test_12%20-%20fairness.md)
- [Test_13 - Model Explainability](Test_13%20-%20model%20explainability.md)
- [Test_14 - Noise Sensitivity Analysis](Test_14%20-%20noise%20sensitivity%20analysis.md)
- [Test_15 - Compare to Baseline Model](Test_15%20-%20compare%20to%20baseline%20model.md)