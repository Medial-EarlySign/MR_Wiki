# Applying Your Model

This guide demonstrates how to apply a trained model to generate predictions. You can use either the Python API for programmatic control or the command-line tools for a code-free approach.

## Method 1: Python API

This method offers model application process within a Python script.

### Prerequisites

Before you begin, make sure you have:

1.  Installed the [Python API for MES Infrastructure](../../Installation/Python%20API%20for%20MES%20Infrastructure.md).
2.  Loaded your data repository by following the [ETL Tutorial](../01.ETL%20Tutorial/index.md).
3.  Created your testing dataset as outlined in the [Create Samples Tutorial](../03.Create%20Samples/index.md).

### Inference Script

The following script shows how to perform model inference from start to finish.

```python
import med

# --- Configuration ---
# Path to your data repository
rep_path = ''
# Path to your trained MedModel file
model_file = ''
# Path to your samples file. Alternatively, load from a DataFrame
# using: samples.from_df(dataframe_object)
samples_file = ''

# --- Initialization ---
print("Initializing repository...")
rep = med.PidRepository()
# Initialize for the first processing step
rep.init(rep_path)

# --- Load Model ---
print("Loading model...")
model = med.Model()
model.read_from_file(model_file)
model.fit_for_repository(rep)
# Get the list of signals required by the model
signalNamesSet = model.get_required_signal_names()

# --- Load Samples ---
print("Loading samples...")
samples = med.Samples()
samples.read_from_file(samples_file)
# Get the IDs from the samples to fetch relevant data
ids = samples.get_ids()

# --- Read Data ---
print("Reading data from repository...")
# Read only the necessary data for the specified IDs and signals
rep.read_all(rep_path, ids, signalNamesSet)

# --- Apply Model ---
print("Applying model to samples...")
model.apply(rep, samples)

# --- Save Results ---
# The 'samples' object now contains the model scores
# Convert to a DataFrame for further analysis
df = samples.to_df()
# Save the results to a CSV file
df.to_csv('output_file.csv', index=False)
# Or save as a samples file
samples.write_to_file('output_samples.tsv')

# The feature matrix is available via: model.features.to_df()
print("Inference complete. Results saved.")
```

## Method 2: Command-Line Tools

If you prefer to work from the command line, MES offers tools to apply models without writing any Python code.

### Prerequisites

First, install the [MES Tools for Training and Testing Models](../../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md).

### Prediction Tools

Use the following tool to generate predictions or extract the full feature matrix from your model's pipeline:

*   [Apply a model with Flow](../../Infrastructure%20Library/Medial%20Tools/Using%20the%20Flow%20App/index.md#predictingapplying-a-model)