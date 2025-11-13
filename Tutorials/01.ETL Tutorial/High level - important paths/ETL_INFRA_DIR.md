# 📂 ETL_INFRA_DIR: A Closer Look

The `ETL_INFRA_DIR` contains the standalone ETL infrastructure, available in the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository under `RepoLoadUtils/common/ETL_Infra`. It's designed to be portable and can be used on a remote machine without external dependencies.

---

### Core Files and Folders

-   **`etl_process.py`**: The main Python module to import into your specific ETL code.
-   **`dicts`**: Stores dictionaries for known medical ontologies and their mappings. This is a resource for the infrastructure; **only edit this folder to update global dictionaries for all future work**.
-   **`examples`**: Provides sample loading processes for various repositories. The `THIN` example is fully implemented.
-   **`rep_signals`**: Contains global definitions for standard signals. These definitions can be overridden in your local ETL code but should generally remain as is. **Only edit this folder to update signal definitions for all future work**.
    -   **`general.signals`**: A file with definitions for all known signals, including type, unit, categorical status, and **"tags"**. Tags are crucial as they determine the processing logic and tests to be executed. The File Format: [Repository Signals file format](../../../Infrastructure%20Library/DataRepository/Repository%20Signals%20file%20format.md)
        -   For example, a signal tagged as "labs" and "cbc" will first look for `Hemoglobin.py`, then `labs.py`, then `cbc.py` for processing logic.
        -   All tests associated with `hemoglobin`, `labs`, and `cbc` will be executed.
    -   **`signals_prctile.cfg`**: Contains quantile information for each signal listed in `general.signals`. This data is used to test lab signals.
    -   **`lab_zero_value_allowed.txt`**: A list of signals where a value of `0` is permitted. An error will be raised if a zero value is found for a signal not on this list and the rate is above a defined threshold.
-   **`tests`**: Holds additional, specific tests for signals. The ETL process always performs basic structural checks (e.g., correct channels, data types).
    -   **`TAG_NAME`** (e.g., "labs"): Each file within this folder represents a different test that will be executed for every signal with that specific tag. To add additional tests see [ETL_process dynamic testing of signals](../ETL_process%20dynamic%20testing%20of%20signals.md)
-   **`data_fetcher`**: A library with helper functions for the parsing phase, which fetches data from databases or files. For example, it includes functions for batching large files.
