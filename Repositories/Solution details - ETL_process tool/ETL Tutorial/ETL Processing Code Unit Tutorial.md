# ETL Processing Code Unit Tutorial

This section explains how to transform your raw DataFrame into the required format for downstream analysis in the ETL pipeline.

---

## ETL Processing Workflow

After retrieving your data, the processing step includes:

1. **PID Mapping:**  
   Convert non-numeric patient IDs to numeric. The mapping is stored in `[WORK_DIR]/FinalSignals/ID2NR`. Demographic signals create this mapping; all other signals join on it. Rows with missing patients are dropped (with a message).

2. **Signal Mapping:**  
   If your DataFrame has a `signal` column, map signals using your [CODE_DIR](../High%20level%20-%20important%20paths/CODE_DIR) resources - under `configs/map.tsv` need to have columns: source, destination

3. **Data Transformation:**  
   Transform the DataFrame to the final format.  
   **This is the main customization step for your ETL.**

4. **Testing:**  
   Implement and run tests to validate the processed data.

5. **Storing:**  
   Sort and save the processed data in `[WORK_DIR]/FinalSignals`.

<img src="/attachments/14811382/14811576.png"/>

---

## Processing the DataFrame

Suppose you start with a DataFrame called `df` and want to process demographic signals (e.g., GENDER).  
You also have a `code_dir` variable pointing to your ETL code directory for accessing configs or helpers.

**Example Source DataFrame:**

```text
   dup  index_dato  LC  date_LCdiagnosis  outpatientclinic_date  Age  FEV1  height  weight   BMI   Sex Smokingstatus  stage  NSCLC  pathology signal  pid
0    0  12mar2013   0              NaN             12mar2013     85   NaN     NaN    NaN    23.0  male  Formersmoker   NaN    NaN        NaN   None    1
1    1  04jun2021   0              NaN             04jun2021     92  0.89   164.0   50.0     NaN  male  Formersmoker   NaN    NaN        NaN   None    2
...
```

---

## Transforming the DataFrame

Here’s how to convert the input DataFrame into the required format for the GENDER signal:

```python
# Start with DataFrame "df" and process it to generate the "demographic" signal (e.g., GENDER)
# The output DataFrame should have these columns:
#   pid
#   signal
#   value_0 (string categorical, e.g., 'Male', 'Female')

# Extract relevant columns and rename 'Sex' to 'value_0'
df = df[['pid', 'Sex']].rename(columns={'Sex': 'value_0'})
# Create a new 'signal' column with the value 'GENDER'
df['signal'] = 'GENDER'
# Standardize values in 'value_0'
df.loc[df['value_0'] == 'male', 'value_0'] = 'Male'
df.loc[df['value_0'] == 'female', 'value_0'] = 'Female'
# Keep only the required columns and remove duplicates per patient
df = df[['pid', 'signal', 'value_0']].drop_duplicates().reset_index(drop=True)
```

**Notes:**
- The ETL infrastructure will validate the signal type. If something is missing, a test will fail and prompt you to fix it.
- Any `print` statements will be logged automatically.
- The comments above are part of the ETL template to help you complete your code.
- To import helpers, use your `code_dir` path, e.g.,  
  `from signal_processings.process_helper import *`

---

## Code File Organization & Execution Order

- If your DataFrame has a non-None `signal` column, its value determines the signal name. Otherwise, the name passed to `prepare_final_signals` is used.
- If the DataFrame contains multiple signal names, it will be split by signal.
- For each signal, the ETL will execute the most specific code found in `[CODE_DIR]/signal_processings/$SIGNAL_NAME_OR_TAG.py`.  
  If not found, it will fall back to more general tags as defined in the global signal definitions (`rep_signals/`).

**Example Directory Structure:**

```text
CODE_DIR/
├── signal_processings/
│   ├── GENDER.py
│   ├── cbc.py
│   └── labs.py
├── configs/
└── ...
```

---

For more details, refer to the [global signal definitions](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths/structure/ETL_INFRA_DIR).

