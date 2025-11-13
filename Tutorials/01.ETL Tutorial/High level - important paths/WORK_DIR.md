# 📁 WORK_DIR: The Output Directory

The `WORK_DIR` is where all output files from the ETL process are automatically generated. **You should not manually edit any files in this folder.** It serves as the single source of truth for the state of the ETL and holds all final outputs and logs.

---

### Core Files and Folders

-   **`loading_status.state`**: A state file that tracks the loading status of each signal.
    -   It has three columns: `signal`, `date+time` (last creation date), and `status`.
    -   Signals with a "Completed" status are skipped unless the `override` flag is used. Overriding a signal is functionally equivalent to manually deleting its row from this file.
    -   Signals with an "In Process" status will continue from the first unprocessed batch.
-   **`loading_batch_status.state`**: Tracks the loading status at the batch level. If the process crashes, it will resume from the last unprocessed batch. Unless  `override` was set to true
-   **`FinalSignals`**: This directory contains the final, processed signal files ready for loading with Flow. It may also include an `ID2NR` file for converting patient IDs to a numeric format.
-   **`rep_configs`**: A directory that holds the necessary configuration files for the repository loading process, including the signals file, `convert_config`, and a script to run Flow. This is created automatically.
-   **`outputs`**: Contains reports and detailed test analysis for each signal.
    -   **`$SIGNAL_NAME`**: A dedicated folder for each signal (e.g., `Hemoglobin`). It holds test results, comparisons to reference distributions, and analysis for each batch and whole data combined in the end. HTML plots with distribution of values will be presented
    -   **`test.$SIGNAL_NAME.log`**: A log file containing the results of all tests run on a signal. If a test fails, the process stops, and you must fix the issue before proceeding. This file is overwritten with each new run (override = true) or appended to previous logs and stored by batch and final test for all batches in the end.
-   **`signal_processings_log`**: A directory for logging the signal processing steps.
    -   **`process_XXXX.log`**: Captures all print statements from your processing scripts (e.g., `process_labs.log`). It shows the output for each batch sequentially.
    -   **`XXXX.log`**: If you use interactive mode, this file logs the commands and outputs from your data inspection, serving as a record of your ETL development process.
