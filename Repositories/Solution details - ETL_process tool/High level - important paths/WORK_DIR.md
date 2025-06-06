# WORK_DIR
Folder that contains output files from the loading process **- IMPORTANT - NO NEED TO EDIT ANYTHING IN THIS FODLER. ALL IS CREATED AUTOMATICALLY**:
- FILE -** loading_status.state** - keeps track on the loading process:
  - The file has 3 columns : signal, date+time (last date the signal was created), and status.
  - Signals that are not in the file - would be processed. 
  - Signals with "Completed" status would be skipped, unless override flag was passed. 
    - Setting override for a processed signal is equal to manually erasing its row from the file.
  - Signals with "In Process" status is this the name? - would be processed from the first unprocessed batch (see next).
- FILE  - **loading_batch_status.state** - keeps track on the loading process up to the batch level. If something crashed, next run the ETL would continue from the first unprocessed batch. 
- FOLDER - **FinalSignals** - the directory with the final signals for loading with Flow, may also contains ID2NR if conversions between patient ID to numeric is needed (ID2NR will not be loaded). 
- FOLDER - **rep_configs** - directory with configurations for loading the repository. Will contains the signals file, convert_config and a script to run Flow to load the data. Will be created automatically.
- FOLDER - **outputs** - a directory with reports and tests analysis for each signal:
  - FOLDER - **$SIGNAL_NAME** - directory for each signal statistics. For example "Hemoglobin" directory - test for time, and values, compare to reference distribution, resolution, etc. It will also contain analysis for each batch (if you have batches) and all together.
  - FILE - **test.$SIGNAL_NAME.log** - with results for tests on all batches together for this signal. results of test = the "prints" you call to the screen from each test. If test fails - crashed or returns False, you won't be able to proceed and it will ask you to fix the ETL to pass the test. Here you will see the outputs after passing the test. Each time you fix your code and rerun the code, this file is overwritten. To see results from all batched alone you will need to go into "test.labs.log" and see results of this processing batch by batch if you have and for all signals one after the other
- FOLDER - **signal_processings_log** - directory with logging of the signal processing and the exploration/games you did with the data 
  - FILE - **process_XXXX.log** - you will see "outputs/prints" from your processings. If you call "print" from labs.py it will appear here under "process_labs.log" for each batch one after the other
  - FILE - **XXXX.log** - If you are using interactive mode - you will see the commands and outputs of those commands when you were inspecting the data - like "logging" of your process to identify the ETL.
