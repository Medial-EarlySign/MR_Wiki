# Home

**A note on our journey:** Medial EarlySign was a company that developed a proprietary platform for machine learning on electronic medical records. Following the company's liquidation, the decision was made to release the core software as an **open-source** project to allow the community to benefit from and build upon this technology.

Our platform is designed to transform complex, semi-structured Electronic Medical Records (EMR) into **machine-learning-ready** data and reproducible model pipelines. The framework is optimized for the unique challenges of sparse, time-series EMR data, delivering **low memory usage** and **high-speed processing** at scale.

It was conceived as a "TensorFlow" for machine learning on medical data.

All software is now open-sourced under the MIT license. Some of the models developed by Medial EarlySign that are currently in production are available exclusively through our partners.

The framework was battle-tested in production across multiple healthcare sites and was a key component of an **award-winning** submission to the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge).

## Why Use This Platform?

*   **High-Performance Processing:** Engineered for large-scale, sparse EMR time-series data where general-purpose libraries like pandas fall short.
*   **Reusable Pipelines:** Save valuable engineering time by providing shareable, tested pipelines and methods.
*   **Built-in Safeguards:** Mitigate common pitfalls like data leakage and time-series-specific overfitting.
*   **Production-Ready:** Designed for easy deployment using Docker or minimal distroless Linux images.

## Core Components

The platform is built on three key pillars:

*   **MedRepository:** A compact, efficient data repository and API for storing and accessing EMR signals. Querying categorical signals like perscriptions and diagnosis in an easy and efficient API. 
*   **MedModel:** An end-to-end machine learning pipeline that takes data from MedRepository or JSON EMR inputs to produce predictions and explainability outputs. It supports both training and inference.
*   **Medial Tools:** A suite of utilities for training, evaluation, and workflow management, including bootstrap analysis, fairness checks, and explainability.

## Getting Started

*   **Build a new model:** Follow the step-by-step [Tutorials](Tutorials/) to build a model from scratch.
*   **Use an existing model:** Browse the collection of [Models](Models) or learn how to deploy a model with [AlgoMarker Deployment](Tutorials/07.Deployment).

### Complete Example: From Data to Model

This walkthrough demonstrates a complete workflow, from loading raw data to training a predictive model.

#### Step 1: Load and Process Raw Data

First, we'll fetch the raw data and prepare it for our repository. This example uses public NHANES datasets. The `prepare_final_signals` function initiates the loading process for each data source.

```python title="1. Load Raw Data"
from ETL_Infra.data_fetcher.files_fetcher import files_fetcher
from ETL_Infra.etl_process import (
    prepare_dicts,
    prepare_final_signals,
    finish_prepare_load,
)
import requests
import pandas as pd
import os

def get_demo():
    url = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.xpt"
    cache_file = "/tmp/DEMO_J.xpt"

    if not os.path.exists(cache_file):
        print("Retrieving demo data from cdc.gov...")
        resp = requests.get(url).content
        with open(cache_file, "wb") as f:
            f.write(resp)
    
    # Helper function to read and parse the SAS file into a DataFrame
    def read_file(cache_file):
        df = pd.read_sas(cache_file, format="xport")
        df.rename(columns={"SEQN": "pid", "RIAGENDR": "GENDER", "RIDAGEYR": "Age"}, inplace=True)
        return df
    
    # Return a callable for lazy data loading, which is good practice for large datasets.
    return lambda batch_size, start_batch: files_fetcher([cache_file], batch_size, read_file, start_batch)

def get_labs():
    url = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/CBC_J.xpt"
    cache_file = "/tmp/CBC_J.xpt"
    if not os.path.exists(cache_file):
        print("Retrieving lab data from cdc.gov...")
        resp = requests.get(url).content
        with open(cache_file, "wb") as f:
            f.write(resp)

    # Helper function to read and parse the SAS file into a DataFrame
    def read_file(cache_file):
        df = pd.read_sas(cache_file, format="xport")
        convert_names = {
            "LBXRBCSI": "RBC", "LBXHGB": "Hemoglobin",
            "LBXHCT": "Hematocrit", "LBXMCHSI": "MCH",
        }
        df.rename(columns={"SEQN": "pid"}, inplace=True)
        df.rename(columns=convert_names, inplace=True)
        df["pid"] = df["pid"].astype(int)
        return df

    # Return a callable for lazy data loading.
    return lambda batch_size, start_batch: files_fetcher([cache_file], batch_size, read_file, start_batch)

# Define a working directory for the ETL process
WORK_DIR = "/tmp/NHANES_ETL"

# The system will prompt you to create the processor scripts below (BDATE.py and labs.py)
prepare_final_signals(get_demo(), WORK_DIR, "BDATE", override="n")
prepare_final_signals(get_labs(), WORK_DIR, "labs", override="n")

# Finalize the loading process and create the repository
finish_prepare_load(WORK_DIR, dest_folder="/tmp/repository/NHANES", dest_rep="nhanes")
```

