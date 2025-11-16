# Training a Model

This guide covers two primary methods for training a model: using the Python API for a code-driven approach or using command-line tools.

## Step 1: Define the Model Architecture

Before training, you must define the model's architecture in a JSON file. This file specifies the entire pipeline, including feature generators, processors, and the algorithm to be used. This is conceptually similar to defining layers and stacking them in a deep learning framework.

For detailed instructions on the file format, see the [MedModel JSON format documentation](../../Infrastructure%20Library/MedModel%20json%20format.md).

## Method 1: Training with the Python API

This method provides control over the training process within a Python script.

### Prerequisites

Ensure you have completed the following setup steps:

1.  **Install Python API**: [Python API for MES Infrastructure](../../Installation/Python%20API%20for%20MES%20Infrastructure.md).
2.  **Load Data Repository**: Follow the [ETL Tutorial](../01.ETL%20Tutorial/index.md).
3.  **Create Samples**: Prepare your training data as described in the [Create Samples Tutorial](../03.Create%20Samples/index.md).

### Python Training Example

The following script demonstrates the end-to-end process of training a model.

```python
import med

# --- 1. Configuration ---
rep_path = '/path/to/your/repository_file'
model_json_path = '/path/to/your/model_architecture.json'
samples_path = '/path/to/your/training_samples.tsv'
output_model_path = 'trained_model.bin'

# --- 2. Initialize Model and Fit to Repository ---
print("Initializing model and fitting to the repository...")

# Load the model architecture from the JSON file
model = med.Model()
model.init_from_json_file(model_json_path)

# Before loading all data, initialize a repository to analyze its structure
# This helps the model determine which signals are "virtual" (i.e., can be
# generated from other signals, like BMI from Height and Weight) versus
# which need to be fetched directly.
rep = med.PidRepository()
rep.init(rep_path)
model.fit_for_repository(rep)

# Get the list of signals that must be fetched from the repository
required_signals = model.get_required_signal_names()

# --- 3. Load Data ---
print("Loading training samples and repository data...")

# Load the training samples (patient IDs, dates, and labels)
samples = med.Samples()
samples.read_from_file(samples_path)
# Alternatively, load from a pandas DataFrame:
# samples.from_df(your_dataframe)

# Get the unique patient IDs required for training
patient_ids = samples.get_ids()

# Load the actual data for the required signals and patients
rep = med.PidRepository()
rep.read_all(rep_path, patient_ids, required_signals)

# --- 4. Train the Model ---
print("Starting model training...")
model.learn(rep, samples)
print("Training complete.")

# --- 5. Save the Trained Model ---
model.write_to_file(output_model_path)
print(f"Model saved to {output_model_path}")

# --- Optional: Post-Training Steps ---

# Access the generated feature matrix as a pandas DataFrame
feature_matrix_df = model.features.to_df()

# Apply the trained model to a new set of samples (e.g., a test set)
# test_samples = med.Samples()
# test_samples.read_from_file('path/to/test_samples.tsv')
# predictions = model.apply(rep, test_samples)

```

### Loading a Trained Model

You can load a previously trained binary model file directly without needing the original JSON or data.

```python
import med

model = med.Model()
model.read_from_file('trained_model.bin')
```

## Method 2: Training with Command-Line Tools

For users who prefer command-line operations, MES provides tools to train models without writing Python code.

### Prerequisites

First, ensure you have set up the [MES Tools for Training and Testing Models](../../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md).

### Training Tools

*   **Flow App**: For a straightforward training run without hyperparameter tuning.
    *   **Guide**: [Training with Flow](../../Infrastructure%20Library/Medial%20Tools/Using%20the%20Flow%20App/index.md#training-a-model)
*   **Optimizer**: For grid-search style hyperparameter tuning with built-in regularization to improve generalization. For more advanced tuning, consider using external libraries like Optuna.
    *   **Guide**: [Optimizer Tool](../../Infrastructure%20Library/Medial%20Tools/Optimizer.md)
