# Simulator

## Goal

Simulate expected performance of a frozen model under a new environment (covariate/covariance shift). The simulator lets you specify target population characteristics (age, sex, availability of signals, etc.) and estimates how model performance will change.

## Approach (high level)

The simulator reweights or subsamples an existing labeled dataset (where ground-truth and original performance are known) to match a user-defined target population. This is a statistical, not machine-learning, adjustment - conceptually similar to inverse-probability weighting but using an explicit target population definition rather than learned propensities.

Example: if the original population age range is uniform 40-80 and the target environment is 50-80, patients aged 40-49 receive zero weight in the estimation and the performance metrics are computed on the reweighted population.

This method generalizes to multi-dimensional scenarios (age, sex, signal missingness, etc.) and gives an **accurate estimate** of expected performance when the target population is well specified.

## Code location

The simulator is implemented in the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository under: `AlgoMarker_python_API/PopulationAnalyzer`

Slides and documentation:

- [Brief Slides](../SharePoint_Documents/Research/Performance_Simulator/Performance_Simulator.pptx)
- [Full simulator slides](../SharePoint_Documents/Research/Performance_Simulator/performance_simulator_20241229.pptx)

## Running the server

From the simulator directory start the UI server:

```bash
./ui.py
```

Default port: 3764. Use the full path to `ui.py` if you run it from another working directory.

## Adding a new AlgoMarker

To register a new AlgoMarker in the simulator UI:

1. Copy an existing AlgoMarker Python file (for example `LungFlag.py`) into the `algomarkers/` folder.
   - The chosen filename (without `.py`) will appear in the UI. Filenames may use `_SLASH_` to show a `/` in the UI.
2. Create or edit the AlgoMarker config Python file (the module the UI imports) and define the following fields:
    - **am_regions**: dict mapping region keys to `ReferenceInfo` objects (paths to reference matrices, repository paths, CV results, etc.).
    - **sample_per_pid**: numeric bootstrap parameter (how many samples per patient).
    - **default_region**: optional default region key.
    - **additional_info**: short descriptive text shown near the model selector.
    - **optional_signals**: optional list of InputSignal/InputSignalsExistence objects describing extra input groups (e.g., Smoking, Labs, BMI).
    - **model_path**: path to the model file used by the simulator.
    - **orderdinal**: optional integer to order this AlgoMarker in the UI.

These fields are used by the server to load reference matrices, build cohorts, and run the simulation UI.

## Example configuration

An example (abridged) config is included below. The full example in the original file shows cohort filters, region definitions, and optional signals.

<details><summary>Click to expand</summary>

```python
from models import *

lung_cohorts = [
    CohortInfo(cohort_name='Ever Smokers Age 50-80', bt_filter=lambda df: (df['age']>=50) & (df['age']<=80)),
    CohortInfo(cohort_name='Ever Smokers Age 45-80', bt_filter=lambda df: (df['age']>=45) & (df['age']<=80)),
    CohortInfo(cohort_name='Ever Smokers Age 40-90', bt_filter=lambda df: (df['age']>=40) & (df['age']<=90)),
    CohortInfo(cohort_name='Ever Smokers Age 55-74', bt_filter=lambda df: (df['age']>=55) & (df['age']<=74)),
]

us_lung_cohorts = [
    CohortInfo(cohort_name='Ever Smokers Age 50-80', bt_filter=lambda df: (df['age']>=50) & (df['age']<=80)),
    CohortInfo(cohort_name='Ever Smokers Age 55-74', bt_filter=lambda df: (df['age']>=55) & (df['age']<=74)),
    CohortInfo(cohort_name='Ever Smokers Age 45-90', bt_filter=lambda df: (df['age']>=45) & (df['age']<=90)),
    CohortInfo(
        cohort_name='USPSTF Age 50-80 (20 pack years, <15 years quit)',
        bt_filter=lambda df: (df['age']>=50) & (df['age']<=80) &
                             (df['smoking.smok_pack_years']>=20) &
                             (df['smoking.smok_days_since_quitting']<=15*365)
    ),
]

am_regions = {
    'US-KP': ReferenceInfo(
        matrix_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/reference_matrices/reference_features_kp.final.matrix',
        control_weight=20,
        cohort_options=us_lung_cohorts,
        default_cohort='USPSTF Age 50-80 (20 pack years, <15 years quit)',
        repository_path='/nas1/Work/CancerData/Repositories/KP/kp.repository',
        model_cv_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/results',
        model_cv_format='CV_MODEL_%d.medmdl'
    ),
    'UK-THIN': ReferenceInfo(
        matrix_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/reference_matrices/reference_features_thin.final.matrix',
        cohort_options=lung_cohorts,
        default_cohort='Ever Smokers Age 55-74',
        repository_path='/nas1/Work/CancerData/Repositories/THIN/thin_2021.lung/thin.repository'
    ),
}

sample_per_pid = 0
default_region = 'UK-THIN'
additional_info = 'Time Window 90-365'

optional_signals = [
    InputSignalsExistence(
        signal_name='Smoking',
        list_raw_signals=['Smoking_Duration', 'Smoking_Intensity', 'Pack_Years', 'Smoking_Quit_Date'],
        tooltip_str='If true, include smoking duration/intensity/pack-years/quit date in inputs.'
    ),
    InputSignalsExistence(
        signal_name='Labs',
        list_raw_signals=[
            "Albumin", "ALKP", "ALT", "Cholesterol", "Triglycerides", "LDL", "HDL", "Creatinine",
            "Glucose", "Urea", "Eosinophils%", "Hematocrit", "Hemoglobin", "MCHC-M", "MCH",
            "Neutrophils#", "Neutrophils%", "Platelets", "RBC", "WBC", "RDW", "Protein_Total",
            "Lymphocytes%", "Basophils%", "Monocytes%", "Lymphocytes#", "Basophils#", "Monocytes#",
            "Eosinophils#", "MCV"
        ]
    ),
    InputSignalsExistence(signal_name='BMI', list_raw_signals=['BMI', 'Weight', 'Height']),
    InputSignalsExistence(signal_name='Spirometry', list_raw_signals=['Fev1']),
]

model_path = '/earlysign/AlgoMarkers/LungFlag/lungflag.model'
orderdinal = 1
```

</details>