When you run the script above, the framework will prompt you to create processor scripts to transform the raw dataframes into the required signal format. Create the two files below in the `signal_processings` directory as requested.

```python title="signal_processings/BDATE.py"
# This script processes demographic data to extract BDATE (birth date) and GENDER signals.
import pandas as pd

# Extract Gender
df_gender = df[["pid", "GENDER"]].rename(columns={"GENDER": "value_0"}).copy()
df_gender["signal"] = "GENDER"
df_gender = df_gender[["pid", "signal", "value_0"]]
df_gender.dropna(subset=["value_0"], inplace=True)
df_gender["value_0"] = df_gender["value_0"].map({1.0: "Male", 2.0: "Female"})

# Extract Birth Year (approximated from age)
df_age = df[["pid", "Age"]].copy()
df_age.dropna(subset=["Age"], inplace=True)
df_age["signal"] = "BDATE"
# All input data is from 2017, so we approximate the birth year.
df_age["value_0"] = (2017 - df_age["Age"].astype(int)) * 10000 + 101
df_age = df_age[["pid", "signal", "value_0"]]

# Combine and assign back to the 'df' variable
df = pd.concat([df_age, df_gender], ignore_index=True)
```

```python title="signal_processings/labs.py"
# This script processes lab results, transforming them from a wide to a long format.
import pandas as pd

df = df.drop(columns=["LBXNRBC", "signal"])
sig_list = ["Hemoglobin", "Hematocrit", "RBC", "MCH"]

# Assume the lab test date was Jan 1, 2017
df["time_0"] = 20170101

all_dfs = []
for sig in sig_list:
    sig_df = df[["pid", "time_0", sig]].rename(columns={sig: "value_0"}).copy()
    sig_df["signal"] = sig
    all_dfs.append(sig_df)

# Combine all individual signal DataFrames
df = pd.concat(all_dfs, ignore_index=True)
df.dropna(subset=["value_0"], inplace=True)
```

Finally, run the generated shell script to complete the data repository creation.

```bash
/tmp/NHANES_ETL/rep_configs/load_with_flow.sh
```

#### Step 2: Generate Training Samples

With the repository created, we'll now generate a sample file for training. This file defines which patients to include, at what point in time, and what their outcome was. For this example, we'll assign a random outcome to each patient.

```python title="2. Generate Training Samples"
import med
import random

# Initialize a repository object and load the BDATE signal to get all patient IDs
rep = med.PidRepository()
rep.read_all("/tmp/repository/NHANES/nhanes.repository", [], ["BDATE"])

# Create a DataFrame with all patients
all_patients = rep.get_sig("BDATE").rename(columns={"pid": "id"})

# Define the structure for a MedSamples file
all_patients["EVENT_FIELDS"] = "SAMPLE"
all_patients["time"] = 20170101  # The time of prediction
all_patients["outcome"] = [random.randint(0, 1) for _ in range(len(all_patients))]
all_patients["split"] = -1  # Can store split information for cross validation
all_patients["outcomeTime"] = 20500101

# Ensure columns are in the correct order and save to a TSV file
all_patients = all_patients[["EVENT_FIELDS", "id", "time", "outcome", "outcomeTime", "split"]]
all_patients.to_csv("/tmp/train_samples", index=False, sep="\t")
```

