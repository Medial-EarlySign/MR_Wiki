## Description of the simulator
The code base is under Tools git repository. 
Under MR_TOOLS git repo it is this directory: AlgoMarker_python_API/PopulationAnalyzer
To run the server:
`./ui.py` from this folder or provide full path to ui.py
Please run this in node-04 that Ori/Eran can access it. The port will be 3764.
### Add additional Algomarker
Please copy LungFlag.py or other model in folder "algomarkers" under this project.
The file name you give will be used in the application with suffix ".py".
There is a keyword "\_SLASH\_" that will be replaced in display by "/".
You will need to define those fields in the python config file of the AlgoMarker:
- am_regions - An Object of type dictionary from "string" name of region to ReferenceInfo Object
- sample_per_pid - the numeric parameter for bootstrap assement
- default_region - string parameter to choose default region (optional)
- additional_info - string paramter to describe/put text near the model selection
- optional_signals - List of Objects of type "InputSignal" that describes options for changing model inputs. For example erasing list of signals, limiting the history, taking just most recent. this is optional
- model_path - string to model path
- orderdinal - integer number to list this AlgoMarker compared to others (optional)
### Example config
<details><summary>Click to expand example</summary>

```python
from models import *
lung_cohorts = []
lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 50-80', bt_filter=lambda df: (df['age']>=50) & (df['age']<=80) ))
lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 45-80', bt_filter=lambda df: (df['age']>=45) & (df['age']<=80) ))
lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 40-90', bt_filter=lambda df: (df['age']>=40) & (df['age']<=90) ))
lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 55-74', bt_filter=lambda df: (df['age']>=55) & (df['age']<=74) ))
#Add USPSTF to us
us_lung_cohorts = []
us_lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 50-80', bt_filter=lambda df: (df['age']>=50) & (df['age']<=80) ))
us_lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 55-74', bt_filter=lambda df: (df['age']>=55) & (df['age']<=74) ))
us_lung_cohorts.append(CohortInfo(cohort_name='Ever Smokers Age 45-90', bt_filter=lambda df: (df['age']>=45) & (df['age']<=90) ))
us_lung_cohorts.append(CohortInfo(cohort_name='USPSTF Age 50-80 (20 pack years, less then 15 years quit)', bt_filter=lambda df: (df['age']>=50) & (df['age']<=80) &
                                   (df['smoking.smok_pack_years']>=20) & (df['smoking.smok_days_since_quitting']<=15*365) ))
am_regions = dict()
am_regions['US-KP'] = ReferenceInfo(matrix_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/reference_matrices/reference_features_kp.final.matrix', control_weight=20, cohort_options=us_lung_cohorts, default_cohort='USPSTF Age 50-80 (20 pack years, less then 15 years quit)', repository_path='/nas1/Work/CancerData/Repositories/KP/kp.repository', model_cv_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/results', model_cv_format='CV_MODEL_%d.medmdl')
am_regions['UK-THIN'] = ReferenceInfo(matrix_path='/nas1/Work/Users/eitan/Lung/outputs/models2023/EX3/model_63/reference_matrices/reference_features_thin.final.matrix', cohort_options=lung_cohorts, default_cohort='Ever Smokers Age 55-74', repository_path='/nas1/Work/CancerData/Repositories/THIN/thin_2021.lung/thin.repository')
sample_per_pid = 0
default_region = 'UK-THIN'
additional_info = 'Time Window 90-365'
optional_signals = []
optional_signals.append(InputSignalsExistence(signal_name='Smoking', list_raw_signals=['Smoking_Duration', 'Smoking_Intensity',
                                                                                        'Pack_Years', 'Smoking_Quit_Date'], tooltip_str='If true will include Smoking_Duration, Smoking_Intensity, Pack_Years, Smoking_Quit_Date  in the inputs and not only status'))
optional_signals.append(InputSignalsExistence(signal_name='Labs', list_raw_signals=["Albumin","ALKP","ALT","Cholesterol",
                                                                                                    "Triglycerides","LDL","HDL","Creatinine",
                                                                                                    "Glucose","Urea","Eosinophils%","Hematocrit",
                                                                                                    "Hemoglobin","MCHC-M","MCH","Neutrophils#",
                                                                                                    "Neutrophils%","Platelets","RBC","WBC", "RDW",
                                                                                                    "Protein_Total", "Lymphocytes%", "Basophils%",
                                                                                                    "Monocytes%", "Lymphocytes#", "Basophils#",
                                                                                                    "Monocytes#","Eosinophils#","MCV"]))
optional_signals.append(InputSignalsExistence(signal_name='BMI', list_raw_signals=['BMI', 'Weight', 'Height']))
optional_signals.append(InputSignalsExistence(signal_name='Spirometry', list_raw_signals=['Fev1']))
model_path = '/earlysign/AlgoMarkers/LungFlag/lungflag.model'
orderdinal = 1
```
</details>
