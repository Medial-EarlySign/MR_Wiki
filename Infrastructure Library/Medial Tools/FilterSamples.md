# FilterSamples

## Overview
This simple application helps you filter your MedSamples based on bootstrap query language criteria or by simple criteria based on `TRAIN` signal.

## How to use

Example run:

```bash
FilterSamples --rep $REPOSITORY_PATH --samples $INPUT_SAMPLES_PATH --output $OUTPUT_SAMPLES_PATH --filter_train $FILTER_TRAIN_VAL
```

- `TRAIN == 1`: Training set (70%)
- `TRAIN == 2`: Test set (20%)
- `TRAIN == 3`: Validation set (10%)

You can also specify `--json_mat` and `--filter_by_bt_cohort` to filter by bootstrap query language.
More info on bootstrap query language in here: [](../../Infrastructure%20Library/MedProcessTools%20Library/MedBootstrap.md#cohorts-file-format)