#### Step 3: Define and Train the Model

Now we define the model pipeline and train it.

First, create a JSON file that specifies the sequence of actions for feature engineering and the final prediction algorithm.

```json title="model_architecture.json"
// This is an example JSON file with comments. If your editor does not support comments in JSON, you may need to remove them.
{
    "$schema": "https://raw.githubusercontent.com/Medial-EarlySign/MR_Tools/refs/heads/main/medmodel_schema.json",
    "model_json_version": 2,
    "model_actions": [
        // Action: Clean raw signal data.
        {
            "action_type": "rp_set",
            "members": [
                {
                    "rp_type": "basic_cln",
                    "signal": ["Hemoglobin", "RBC", "MCH", "Hematocrit"],
                    "type": "iterative",
                    "trimming_sd_num": 7, // Iteratively trim values beyond 7 SD.
                    "removing_sd_num": 14, // Remove values beyond 14 SD.
                    "range_min": 0
                }
            ]
        },
        // Action: Remove measurements that have different values on the same date.
        {
            "action_type": "rp_set",
            "members": [
                {
                    "rp_type": "sim_val",
                    "signal": ["Hemoglobin", "RBC", "MCH", "Hematocrit"],
                    "type": "rem_diff"
                }
            ]
        },
        // Action: Apply clinical rules to clean data (e.g., MCH = (Hemoglobin / RBC) * 10).
        {
            "action_type": "rp_set",
            "members": [
                {
                    "rp_type": "rule_cln",
                    "addRequiredSignals": "1",
                    "time_window": 0,
                    "tolerance": 0.1,
                    "calc_res": 0.1,
                    "consideredRules": ["2"]
                }
            ]
        },
        // Action: Generate 'Age' feature from the 'BDATE' signal.
        {
            "action_type": "feat_generator",
            "fg_type": "age"
        },
        // Action: Generate features from the last 3 years (1095 days) of data.
        {
            "action_type": "feat_generator",
            "fg_type": "basic",
            "type": ["last", "min"],
            "win_from": 0,
            "win_to": 1095,
            "signal": ["Hemoglobin", "RBC", "MCH", "Hematocrit"]
        }
    ],
    // Define the predictor.
    "predictor": "xgb",
    "predictor_params": "tree_method=auto;booster=gbtree;objective=binary:logistic"
}
```

Finally, run the training script. It initializes the model from the JSON file, loads the necessary data from the repository, and trains the XGBoost predictor.

```python title="3. Train the Model"
import med

# --- 1. Configuration ---
rep_path = '/tmp/repository/NHANES/nhanes.repository'
model_json_path = 'model_architecture.json'
samples_path = '/tmp/train_samples'
output_model_path = 'trained_model.bin'

# --- 2. Initialize Model and Fit to Repository ---
print("Initializing model...")
model = med.Model()
model.init_from_json_file(model_json_path)

# Initialize the repository to understand its structure. This helps the model
# identify which signals can be generated vs. which need to be fetched.
rep = med.PidRepository()
rep.init(rep_path)
model.fit_for_repository(rep)

# Get the list of signals that must be fetched from the repository.
required_signals = model.get_required_signal_names()

# --- 3. Load Data ---
print("Loading training samples and repository data...")
samples = med.Samples()
samples.read_from_file(samples_path)

# Get patient IDs from the samples to load only the necessary data.
patient_ids = samples.get_ids()

# Load the actual data for the required signals and patients.
rep = med.PidRepository()
rep.read_all(rep_path, patient_ids, required_signals)

# --- 4. Train the Model ---
print("Starting model training...")
model.learn(rep, samples)
print("Training complete.")

# --- 5. Save the Trained Model ---
model.write_to_file(output_model_path)
print(f"Model saved to {output_model_path}")

# Print the model's feature matrix.
print(model.features.to_df())
```

## Resources

*   **[MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs):** The core infrastructure libraries.
*   **[MR_Tools](https://github.com/Medial-EarlySign/MR_Tools):** Tools and pipelines built on top of MR_LIBS.
*   **[MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts):** A collection of helper scripts and utilities.

Explore the documentation to understand the architecture and tools.