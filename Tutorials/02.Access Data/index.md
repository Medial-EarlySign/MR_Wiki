# Accessing Repository Data

This guide explains two methods for accessing data from the repository: using the Python API for programmatic access or using MES Tools for a user-interface-based approach.

## Method 1: Using the Python API

This method is ideal for programmatic data access and analysis within a Python environment.

### Prerequisites

Before you begin, ensure you have:

1.  Installed the [Python API for MES Infrastructure](../../Installation/Python%20API%20for%20MES%20Infrastructure.md).
2.  Loaded a Data Repository by following the [ETL Tutorial](../01.ETL%20Tutorial/index.md).

### Basic Data Retrieval

To get started, import the `med` library and initialize the `PidRepository` with the path to your loaded repository file.

```python
import med

# Initialize the repository
rep = med.PidRepository()
rep.init('/path/to/your/repository_file')

# Retrieve a signal, for example, 'Albumin'
albumin = rep.get_sig('Albumin')

# 'albumin' is now a pandas DataFrame containing patient IDs ('pid'), 
# time channels ('timeX'), and value channels ('valX').
```

### Filtering by Patients and Signals

You can optimize data loading by initializing the repository with a specific list of patient IDs and signals. This is particularly useful for large datasets.

```python
list_of_patient_ids = [101, 102, 103] # Example patient IDs
list_of_signals = ['Albumin', 'DIAGNOSIS']

# Read data only for specified patients and signals
rep.read_all('/path/to/your/repository_file', list_of_patient_ids, list_of_signals)

# Subsequent calls to get_sig will now only return data for the filtered patients.
# If list_of_patient_ids is empty, it will query all patients in the repository.
```

### Working with Categorical Signals

Categorical signals, like 'DIAGNOSIS', can be handled in two ways.

#### 1. Translated (String) Values

By default, `get_sig` returns a DataFrame with human-readable string values. While convenient, this can be memory-intensive.

```python
# This can consume a lot of memory for large datasets
diagnosis_strings = rep.get_sig('DIAGNOSIS') 
```

#### 2. Untranslated (Numeric) Codes

For more efficient memory usage and advanced querying, you can retrieve the raw numeric codes for each category.

```python
# Set translate=False to get numeric codes instead of strings
diagnosis_codes = rep.get_sig('DIAGNOSIS', translate=False)
```

This returns a DataFrame with integer codes, which is more memory-efficient but requires an extra step for querying based on categories.

### Efficiently Querying Categorical Data

To efficiently query categorical signals by their meaning (e.g., finding all diagnoses related to a specific disease group), use **lookup tables (LUTs)**.

A lookup table is an array where each index corresponds to a numeric category code. By marking relevant indices, you can perform very fast filtering.

**Example: Filtering for Respiratory Diseases**

Let's filter the 'DIAGNOSIS' signal for all codes corresponding to respiratory diseases, defined by the ICD-10 range `J00-J99`.

**Step 1: Create a Lookup Table**

First, get the dictionary section for the 'DIAGNOSIS' signal. Then, create a lookup table for the desired code range.

```python
# Get the dictionary section ID for the 'DIAGNOSIS' signal
sig_dict_section_id = rep.dict.section_id('DIAGNOSIS')

# Create a lookup table for the ICD-10 range 'J00-J99'
lut = rep.dict.prep_sets_lookup_table(sig_dict_section_id, ["ICD10_CODE:J00-J99"])
```

The `lut` now contains `1` at indices corresponding to the `J00-J99` codes and `0` otherwise. This mapping can handle complex relationships, such as mapping NDC drug codes to ATC codes, not just simple string matching.

> [!NOTE]
> You can pass multiple values to `prep_sets_lookup_table`, it acceptes a list of codes to create a single lookup table with OR condition between all codes.


**Step 2: Apply the Lookup Table**

Now, use the lookup table to filter your DataFrame of diagnosis codes.

```python
# diagnosis_codes is the DataFrame from the get_sig('DIAGNOSIS', translate=False) call
filtered_diagnosis = diagnosis_codes[lut[diagnosis_codes["val0"]] != 0]
```

`filtered_diagnosis` now contains only the diagnosis records that fall within the `J00-J99` range.

## Method 2: Using MES Tools and UI

If you prefer command line or a graphical interface, you can use the MES Tools.

### Prerequisites

First, complete the [MES Tools Setup](../../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md).

### Examples

*   **View or Export Data with `Flow`**: See the guide on [how to use Flow to view signals and export data](../../Infrastructure%20Library/Medial%20Tools/Using%20the%20Flow%20App/index.md#printing-pids-and-signals).
*   **Inspect a Single Patient**: Use the [Repository Viewers UI](../../Infrastructure%20Library/DataRepository/Repository%20Viewers.md) to open and explore the data for a single patient.
