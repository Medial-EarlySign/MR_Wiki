# High-Level Overview of the ETL Process

This document outlines the high-level structure and flow of the ETL (Extract, Transform, Load) process. It covers the core file structure and the sequential steps involved in loading data.

---

## 📁 ETL File Structure

The ETL process uses three main directories:

* **[ETL_INFRA_DIR](ETL_INFRA_DIR.md)**: This directory, located at [MR_TOOLS](https://github.com/Medial-EarlySign/MR_Tools) git repo `RepoLoadUtils\common\ETL_Infra`, contains the standalone ETL infrastructure. It's portable and doesn't require other files to function.
* **[CODE_DIR](CODE_DIR.md)**: This is where you write the code specific to your ETL task.
* **[WORK_DIR](WORK_DIR.md)**: This directory serves as the output location for the ETL process.

For more details on the contents of each directory, click the links above.

---

## ⚙️ The ETL Process Flow

The ETL process is managed by a `load.py` script located in the **CODE_DIR**. This script orchestrates the loading process by calling the `prepare_final_signals` function, which in turn initiates a "parser" for each signal. `load.py` is a convention name, it is not necessarily needs to be like that.

### Step 1: Handling Signals

1.  **Status Check**: The `prepare_final_signals` function first checks the status of the required signal.
    * If `override` is specified, the signal is loaded from the start.
    * If the signal is already loaded, it's skipped.
    * Otherwise, it resumes loading from the last interrupted batch or starts from the beginning.
2.  **PID Validation**: The `pid` column is mandatory in the parser's output.
    * If `pid` column is missing, the process will **ERROR** and **STOP**.
    * If `pid` is a string, it's mapped to a numeric value. **This mapping is only performed for demographic signals (e.g., BDATE, GENDER)**. A `pid` in another signal (e.g., DIAGNOSIS) that hasn't been seen in a demographic signal will be excluded. Therefore, **demographic signals must be processed first** with `prepare_final_signals`.
3.  **Preliminary Check**: Before processing, the system checks if the signal data is already complete and valid.
    * If the dataframe contains all necessary columns and attributes as defined in `rep_signals/general.signals` and passes all preliminary tests, no further processing is needed. The data is sorted, and the signal processing is marked as complete.
    * Otherwise, the process continues to the next step.

### Step 2: Determining the Processing Unit

The system identifies the appropriate "processing unit" based on the data.

1.  **When `signal` column exists**:
    * The most specific code is executed based on the signal name and its classifications. For example, for the "BDATE" signal (classified as "demographic" and "singleton"), the system would search for `BDATE.py`, then `demographic.py`.
    * The signals configuration file and their classifications is located in the `general.signals` file in [ETL_INFRA_DIR](ETL_INFRA_DIR.md) or in "configs/rep.signals" added to [CODE_DIR](CODE_DIR.md).
2.  **Without a `signal` column**:
    * The `prepare_final_signals` function's parameter is used to determine the signal. This also allows for multiple signals to be passed (e.g., "BDATE,GENDER"), and the most specific code is found for each.

If no relevant processing unit is found, a new one is created with instructions. In interactive mode, a Python environment opens for real-time processing and inspection. In non-interactive mode, the process fails, waiting for the unit's code to be filled in.

---

### Step 3: Testing and Finalizing the Signal

1.  **Post-Processing Tests**: After the processing unit returns the signal file, two types of tests are performed:
    * **General Tests**: These check for valid time/value channels, numeric values, valid dates, and illegal characters.
    * **Specific Tests**: These are associated with the signal name and its classifications, such as comparing signal distribution or counting outliers. These tests can be added globally in **ETL_INFRA_DIR** or locally in **CODE_DIR**.
2.  **Post-Test Actions**: Once the signal passes all tests:
    * Columns are sorted and organized.
    * Statistics for categorical signals are collected to aid in dictionary creation.
    * The batch or signal state is updated to reflect successful completion.

### Step 4: Dictionaries and Final Load

1.  **Dictionary Creation**: If your data requires specific dictionaries, you can call the `prepare_dicts` function.
    * For categorical features like "Drug", "PROCEDURES", and "DIAGNOSIS" that have specific prefixes (e.g., `ICD10_CODE:*`), the system can automatically recognize and use the correct ontology.
    * Statistics from these steps are collected for the final report.
2.  **Finalization**: The final step is to call `finish_prepare_load`. This function:
    * Processes all categorical signal dictionaries.
    * Generates a merged "signals" file.
    * Creates a `convert_config` file.
    * Prepares the `Flow` command to execute the loading process.