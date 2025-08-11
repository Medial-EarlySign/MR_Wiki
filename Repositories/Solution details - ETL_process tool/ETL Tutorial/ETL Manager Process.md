# ETL Manager Process

This guide explains how to use the ETL manager to prepare, test, and load your processed signals into the repository. You’ll learn how to:

- Prepare final signals for each data type
- Handle special client dictionaries (if needed)
- Complete the preparation and load data into the repository

---

## Overview

The ETL manager process consists of three main API calls:

1. `prepare_final_signals` — Process and test each data type
2. `prepare_dicts` — (Optional) Create custom dictionaries for categorical signals
3. `finish_prepare_load` — Finalize and load data into the repository

<img src="/attachments/13402629/14811579.png"/>

---

## Step-by-Step Guide

### 1. Environment Setup & Imports

Start by importing the required modules and your data fetchers.

```python
import sys
import os
import pandas as pd
from ETL_Infra.etl_process import *
import thin_ahd_data_fetcher, thin_patient_data_fetcher  # Your custom fetchers
```

---

### 2. Prepare Final Signals

Use `prepare_final_signals` for each data type. This function processes, tests, and (optionally) batches your data.

```python
WORK_DIR = '/nas1/Work/Users/Alon/ETL/demo_thin'
batch_size = 1  # Process files one by one
sig_name_or_group_name = 'demographic'

# Prepare signals for each data type
prepare_final_signals(thin_patient_data_fetcher, WORK_DIR, sig_name_or_group_name, batch_size, override='n')
prepare_final_signals(thin_ahd_data_fetcher, WORK_DIR, 'labs', batch_size, override='n')
# Add more data types as needed
```

---

### 3. (Optional) Prepare Special Client Dictionaries

If your project requires custom mapping dictionaries for categorical signals, use `prepare_dicts`.

```python
# Example definition dictionary DataFrame
def_dict = pd.DataFrame({
    'internal_client_code': ['A123', 'B456'],
    'description': ['Description A', 'Description B']
})

# Example set dictionary DataFrame
set_dict = pd.DataFrame({
    'parent': ['ICD10_1', 'ICD10_2'],
    'child': ['A123', 'B456']
})

# Prepare dictionaries for the 'DIAGNOSIS' signal
prepare_dicts(WORK_DIR, 'DIAGNOSIS', def_dict, set_dict)
```

> **Tip:**  
> For more on categorical signals and custom dictionaries, see:  
> [Categorical signal/ Custom dictionaries](Categorical%20signal_%20Custom%20dictionaries.md)

---

### 4. Finish Preparation and Load

Finalize the process and load your data into the repository with `finish_prepare_load`.

```python
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```

---

## Full Example

Here’s a complete example combining all steps:

```python
import sys
import os
import pandas as pd
from ETL_Infra.etl_process import *
from examples.thin_example.thin_parser import thin_ahd_data_fetcher, thin_patient_data_fetcher

WORK_DIR = '/nas1/Work/Users/Alon/ETL/demo_thin'
batch_size = 1

# Prepare signals
prepare_final_signals(thin_patient_data_fetcher, WORK_DIR, 'demographic', batch_size, override='n')
prepare_final_signals(thin_ahd_data_fetcher, WORK_DIR, 'labs', batch_size, override='n')

# Optional: Prepare custom dictionaries
def_dict = pd.DataFrame({
    'internal_client_code': ['A123', 'B456'],
    'description': ['Description A', 'Description B']
})
set_dict = pd.DataFrame({
    'parent': ['ICD10_1', 'ICD10_2'],
    'child': ['A123', 'B456']
})
prepare_dicts(WORK_DIR, 'RC', def_dict, set_dict)

# Finish and load
finish_prepare_load(WORK_DIR, '/nas1/Work/CancerData/THIN/thin_20XX', 'thin')
```

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

For more details, see the [old documentation](#) below or reach out for help.

