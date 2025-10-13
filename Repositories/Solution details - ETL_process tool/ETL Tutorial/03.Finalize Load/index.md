# Finalizing the Load Process

This step **completes the ETL pipeline** and prepares the repository for use.

## Recap of earlier steps
* **Prepare signals**: Run `prepare_final_signals` for each data type (see [previous step](../02.Process%20Pipeline))
* **Handle client dictionaries (if needed)**: Use `prepare_dicts` for [categorical signals](../02.Process%20Pipeline/Categorical%20signal_%20Custom%20dictionaries.md)


Now we will **finalize the preparation** and generate all configuration files needed for loading by using a third function: `finish_prepare_load`.

---

## `finish_prepare_load`

Finalizes preparation and loads your data into the repository.

```python
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```

**Parameters:**

* `WORK_DIR` - path to the working directory (string)
* `REPOSITORY_OUTPUT_DIR` - destination folder for the repository (string)
* `REPO_NAME` - name of the repository (string)

---

## Full Workflow Example

Here’s a complete example combining all steps:

```python
import pandas as pd
from ETL_Infra.etl_process import *
from parser import generic_file_fetcher, generic_big_files_fetcher

WORK_DIR = '/nas1/Work/demo_ETL'

# Step 1: Prepare signals
prepare_final_signals(
    generic_file_fetcher("^demo.*"),  # Fetch files starting with "demo"
    WORK_DIR,
    "demographic",  # Name of this processing pipeline
    batch_size=0,   # Process all files in a single batch
    override="n"    # Skip if already successfully completed
)
prepare_final_signals(
    generic_big_files_fetcher("^labs.*"),  # Fetch files starting with "labs"
    WORK_DIR,
    "labs",  
    batch_size=1e6,   # Process each 1M lines in a single batch
    override="n"    
)

# Step 2 (optional): Handle custom dictionaries
# Provide client dicts as DataFrames: def_dict, set_dict (or None)
prepare_dicts(WORK_DIR, 'DIAGNOSIS', def_dict, set_dict)

# Step 3: Finalize and load
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```

## Final Script to Create the Data Repository
Look for a message on your screen similar to the last two lines below, which provide the full path to the script that runs `Flow` and generates the repository:

```text
Full script to execute :
.../rep_configs/load_with_flow.sh
```
This script is located at `WORK_DIR`/rep_configs/load_with_flow.sh. Run this script and confirm that it completes successfully with a success message at the end.

---

## Function Reference

**1. `prepare_final_signals`**  
Processes and tests each data type. Handles batching if needed.

- **Arguments:**
  - `data_fetcher` or `DataFrame`: Source of your data
  - `workdir`: Working directory for outputs
  - `signal_type`: Name/type of the signal (used for classification)
  - `batch_size`: Batch size (0 = no batching)
  - `override`: `'y'` to overwrite, `'n'` to skip completed signals

**2. `prepare_dicts`**  
Creates mapping dictionaries for categorical signals.

- **Arguments:**
  - `workdir`: Working directory
  - `signal`: Signal name
  - `def_dict`: DataFrame with internal codes and descriptions (optional)
  - `set_dict`: DataFrame mapping client codes to known ontology

**3. `finish_prepare_load`**  
Finalizes preparation, generates signals, and loads the repository.

- **Arguments:**
  - `workdir`: Working directory
  - `dest_folder`: Destination for the repository
  - `dest_rep`: Repository name (prefix)
  - `to_remove` (optional): List of signals to skip
  - `load_only` (optional): List of signals to load only

---

### Extending and Testing

For guidance on extending the process and adding automated tests, see [Test Extention](../ETL_process%20dynamic%20testing%20of%20signals.md)

## Validating The ETL Outputs and Tests

Follow [this guide](../04.Read%20Results/)