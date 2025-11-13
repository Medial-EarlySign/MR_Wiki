
# AutoTest

## Motivation

AutoTest standardizes and accelerates model validation by providing generic tests and documentation practices. It ensures consistent model quality and simplifies transitions between projects by applying best practices for model testing (e.g., feature importance checks, cleaner verification).

### Goals
- Automate validation of models and data repositories
- Enable reproducible and standardized testing across environments
- Support a wide range of validation tasks (fairness, coverage, feature importance, etc.)
- Provide extensible configuration and resource templates

## Location

- **Repository:** [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools)
- **Path:** `AutoValidation/kits`
- **Environment variable:** `$AUTOTEST_LIB` (set to the kits path for convenience)

The `kits/` directory contains the main test kits and scripts for running validation workflows. Each kit is tailored for a specific validation scenario, such as development, silent run, or external validation after silent run.

## Use Cases
AutoTest supports three main scenarios:

- [Development](Development%20kit): Test new models during development.
- [External Silent Run](External%20Silent%20Run): Run auto tests on datasets without labels/outcomes.
- [External_validation_after_SR](External_validation_after_SR): Test datasets with labels/outcomes, extending the silent run with additional analyses and sanity checks.

## Creating a New TestKit for Your Model

To set up a new TestKit for your model:

1. Create an empty directory for your TestKit.
2. Navigate into the directory.
3. Run the generator script:
	```bash
	$AUTOTEST_LIB/generate_tests.sh
	```
	(`AUTOTEST_LIB` should point to the cloned [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools/tree/main/AutoValidation/kits) repository.)
4. When prompted, select the desired TestKit type: [Development](Development%20kit), [External Silent Run](External%20Silent%20Run), or **External_validation_after_SR**. This creates a template directory with example configuration files you can adapt for your model. The `Tests` directory starts empty; all tests are executed from `$AUTOTEST_LIB/$KIT_NAME/Tests` unless you override them in your own `Tests` folder.
5. Configure `configs/env.sh` and other settings in the `configs` folder. To override tests for your specific use case, place them in your `Tests` folder. For generic changes affecting all models, edit the corresponding test in the infrastructure folder (`$AUTOTEST_LIB/$KIT_NAME/Tests`).
6. Run all tests with:
	```bash
	./run.sh
	```
	To run a specific test, use:
	```bash
	./run.specific.sh
	```
	(Without arguments, it lists all available tests and their numbers.)

## Writing and Executing Tests

Each test in the `Tests` directory receives three arguments:

1. `CFG_PATH_OF_CURRENT_KIT`: Path to the current kit’s config folder.
2. `SCRIPT_DIR_OF_INFRA`: Path to the AutoTest infrastructure.
3. `OVERRIDE`: Binary flag (0/1) to override previous results.

Tests run sequentially, with unified and per-test logs. After execution, manually verify the output to ensure results are meaningful.

Test statuses are tracked in `tests_status.log`:

- `FINISHED_NEED_VERIFY`: Test completed successfully; review and approve/disapprove.
- `FINISHED_FAILED`: Test completed but failed; rerun after clearing the status.
- `FINISHED_VERIFIED`: Test completed and verified.
- `STOPPED_NEED_VERIFY`: Test crashed; review for acceptability.
- `STOPPED_FAILED`: Test crashed and marked as failed; rerun after clearing the status.
- `STOPPED_VERIFIED`: Test crashed but marked as OK.

If a test has a `*_NEED_VERIFY` status, the next run of `run.sh` will prompt you to approve, disapprove, rerun, or skip the decision.

## Configuration

Main parameters are defined in `configs/env.sh`. All tests should use/reuse these arguments. Place external files (e.g., bootstrap JSON) in the config folder for consistency. This makes it easier to reuse parameters across all tests.

## Extension

To add or override tests:

- Copy the desired template from `Test/Templates` (`TEMPLATE_TEST.sh` for shell, `TEMPLATE_TEST.py` for Python).
- Place new or overridden tests in your `Tests` folder, using the same numeric prefix as the base template to override.
- Templates specify required arguments from `env.sh`; reuse and extend as needed.

Guide for writing/adding a new test: [Add a new AutoTest](Add_a_new_AutoTest.md)

## Testing the TestKit

Unit tests for the TestKit are available for LGI in "Development", "External_Silent_Run", and "External_validation_after_SR". See `MR_Tools/AutoValidation/test_kit` to run the desired TestKit tests.
