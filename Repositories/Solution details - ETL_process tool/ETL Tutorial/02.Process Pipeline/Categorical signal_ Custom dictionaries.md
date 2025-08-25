# Categorical Signals & Custom Dictionaries

This page explains how categorical signals are handled in the ETL process, with examples of when to use **known ontologies**, how to deal with **client-provided values**, and how to integrate **custom mapping dictionaries**.

## Use Case 1 – Known Signals with Standard Ontologies

When using a known categorical signal from [ETL_INFRA_DIR](../../High%20level%20-%20important%20paths/ETL_INFRA_DIR.md)/rep_signals/general.signals (e.g., **DIAGNOSIS**, **Drug**, **PROCEDURE**), the ETL automatically applies existing **ontologies** and **mappings** between codes.

### Example:
For the Drug signal, if you create values with the `RX_CODE` prefix, the ETL will detect this and automatically pull:

* The `RX_CODE` dictionary,
* The `ATC` dictionary, and
* The mapping between `RX_CODE` and `ATC`.

You only need to set the correct prefixes in `prepare_final_signals` processings.
The call to `finish_prepare_load` takes care of the rest. No need to do anything special.

### Known Ontologies and Prefixes

|Coding system prefix | description|
|---------------------------------|------------------| 
|ICD10_CODE:| Diagnosis or procedure with ICD10 codes. For PROCEDURE signal, uses procedure ontology |
|ICD9_CODE| Diagnosis or procedure with ICD9 codes. For PROCEDURE signal, uses procedure ontology |
| ATC_CODE: | Medication prescriptions in ATC codes |
| RX_CODE: | Medications prescriptions in RX norm|
| NDC_CODE:| Medications in NDC codes|

## Use Case 2 – New Signals from Client (List of Values)

Sometimes we receive a signal that is not part of a known ontology and comes only as a list of values from the client.

### Example:
A signal like Cancer_Type with values such as:

* `Adenocarcinoma`
* `Small_Cells`
* etc. (extracted from cancer patients)

### What to do:

* Define the new categorical signal in [CODE_DIR](../../High%20level%20-%20important%20paths/CODE_DIR.md)/configs/rep.signals
➡️ No manual mapping is needed. It will processed in the end as part of `finish_prepare_load` call later

## Use Case 3 – New or Known Signals with Additional Client Dictionaries

Sometimes the signal is known (e.g., **DIAGNOSIS**) or new, but the client provides extra **mapping dictionaries**.

### Example:
The client uses an internal coding system (`EDG_CODE`) and provides:

1. **Translation dictionary** - maps internal codes to descriptions.
    - Example: ``EDG_CODE:1234` → _Diabetes type II_
2. **Mapping dictionary** - maps internal codes to another known ontology.
    - Example: `EDG_CODE:1234` (Diabetes type II) → `ICD10_CODE:E11`

### Notes:

* Sometimes only **#1 (translation)** is available → still valid.
* Sometimes only **#2 (mapping)** is available → also valid.
* If the ontology is **common and reusable**, we may store the mapping dictionary in ETL for future use. We will need to change the code in `create_dicts.py`, currently it is not very easily extended.

### How to use

Use the function `prepare_dicts` with up to two optional dataframes:

* **Translation dictionary:**

| Column | Meaning |
| ------ | ------- |
| `code` | Internal code |
| `description` | Human-readable description |

* **Mapping dictionary:**

| Column | Meaning |
| ------ | ------- |
| `client_value` | Value from client |
| `ontology_code` | Code from our known ontology |
 

## How-To: Reading the Output of prepare_dicts / finish_prepare_load

During processing, the ETL produces log messages with **statistics** about how the dictionaries were handled.

### What to Expect

* **Known codes detected** - how many values already exist in our mappings.
* **New codes detected** - how many values were introduced for the first time (e.g., new ICD10 codes for new diseases).
* **Automatic mapping attempts** - in some cases, new codes are mapped by truncating strings to a higher-level category (e.g., grouping a specific disease into a broader disease family).
 
### Why It Matters

* Helps identify if client data aligns well with existing ontologies.
* Flags new codes that may need review or long-term integration.
* Provides confidence that signal values were normalized as expected.
 
