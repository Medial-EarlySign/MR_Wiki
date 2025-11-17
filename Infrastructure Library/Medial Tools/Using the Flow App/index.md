# Using the Flow App

## Overview

The Flow App is a versatile tool with multiple switches, each designed to perform a specific action. Below are its key functionalities:

- [Load New Repository](../../../Infrastructure%20Library/DataRepository/Load%20new%20repository.md): Converts raw ETL output files into an efficient, binary, and indexed format compatible with the AlgoMedical library framework.
- [Train](#training-a-model) a model.
- [Apply](#predictingapplying-a-model) a model to generate predictions.
- Extract [feature matrices](#creating-a-feature-matrix-for-samples) from the model pipeline.
- [Print](#printing-pids-and-signals) specific patient data or signal distributions.
- [Feature Importance with Shapley Values Analysis](../../05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md).
- [Prepare Samples and Get Incidences Using Flow](Using%20Flow%20To%20Prepare%20Samples%20and%20Get%20Incidences.md).
- [Fit MedModel to Repository](Fit%20MedModel%20to%20Repository.md): Adjusts an existing model to fit a new repository. For instance, if a non-critical signal is missing, the "fit" operation generates a virtual empty signal to bypass errors, ensuring compatibility. The suggested changes can later be reviewed and validated or corrected. More information inside

GitHub Repository: [Flow App Code](https://github.com/Medial-EarlySign/MR_Tools/tree/main/Flow)

The Flow App is also compiled as part of AllTools. Refer to the [Setup Instructions](../../../Installation/index.md#3-mes-tools-to-train-and-test-models).

## Flow App Options

### General Switches

- `--help`: Displays the full help menu.
- `--help_`: Searches the help menu and displays only the relevant sections matching the search term.
- `--rep`: Specifies the path to the repository.

### Creating Repositories

To create a repository using a convert configuration file, use the `--convert_conf` option:

```bash
Flow --rep_create --convert_conf ./ICU.convert_config
```

To create a by-pid transposed version of a repository, use the following command. This allows faster access to specific patient IDs (pids) and reduces memory consumption significantly:

```bash
Flow --rep_create_pids --rep ./ICU.repository
```

For more details on creating repositories, convert configuration files, and required inputs, refer to [Load a New Repository](../../../Infrastructure%20Library/DataRepository/Load%20new%20repository.md).

### Printing PIDs and Signals

- Print all records for all signals for a specific pid using the default API:

```bash
Flow --rep ./ICU.repository --printall --pid 200001
```

- Print all records for all signals for a specific pid using the by-pid API (faster but requires a by-pid repository):

```bash
Flow --rep ./ICU.repository --pid_printall --pid 200001
```

- Print all records for a specific signal and pid using the default API:

```bash
Flow --rep ./ICU.repository --print --pid 200001 --sig Sepsis
```

- Print all records for a specific signal and pid using the by-pid API (faster but requires a by-pid repository):

```bash
Flow --rep ./ICU.repository --pid_print --pid 200001 --sig Sepsis
```

- Print general statistics for a signal, such as sample counts, gender distribution, average samples per person, and more. This works only for `SDateVal` type signals and repositories containing `GENDER` and `BYEAR` signals:

```bash
Flow --rep ./thin.repository --describe --sig Creatinine
```

### Training a Model

To train a model, you need the following inputs:

- `REPOSITORY_PATH`: Path to the data repository.
- `PATH_TO_TRAIN_SAMPLES`: Path to [MedSamples](../../../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md), a TSV file defining labels for each patient and point in time.
- `PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS`: Path to the JSON file defining the model architecture. See [Model JSON Format](../../../Infrastructure%20Library/MedModel%20json%20format.md).
- `PATH_TO_OUTPUT_TO_STORE_MODEL`: Path to save the trained model.

Example command:

```bash
Flow --simple_train --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_model $PATH_TO_OUTPUT_TO_STORE_MODEL
```

For cross-validation, use the `--train_test` mode switch. However, this is deprecated.
Use the [Optimizer](../Optimizer.md) instead.

### Predicting/Applying a Model

To apply a model, you need the following inputs:

- `REPOSITORY_PATH`: Path to the data repository.
- `PATH_TO_TRAIN_SAMPLES`: Path to [MedSamples](../../../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md), defining requested prediction times for each patient. The outcome column is not used during testing.
- `PATH_TO_TRAINED_MODEL_BINARY_FILE`: Path to the stored model.
- `OUTPUT_PATH_TO_STORE_SAMPLES`: Path to save the predictions. The output will include a `pred_0` column in the MedSamples file for each requested prediction date.

Example command:

```bash
Flow --get_model_preds --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_preds $OUTPUT_PATH_TO_STORE_SAMPLES
```

**Pre-processors** can be added to the beginning of the model pipeline to manipulate raw signals before they are fed into the model. This allows you to perform operations that don't require training or storage in the model itself, such as simulating the removal or limitation of a specific signal. For more details, see [Using Pre Processors](Using%20Pre%20Processors.md)

### Creating a Feature Matrix for Samples

To create a feature matrix, use the same inputs as for predicting/applying a model. The output will be a CSV file containing the feature matrix:

```bash
Flow --get_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_model $PATH_TO_TRAINED_MODEL_BINARY_FILE --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
```

To inspect the training matrix directly from the model JSON, use the following command. The inputs are the same as for model training, but the output is a matrix instead of a model:

```bash
Flow --get_json_mat --rep $REPOSITORY_PATH --f_samples $PATH_TO_TRAIN_SAMPLES --f_json $PATH_TO_JSON_WITH_MODEL_INSTRUCTIONS --f_matrix $OUTPUT_PATH_TO_STORE_MATRIX
```
#### How to Generate a Matrix Without Imputations
To create a matrix that skips imputations and normalizations, add the `--stop_step 2` argument to your `--get_mat` command.

This setting halts the pipeline after the feature generation step, skipping the "feature processors" that would normally handle imputation and normalization. In the resulting matrix, missing data will be marked with the value `-65536`.

### Print trained model information

To inspect model pipeline:

```bash
Flow --print_model_info --f_model $MODEL 
```
You can add `--print_json_format 1 --f_output $OUTPUT_JSON` and set `OUTPUT_JSON` to output path with a more detailed information about the model. It is not exactly a json format, but this is textual.