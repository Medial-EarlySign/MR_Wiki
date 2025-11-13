# Test 01 - Generate Repository

## Purpose

Load input data from the AlgoAnalyzer into a repository for evaluation. This step prepares the dataset for further ETL tests and model validation.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output folder path to process and load the repository
- `SILENCE_RUN_INPUT_FILES_PATH`: Path to the input data files in "file_api" format

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 1
```
Or include as part of the full suite:
```bash
./run.sh
```

Check the output repository for correct data loading.

## What This Test Does

This script loads the new dataset into a structured repository, checks data integrity, and prepares files for further analysis. The repository is the foundation for all subsequent validation steps.

## Output Location

- Processed dataset: `${WORK_DIR}/rep`
- ETL log files: `${WORK_DIR}/ETL`

## How to Interpret Results

ETL test results are found in `${WORK_DIR}/ETL`. For more details, see [ETL_WORK_DIR](../../../../../Tutorials/01.ETL%20Tutorial/High%20level%20-%20important%20paths/WORK_DIR.md).

### Test Results Review

The main ETL log is `${WORK_DIR}/01.generate_repository.log`. Use the following approach to review the log:

#### a. High-level review of signal value distributions and sources

Example output:

```text
Done testing nulls in signal Hemoglobin
unit:g/L || KLD (127)= 0.005790, KLD_to_Uniform=0.740022, entory_p=4.105875, grp_cnt=8444, group_counts=1/4
unit:g/l || KLD (127)= 0.010441, KLD_to_Uniform=0.740022, entory_p=4.105875, grp_cnt=6995, group_counts=2/4
There are issues with low range, please have a look (more than factor 3)
       q  value_0  reference     ratio1    ratio2      ratio
0  0.001   80.908        7.2  11.237223  0.088990  11.237223
1  0.010  102.000        9.0  11.333333  0.088235  11.333333
2  0.100  126.000       11.2  11.250000  0.088889  11.250000
There are issues with the median, please have a look (more than factor 2)
     q  value_0  reference     ratio1    ratio2      ratio
3  0.5    145.0       13.3  10.902255  0.091724  10.902255
There are issues with high range, please have a look (more than factor 3)
       q  value_0  reference     ratio1    ratio2      ratio
4  0.900    163.0  15.300000  10.653595  0.093865  10.653595
5  0.990    178.0  16.799999  10.595239  0.094382  10.595239
6  0.999    189.0  17.900000  10.558659  0.094709  10.558659
Done testing values of signal Hemoglobin
```

In this example, Hemoglobin data comes from four sources, but only two are large enough for analysis. The first source uses unit `g/L`, the second `g/l`. A small KLD value (<< 1) means the source's value distribution is similar to the overall Hemoglobin distribution. You can verify this by reviewing graphs in `${WORK_DIR}/ETL/outputs/Hemoglobin`, but if the numbers are very small, further review may not be necessary.

Lines starting with "There are issues with" and the following tables highlight discrepancies:

- `q`: Quantile being compared
- `value_0`: Quantile in current dataset
- `reference`: Quantile in reference dataset
- `ratio1`: value_0 / reference
- `ratio2`: 1 / ratio1
- `ratio`: max(ratio1, ratio2)

Large ratios (e.g., factor of 10) may indicate mismatched units. The log may suggest how to fix units, such as converting from `g/L` or `g/l` to the expected `g/dL` (as described in the AlgoMarker), and recommend multiplying by 10.

> **Important:** If there are mismatches in the input, loading will not fail. Warnings will appear in the log, and it is **your responsibility** to review and ensure the data is correct.

#### b. Deep dive into important features

Important features for the model are defined in `configs/env.sh`. For each SIGNAL, detailed outputs include:

- Specific test log: `ETL/outputs/test.$SIGNAL.log`
- Processing logs (e.g., dropped lines): `ETL/signal_processings_log/$SIGNAL.log`
- Distribution of day, month, year, and value: `ETL/signal_processings_log/SIGNAL/batches/`
    * If there are multiple batches, an aggregated report appears in `ETL/signal_processings_log/SIGNAL`

It is recommended to manually check logs and charts for all important features. For example:

* Example 1: Monthly distribution of Hemoglobin samples from a dataset prepared in mid-2023. Monthly samples may look suspicious, but the yearly graph shows samples are only from the last year, so more samples in early months are expected.

<img src="../../../../../attachments/13926413/13926420.png"/>
<img src="../../../../../attachments/13926413/13926421.png"/>

* Example 2: On the right, a normal distribution of a lab measurement. On the left, unclear 'vibrations'. This may not affect the model, but you should check with the dataset owner to ensure it does not hide a larger issue.

<img src="../../../../../attachments/13926413/13926422.png"/>
<img src="../../../../../attachments/13926413/13926423.png"/>
 
