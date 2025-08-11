## Simulator Overview

The simulator code is located in the [Tools](https://github.com/Medial-EarlySign/MR_Tools) git repository, specifically under the MR_TOOLS repo at: `AlgoMarker_python_API/PopulationAnalyzer`.

### Running the Server

To start the server, execute `./ui.py` from this directory, or use the full path to `ui.py`. The server default port is 3764.

### Adding a New AlgoMarker

To add an additional AlgoMarker, copy an existing model file (e.g., `LungFlag.py`) into the "algomarkers" folder within this project. The filename you choose will be used in the application with a `.py` extension. The keyword `_SLASH_` in filenames will be displayed as `/` in the UI.

In the Python config file for the AlgoMarker, define the following fields:

- **am_regions**: Dictionary mapping region names (strings) to `ReferenceInfo` objects.
- **sample_per_pid**: Numeric parameter for bootstrap assessment.
- **default_region**: (Optional) String specifying the default region.
- **additional_info**: String for descriptive text near the model selection.
- **optional_signals**: (Optional) List of `InputSignal` objects describing input options (e.g., limiting history, selecting recent signals).
- **model_path**: String specifying the model's path.
- **orderdinal**: (Optional) Integer for ordering this AlgoMarker among others.

### Example Configuration

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
        cohort_name='USPSTF Age 50-80 (20 pack years, less then 15 years quit)',
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
        default_cohort='USPSTF Age 50-80 (20 pack years, less then 15 years quit)',
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
        tooltip_str='If true will include Smoking_Duration, Smoking_Intensity, Pack_Years, Smoking_Quit_Date in the inputs and not only status'
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
    InputSignalsExistence(
        signal_name='BMI',
        list_raw_signals=['BMI', 'Weight', 'Height']
    ),
    InputSignalsExistence(
        signal_name='Spirometry',
        list_raw_signals=['Fev1']
    ),
]

model_path = '/earlysign/AlgoMarkers/LungFlag/lungflag.model'
orderdinal = 1
```
</details>
