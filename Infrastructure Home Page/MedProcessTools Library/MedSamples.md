# MedSamples
### MedSamples is a data structure and helpers to deal with a samples, a list of individuals + time-points (dates) and associated information such as outcome (with time), split and prediction(s). 
The data is contained in a three-tier structure. The basic unit is [MedSample](https://Medial-EarlySign.github.io/MR_LIBS/classMedSample), which contiains information about a single sample. [MedIdSamples ](https://Medial-EarlySign.github.io/MR_LIBS/classMedIdSamples)contains information about a set of samples for a specific patient (id), while [MedSamples](https://Medial-EarlySign.github.io/MR_LIBS/classMedSamples) contains a set of [MedIdSamples ](https://Medial-EarlySign.github.io/MR_LIBS/classMedIdSamples)for a collection of patients.
Note that it is not inherently guaranteed that all samples inside a MedIdSample have the same id, but many functions will probably not worked if it is not so. It is also not guaranteed that different samples of the same id are assigned the same split (for cross validation) and that this split is the same as the split parameter in MedIdSample. However, it is ***highly recommended*** for the user to maintain one split per id.
Samples can be read and written to a csv or binary files
### Include file is - *H:/MR/Libs/Internal/MedProcessToola/MedProcessTools/MedSamples.h*
 
