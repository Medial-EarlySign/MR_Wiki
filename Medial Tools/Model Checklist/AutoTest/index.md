# AutoTest

## Motivation
The goal is to execute generic tests collected from our group as common knowledge on certain use cases 
For example, we have knowledge on how we should test a new model, for example - run feature importance, make sure we have all cleaners for all features etc.
Second thing we achieve is standardize way to validate/document a new model. Suppose to be faster to move from one project to another when needed.

## Location
Under tools repository: [https://github.com/Medial-EarlySign/MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) 
In Linux: MR_Tools/AutoValidation\kits.
Or environment variable: "$AUTOTEST_LIB"

## Use cases
There are 4 use cases:

- [Development](Development%20kit) - testing of new model
- [External Silent Run](External%20Silent%20Run) - auto tests for existin model on dataset WITHOUT labeling
- External_validation_after_SR - autotest for dataset after "External_Silent_Run" when we received the labeling.

## How to create a new TestKit for you AlgoMarker
1. Create empty directory to hold your TestKit
2. cd into the directory
3. Execute: $AUTOTEST_LIB/generate_tests.sh
4. It will ask you which Kit to create: Development , External_retrospective , [External Silent Run](External%20Silent%20Run), External_validation_after_SR - please type in the desired TestKit
5. Please configure "configs/env.sh" and other settings if needed in configs folder
6. Execute ./run.sh to run all tests,. There is "run.specific.sh" - to run a specific test by number, if not providing an argument (number) the scripts output the name of all tests with their number that you can choose.

## How each test is being executed/ How to write new test:
Each test in Tests is given 3 arguments:

1. CFG_PATH_OF_CURRENT_KIT - path to config folder of current kit
2. SCRIPT_DIR_OF_INFRA - path of AutoTest infrastructure
3. OVERRIDE - binary 0/1 if to override previous results
You need to respect those arguments when writing a new test
 
The tests are being executed one after another, there is a unified log of all tests and a specific log for each test.
Output of each test has to be manually **verified** (one should make sure that test results make sense)
There is also a file that show the status of all the Tests called "tests_status.log". Each test has status:

- FINISHED_NEED_VERIFY - test was ended successfully without errors. Please go over output and approve/disapprove the test. 
- FINISHED_FAILED - Test ended successfully without errors, but failed. The outputs seems wrong or raised a problem. need to rerun. When you want to rerun, erase this status row for the test
- FINISHED_VERIFIED - If test ended correctly and verified
- STOPPED_NEED_VERIFY - test crashed, has errors. please verify if that's OK or not. It can be OK for example, if you want to skip the test
- STOPPED_FAILED - test crashed, has errors. You marked this test as failure, Needs to rerun. When you want to rerun, erase this status row for the test
- STOPPED_VERIFIED - test crashed, has errors. You marked this test as OK. 
After test finished for the first time, If has "*_NEED_VERIFY" status. In next time you run run.sh, it will ask you to decide on the status: Approved, Not approved, Rerun test, Skip decision for now.

## configuration
Configuration through parameters exposed in "config" folder. The main parameters are supposed to be defined under configs/env.sh.
All The test are suppose to use/reuse arguments defined in env.sh. When we need external files, like bootstrap json. 
It's good practice to put those files in config folder and reuse the same files in all scripts when needed. 

## Extension
In some cases we want to add more tests, override exiting test. 
We can do that be coping the desires test template from Test/Templates - Either "TEMPLATE_TEST.sh" for shell scripts or "TEMPATE_TEST.py" for python scripts.
The tests are going to be execute based on the base template folder, for example: $AUTOTEST_LIB/kits/**Development**/Tests for Development.
To override existing test in our use case, we can put a new test in our "Tests" folder with the same numeric prefix of the test we want to replace/override in the base template folder.
Base Template:
We have in each Template a row with definition of required arguments from "env.sh", pay attention to that. Make use of existing parameters and add new ones to env.sh as you wish/need.

## Testing the TestKit
There is also test unit to run the TestKit for LGI on "Development", "External_Silent_Run" and "External_validation_after_SR" to test the TestKit.
Please refer to `MR_Tools/AutoValidation/test_kit` and run the test of the desired TestKit.
 
