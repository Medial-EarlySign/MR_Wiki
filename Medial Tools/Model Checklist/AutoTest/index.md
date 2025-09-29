# AutoTest

## Motivation

AutoTest aims to standardize and accelerate model validation by providing generic tests and documentation practices. It helps ensure consistent quality and makes it easier to transition between projects by applying common knowledge and best practices for model testing (e.g., feature importance checks, verifying feature cleaners).

## Location

* Repository: [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools)
* Path: `AutoValidation/kits`
* Alternatively, set the environment variable: `$AUTOTEST_LIB`

## Use Cases
AutoTest supports three main scenarios:

- [Development](Development%20kit) - Test new models during development.
- [External Silent Run](External%20Silent%20Run) - Run auto tests on datasets without labels/outcomes.
- External_validation_after_SR - Test datasets with labels/outcomes, extending the silent run with additional analyses and sanity checks.

## Creating a New TestKit for Your Model

1. Create an empty directory for your TestKit.
2. Navigate into the directory.
3. Execute: `$AUTOTEST_LIB/generate_tests.sh`
4. Select the desired TestKit type: [Development](Development%20kit), [External Silent Run](External%20Silent%20Run), or External_validation_after_SR.
5. Configure `configs/env.sh` and other settings as needed in configs folder
6. Run all tests with `./run.sh`. To run a specific test, use `run.specific.sh`. Without arguments, it lists all available tests and their numbers.


## Writing and Executing Tests
Each test in the `Tests` directory receives three arguments:

1. `CFG_PATH_OF_CURRENT_KIT`: Path to the current kit’s config folder.
2. `SCRIPT_DIR_OF_INFRA`: Path to the AutoTest infrastructure.
3. `OVERRIDE`: Binary flag (0/1) to override previous results.

Tests run sequentially, with unified and per-test logs. After execution, manually verify the output to ensure results are meaningful.

Test statuses are tracked in `tests_status.log`:

- `FINISHED_NEED_VERIFY`: Test completed successfully; review and approve/disapprove.the test. 
- `FINISHED_FAILED`: Test completed but failed; rerun after clearing the status.
- `FINISHED_VERIFIED`: Test completed and verified.
- `STOPPED_NEED_VERIFY`: Test crashed; review for acceptability.
- `STOPPED_FAILED`: Test crashed and marked as failed; rerun after clearing the status.
- `STOPPED_VERIFIED`: Test crashed but marked as OK.

If a test has a `*_NEED_VERIFY` status, the next run of `run.sh` will prompt you to approve, disapprove, rerun, or skip the decision.


## Configuration

Main parameters are defined in `configs/env.sh`. All tests should use/reuse these arguments. Place external files (e.g., bootstrap JSON) in the config folder for consistency.
Easier to reuse same parameters over all tests in that way.

## Extension
To add or override tests:

* Copy the desired template from `Test/Templates` (`TEMPLATE_TEST.sh` for shell, `TEMPATE_TEST.py` for Python).
* Place new or overridden tests in your `Tests` folder, using the same numeric prefix as the base template to override.
* Templates specify required arguments from `env.sh`; reuse and extend as needed.

## Testing the TestKit

Unit tests for the TestKit are available for LGI in "Development", "External_Silent_Run", and "External_validation_after_SR". See `MR_Tools/AutoValidation/test_kit` to run the desired TestKit tests.
