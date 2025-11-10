# Medical vocabulary mappings
There are several domains of medical knowledge/onthologies that is getting updated over time - for example diagnosis and medications.
We have several tools for generating dictionaries for those vocabularies.
 
# Updating Medical Vocabulary
We have several scripts under TOOLS git repository - MR_Tools/DictUtils:
Steps to update medications:

1. Download update vocabulary from: [https://athena.ohdsi.org/search-terms/start](https://athena.ohdsi.org/search-terms/start)
2. Select for example Drugs, Rx Norm + ATC
3. Copy and extract the files into: /nas1/Work/Data/Mapping/Medications - Or to equivalent folder for Diagnosis or Procedures, etc
4.  Run the script to extract those files into our dicts format with mapping from RX Norm to ATC - MR_Tools/DictUtils/ontologies_scripts/RX_to_ATC.new.py 
5. generate_rx_codes() - generates definitions for RX Norm + ATC from "CONCEPT.csv" to MR_Tools/DictUtils/Ontologies/RX/dicts, MR_Tools/DictUtils/Ontologies/ATC/dicts: 
6. generate_rx_maps() - generate mapping from RX Norm to ATC in MR_Tools/DictUtils/Ontologies/RX/dicts
7. add_atc_hir() - Creates the hierarchy for ATC codes
8. create_atc_syn() - generate synonm dicts for ATC to include codes in old format of ATC_ABB_CDD instead of ATC:ABBCDD
Jupyter notebook with some test on the raw files of OHDSI: [http://node-02:9000/notebooks/alon-internal/Medications_mapping.ipynb](http://node-02:9000/notebooks/alon-internal/Medications_mapping.ipynb)
 
(get_rxnorm_dicts.py - is old script of different data source + RX_to_ATC.py)
## TODOs:
- Need to complete code for NDC - current code: MR_Tools/DictUtils/ontologies_scripts/NDC_to_ATC.py
- SNOMED - MR_Tools/DictUtils/ontologies_scripts/get_snomed.py - but it's based on different data, that requires registration and to send reports+regulations... Need to switch to OHDSI 
- ICD10, ICD9 - MR_Tools/DictUtils/ontologies_scripts/icd*  scripts
 
## Loading categorical signals with those dictionaries:
After having base dictionaries with mappings, when loading new signal we can use those dictionaries and - search for missing codes, define them, use internal dictionary codes.
The library is located in: MR_Tools/RepoLoadUtils/common/dicts_utils.py
 
You can use create_dict_generic to "merge" your signal codes with existing known ontology (for example ICD10) - it will define the missing codes for you and print how many are they? They are also stored in a different dictionary, so they will be easily located, what codes are missing. If it's too much, you can consider updating the ontology dictionaries.
Function inputs:

- cfg - Configuration object with "work_dir" that points to workdir path + "dict_folder" that points to path with the Generic medial vocabularies - for example "MR_Tools/DictUtils/Ontologies/RX/dicts"
    - work_dir points to path that includes those subfolders:
        - FinalSignals - With Prepared signals to load - input path for reading the signals
        - rep_configs/dicts - where we are going to store dictionaries for loading process. The output path of this function
    - dict_folder - base path for searching dicts. You can pass it as empty string '' - But than you will need to specify full paths in def_dicts, sets_dicts
- def_dicts - list of dictionaries names that are located under dict_folder . Contains "DEF" commands
- set_dicts - list of dictionaries names that are located under dict_folder. Contains "SET" commands. We currently support Vocabulary dictionaries that has only "DEF" commands and "SET" command and you need to separate them, to use that tool. Till now the dicts are separated, so there is no concern.
- signal - name of the signal
- data_files_prefix - name of the data file in FinalSignals that needs to be scanned for codes. Mainly we name the file as the name of the signal it contains, so it will be many times the same as signal
- header - the header of the datafile - since FinalSignals doesn't contains headers
- to_use_list - list of columns from "header" that contains our codes for merging with the known dicts from "def_dict + set_dicts"
 
Example usage of diagnosis loading in Optum - it contains additional 2 categorical columns:
```python
def_dicts=['dict.icd9dx', 'dict.icd10']
set_dicts=['dict.set_icd9dx', 'dict.set_icd10', 'dict.set_icd9_2_icd10']
header=['pid','signal' ,'diag_date', 'diagnosis_code', 'diagnosis_status', 'diag_source']
categorical_cols=['diagnosis_code', 'diagnosis_status', 'diag_source']
create_dict_generic(cfg, def_dicts, set_dicts, 'DIAGNOSIS', 'DIAGNOSIS', header, categorical_cols)
```
 
Additional function for internal dicts is generate_dict_from_codes. Function inputs:

- map_df - path or dataframe with 2 columns, first column is the codes, the second column is description. 
- outpath - where to store output dictionary
- min_code - from which code number to start the DEF
This function construct dict with 2 rows for each code - the first is the "code" and the second row is the description.
For example, we might pass "ATC_XYZ \t description" - it will generate "DEF 1 ATC_XYZ" and "DEF 1 description". 
 
 
