# Test 19 - Missing Mappings

## Purpose
This test identifies diagnosis codes present in the dataset that are not found in the model's internal dictionaries. These are considered "unmapped" or "missing" mappings. The goal is to assess data quality, find gaps in the model's knowledge of diagnosis codes, and quantify how prevalent these unmapped codes are in the patient population.

For example, if the model is trained on ICD-9 and ICD-10 codes, but the input data contains diagnosis codes in free text or a different standard, this test will flag them. It then analyzes how common these unmapped codes are, especially in patients who receive high scores from the model, to help prioritize which codes should be manually mapped.

## Required Inputs

From `configs/env.sh` and the test invocation environment:

- `WORK_DIR`: The main working directory for test inputs and outputs.
- `DIAG_PREFIX`: An environment variable containing a regular expression to identify the target diagnosis codes to be analyzed (e.g., `ICD9_CODE:|ICD10_CODE:`). The test will fail if this is not set.
- Optional: `OTHER_DIAG_PREFIX`: An environment variable with a comma-separated list of specific prefixes (e.g., `ICD9_CODE,ICD10_CODE`). If set, the test will generate separate prevalence reports for each code system.

The test also depends on artifacts from previous tests:
- `${WORK_DIR}/rep/test.repository` and `${WORK_DIR}/rep/test.signals` (from Test 01 - Generate Repository)
- `${WORK_DIR}/predictions/all.preds` (or an equivalent samples file with predictions, from Test 06 - Compare Score Distribution)

## How to Run
```bash
./run.specific.sh 19
```
Or run with the full suite:
```bash
./run.sh
```

## What This Test Does

If checks for catgorical values that don't match our regex prefix. For example diagnosis codes that are not ICD10_CODE and not ICD9_CODE.
For each of those code, if there is no mapping to ICD10/ICD9 codes in the hierarchy, we will collect this code as unmapped into file `${WORK_DIR}/unmapped_diagnosis/missing_from_dictionaries.csv`.

We will inspect most common unmapped codes into file `${WORK_DIR}/unmapped_diagnosis/missing.ALL.txt`
It will take top 10% highest scores and will check all of those codes that happened before our samples prediction date (to see how it might effect the model).
It will compare most common codes in top 10% Vs the rest of the scores, to see if there is a pattern that might impact the model and worth mapping.

## Output Location

* `${WORK_DIR}/unmapped_diagnosis/missing.ALL.txt` - summary of most common missing codes, how they are related to cases/controls 

## How to Interpret Results

Explore the results file and see if there are unmapped codes that are related to the prediction or important codes that should be used by the model under certains ICD10/ICD9 codes that the model uses.
BTW, this can also work for Drugs, or other categorical signals.

