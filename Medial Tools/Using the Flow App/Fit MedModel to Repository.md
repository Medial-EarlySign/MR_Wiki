# Fitting a MedModel to a Repository

The Flow app provides an option called `fit_model_to_rep`. You can use it as follows:

```bash
Flow --fit_model_to_rep [other arguments]
# See all arguments with: Flow --help_ fit_model_to_rep
```

## Overview

The purpose of this tool is to take a repository path and a model path as input, and output a new, adjusted model that fits the repository at a specified output path.

## Key Considerations

1. Signal names may change over time (e.g., GENDER ↔ SEX, DIAGNOSIS ↔ ICD9_Diagnosis, RC). These changes can cause compatibility issues.
2. Sometimes, models require signals that do not exist in the repository. Rather than treating missing signals as empty (which can be misleading), MedModel enforces strict checks to avoid confusion.
3. This tool outputs list of "suggested" changes in the model for your review and creates the new adjusted model.

## Workflow

1. The tool reads both the model and the repository, checking for required signals that are missing from the repository.
2. For each missing signal, it attempts to resolve the issue by adding or removing a `rep_processor` in the model, following a set priority. It starts by search an alternative signal name (for example, if SEX signal is missing and we have GENDER it will use GENDER as SEX, otherwise it will create an emoty signal to mark this signal as missing).
3. It validates all categorical codes used by the model to ensure they are present in the repository.
4. The adjusted model is saved to the specified output file.
5. A log of all transformations made to the model is printed to a file or the screen.
6. A log of any missing codes for each signal is also printed to a file or the screen.
7. If all codes are present and all adjustments are successful, the process completes without errors.

## Example Usage

```bash
Flow --fit_model_to_rep \
  --f_model /nas1/Work/Users/Eitan/Lung/outputs/models2023/EX3/model_63/config_params/exported_full_model.final.medmdl \
  --rep /nas1/Work/CancerData/Repositories/THIN/thin_2021.lung2/thin.repository \
  --f_output /tmp/1.mdl \
  --log_action_file_path /tmp/actions.log \
  --log_missing_categories_path /tmp/categ.log \
  --cleaner_verbose -1 \
  --allow_virtual_rep 0
```

### Argument Descriptions

- `log_action_file_path`: Logs all changes made to the model. If not provided, output is printed to the screen.
- `log_missing_categories_path`: Logs all missing codes for signals. If not provided, output is printed to the screen.
- `cleaner_verbose`: Controls verbosity of outlier reporting. Use `1` for production (verbose), `-1` for validation (no verbose, faster).
- `allow_virtual_rep`: Allows use only a repository definition without data (like we have in AlgoMAkrer) for testing model fitting. Some adjustments may be limited, because we don't use actual data.

## Sample Output

```
Signal BUN, median value is 34.200001 in repository
write_to_file [/tmp/1.mdl] with crc32 [273944850]
read_binary_data_alloc [/tmp/1.mdl] with crc32 [273944850]
read_from_file [/tmp/1.mdl] with crc32 [273944850] and size [193041186]
categorical signal ICD9_Diagnosis is OK
categorical signal Smoking_Status is OK
All categorical signals are OK!
All OK - Model can be applied on repository
```

In this example, the model uses Urea, but the repository has BUN. The tool finds the median value of BUN, writes the adjusted model, and verifies it. The output confirms that all categorical signals are valid and the model can be applied.

If all codes exist, the `/tmp/categ.log` file will be empty. If codes are missing, the file will list the signal name and missing categorical value (tab-delimited).

### Example Action Log

```text
REMOVED_RENAME_FROM_TO  SEX     GENDER
CONVERT_SIGNAL_TO_FROM_FACTOR   Urea    BUN     0.467290
EMPTY_SIGNAL    RDW
```

- The first line indicates that the model used "SEX", but the repository has "GENDER". The processor converting GENDER to SEX was removed, so the model now accepts GENDER input signal.
- The second line shows that a virtual signal "Urea" was created from "BUN" by multiplying by 0.467290.
- The third line indicates that "RDW" was missing from the repository, so an empty virtual signal was

This is valid transformation of some breaking changes we had in our signals/repositories during the years + empty RDW signal which is acceptable in that case.