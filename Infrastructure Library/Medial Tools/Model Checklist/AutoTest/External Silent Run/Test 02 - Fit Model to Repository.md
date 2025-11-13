# Test 02 - Fit Model to Repository

## Purpose

Take an existing Medial model file and fit (transform) it so it can be applied to a generated repository. This step produces one or more transformed models ready for inference and further validation.

## Required Inputs
From `configs/env.sh` and test invocation environment:

- `WORK_DIR`: Working output folder where repository and model outputs are written
- `MODEL_PATH`: Path to the input Medial model file to be fitted to the repository
- Optional: `CALIBRATED_MODEL_PATH`: Path to an alternative calibrated model to also fit (optional)

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 2
```
Or include as part of the full suite:
```bash
./run.sh
```

Check `${WORK_DIR}/model` for produced model files and logs.

## What This Test Does

This test performs the following high-level actions:

- Locates the generated repository under `${WORK_DIR}/rep` (looks for the `.repository` file)
- Creates `${WORK_DIR}/model` and writes transformed model(s) there
- Runs the transformation command `Flow --fit_model_to_rep` (more info on [fit_model_to_rep](../../../Using%20the%20Flow%20App/Fit%20MedModel%20to%20Repository.md)) to:
    - produce a cleaned model without explainability at `${WORK_DIR}/model/model.medmdl`
    - produce a cleaned version that retains explainability at `model.with_explainability.medmdl`
    - optionally fit a calibrated model if `CALIBRATED_MODEL_PATH` is provided
- Writes action logs and missing-category logs in `${WORK_DIR}/model`
- Performs simple post-checks to detect missing categories and to verify that the conversion completed successfully by searching the test log for the string "All OK - Model can be applied on repository".

## Output Location

- Transformed model (without explainability): `${WORK_DIR}/model/model.medmdl`
- Transformed model (with explainability): `${WORK_DIR}/model/model.with_explainability.medmdl`
- Calibrated transformed model (if provided): `${WORK_DIR}/model/model.calibrated.medmdl`
- Action logs: `${WORK_DIR}/model/actions.log` and `actions.with_explanability.log` (and `.calibrated.log` if applicable)
- Missing categories logs: `${WORK_DIR}/model/missing_categ.log` (and `.with_explanability` / `.calibrated` variants)

## How to Interpret Results

The script performs basic validation and emits logs. Review the following to ensure the model was fitted correctly:

- Missing categories:
  * Check `${WORK_DIR}/model/missing_categ.log`. Any lines containing `MISSING_CODE_VALUE` indicate categories referenced by the model but absent from the repository. The test prints a failure message with the number of missing categories if any are found.
- Conversion actions and errors:
  * Review `${WORK_DIR}/model/actions.log` and `${WORK_DIR}/${TEST_NAME}.log` for details of transformations and any warnings or errors.
- Final success marker:
  * The script looks for the exact text `All OK - Model can be applied on repository` in `${WORK_DIR}/${TEST_NAME}.log`. If not found, the test exits with code 2 and prints a message pointing to logs above.

### Common failure modes and suggestions

- Missing categories (MISSING_CODE_VALUE):
    * This typically means the model expects categorical values not present in the repository. Check data preprocessing and mapping configuration; consider adding mappings or ensuring training categories exist in the input data.
- Conversion actions in `actions.log`:
    * Inspect `actions.log` to see what transformations were applied and whether any replacements, drops, or heuristic fixes were used.

## Example output snippets

1) When missing categories are detected, the script will print:

```text
Failed has N missing categories - please refer to ${WORK_DIR}/model/missing_categ.log
```

## Notes and Implementation Details

- The script calls `Flow --fit_model_to_rep` multiple times with different flags to produce model variants. The important flags visible in the script are `--cleaner_verbose -1`, `--remove_explainability` (0/1), and log path flags.
- The test expects the environment to provide `WORK_DIR`, `MODEL_PATH`, and optionally `CALIBRATED_MODEL_PATH`.

## Troubleshooting

- If `Flow` is not found on your PATH, ensure the Medial runtime and tools are installed and available in the environment used by the TestKit. You can also modify PATH in `configs/env.sh`.

## Test Results Review

Primary logs to review after running this test:

- `${WORK_DIR}/model/actions.log`
- `${WORK_DIR}/model/missing_categ.log`
- `${WORK_DIR}/${TEST_NAME}.log`

