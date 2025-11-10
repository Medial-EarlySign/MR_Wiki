# MedSamples

he MedSamples object is designed to store key fields such as "label", "patient id", and "requested prediction time", along with additional information. Data is stored in a tab-separated file format. The "pred_0" field, representing a prediction result for performance analysis, is optional.

* `EVENT_FIELDS`: Static field; always set to "SAMPLE"
* `id`: Numeric patient identifier
* `time` : Requested prediction time; only data prior to this point is used for prediction
* `outcome`: The label or outcome; can be binary (0/1) or numeric (for regression)
* `outcomeTime`: Event time if the patient is labeled "1", or "end of followup" for "0". This field is optional; if unused, you can specify a placeholder date like "19000101". Useful for filtering by time windows.
* `split`: Optional field for specifying patient split. Typically, splits are assigned based on patient id in a separate file, so please specify "-1" 
* `pred_0` - optional prediction result

## Example file
```
EVENT_FIELDS	id	time	outcome	outcomeTime	split
SAMPLE	1	20250101	0	20250820	-1
SAMPLE	1	20250201	0	20250820	-1
SAMPLE	2	20250101	1	20250820	-1
```

Explain:

* Patient 1 has two prediction points (20250101 and 20250201), both labeled "0". Follow-up is documented until 20250820.
* Patient 2 has one prediction point (20250101) with label "1". The event date is 20250820.

## Overview

MedSamples is a data structure and set of helper functions for managing samples—combinations of individuals, time-points (dates), and associated information such as outcomes, outcome times, splits, and predictions.

The data is organized in a three-tier hierarchy:

1. [MedSamples](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamples): Represents a collection of MedIdSamples for multiple patients
2. [MedIdSamples](https://Medial-EarlySign.github.io/MR_LIBS/classMedIdSamples): Represents a set of samples for a specific patient (id).
3. [MedSample](https://Medial-EarlySign.github.io/MR_LIBS/classMedSample):  Represents a single sample.

### Notes:

* It is not strictly enforced that all samples within a `MedIdSample` share the same id, but many functions may not work correctly otherwise.
* Different samples for the same id may have different splits, and these may not match the split parameter in `MedIdSample`. However, it is **strongly recommended** to maintain a single split per id.

Samples can be read from and written to CSV or binary files.
 
