# Create MedSamples

Create a tab-separated MedSamples file describing prediction times and outcomes for each patient: [MedSamples format](../../Infrastructure%20Library/MedProcessTools%20Library/MedSamples.md).

Use the Python API when possible to generate MedSamples. Each row typically contains a patient identifier, prediction time, outcome (0/1 or numeric for regression), outcome time, and optional split/metadata fields.

Suggested process:

1. Generate candidate samples (patient id + date) without labels.
2. Label and exclude ineligible samples, documenting exclusions for cohort diagrams and validation.

Example (creating samples for date `20251011`):

```python
import med
rep = med.PidRepository()

rep.read_all("/path/to/repository", [], ["BDATE"])
bdate_sig = rep.get_sig("BDATE").rename(columns={"pid": "id"})

bdate_sig["EVENT_FIELDS"] = "SAMPLE"
bdate_sig["time"] = 20251011
bdate_sig["outcome"] = 0
bdate_sig["split"] = -1
bdate_sig["outcomeTime"] = 20500101

# Keep fields in the MedSamples order
bdate_sig = bdate_sig[["EVENT_FIELDS", "id", "time", "outcome", "outcomeTime", "split"]]

bdate_sig.to_csv("/path/to/samples", index=False, sep="\t")
```

> [!NOTE] 
> Keep in mind that training and test sample sets are often processed differently. For example, training sets may be rebalanced by year to avoid the model learning calendar trends. Those filtering and subsampling choices are part of study design and are under the responsibility of the data scientist to mitigate biases and potential information leakage in training.