# Fit MedModel to Repository
Under [**Flow** ](/Medial%20Tools/Using%20the%20Flow%20App)options called "f**it_model_to_rep**". Flow --fit_model_to_rep (...OTHER ARGUMENTS, full list of arguments can be shown by Flow --help_ fit_model_to_rep)****
# ****
The goal is to receive as input: repository path + model path and output new adjusted model for the repository in given output path.
## ****
1. In some case we made some rename changes in the signal. GENDER <=> SEX, DIAGNOSIS <=> ICD9_Diagnosis, RC. That is unfortunate, but that's life, and some changes break things. 
2. In some cases, there are signals that do not exist in the repository and are used by the model. The model tries to retrieve them and fails. One option is to change this behavior and just treat those signals as empty for all patients, but I prefer our tools will be stricter to eliminate problems in production. In the past, we have created repository with empty signals. This is bad and confusion solution, since you might think that you have some signal in specific repository, but actually you don't. Another problem is that you might try to use a different model in the future with different missing signals and then you will need to create those empty signals in the repository so it's still manual work. 
## ****
1. The tool reads the model and repository and check which signals the model needs do not exists in the repository
2. For each non exists signal in the repository it tries to solve the problem by adding rep_proccessor (or removing) to the model, by this priority
3. Checks for all categorical codes that the model uses - it validates all the codes are known in the repository
4. Store the adjusted model
5. prints to file or screen (if no output log file is provided) what transformation were done in the model to fit it the repository
6. prints to file or screen (if no other additional output log file is provided) what codes were missing for each signal
7. Bottom line, if all is OK (all codes are known, so the log file of missing codes is empty) and all the adjustments in the model were done without any problems.
## ****
 
```bash
Flow --fit_model_to_rep  --f_model /nas1/Work/Users/Eitan/Lung/outputs/models2023/EX3/model_63/config_params/exported_full_model.final.medmdl --rep /nas1/Work/CancerData/Repositories/THIN/thin_2021.lung2/thin.repository --f_output /tmp/1.mdl --log_action_file_path /tmp/actions.log  --log_missing_categories_path /tmp/categ.log --cleaner_verbose -1 --allow_virtual_rep 0
```
 
I took LungFlag model (--f_model) and tried it on THIN (--rep) and stored the output in (--f_output). All the other arguments are less important, but I will explain them:
- log_action_file_path  - log output to list all changes we made in the model. If not given the output will be printed to screen
- log_missing_categories_path - log output to list all missing codes for signals. If not given the output will be printed to screen
- cleaner_verbose - a flag that controls the "verbosity" of outliers reporting. For production, we want to turn the verbosity on and pass "1", for our usage in validation we want to turn this off (faster and less memory consumption run) by passing "-1". This is useful since all official AlgoMarkers have verbosity turned on for cleaners and you want to turn this off in validation
- allow_virtual_rep - If we want to use "empty/virtual" repository definition like we have in AlgoMarker without data to test our "fit" to apply the model. It will limit the adjustment in case we need to inspect the data from the repository (currently only if there is BUN<=>Urea conversion, it will fail)
## ****
```
Signal BUN, medial value is 34.200001 in repository
write_to_file [/tmp/1.mdl] with crc32 [273944850]
read_binary_data_alloc [/tmp/1.mdl] with crc32 [273944850]
read_from_file [/tmp/1.mdl] with crc32 [273944850] and size [193041186]
catgorical signal ICD9_Diagnosis is OK
catgorical signal Smoking_Status is OK
All categorical signals are OK!
All OK - Model can be applied on repository
```
 As you can see it finds the model uses Urea and repository has BUN. The median value of BUN is 34.2 in the repository. It writes the adjusted model to the output file and then read it again to test it "works".Then you can see in bottom line "All OK - Model can be applied on repository", a row above that specify that all categorical signals are ok, and you can see above this for each categorical signal if all values are OK.The file "/tmp/categ.log" will be empty, since all codes exists in the repository. If some codes were missing it will write it in file tab delimited name of signal and the missing categorical value. $> cat  /tmp/actions.log #will output: 
```
REMOVED_RENAME_FROM_TO  SEX     GENDER
CONVERT_SIGNAL_TO_FROM_FACTOR   Urea    BUN     0.467290
EMPTY_SIGNAL    RDW
```
 Which means the model uses "SEX" (but by adding rep_processor that converts GENDER to SEX for production) and we have "GENDER" in the repository.  It will remove this reo_processor and the model will expect GENDER.The 2 line shows that we added a virtual signal Urea based on BUN (what we have in the repository) by multipling it by 0.467290The 3 row shows that THIN doesn't have RDW, so we added empty virtual signal to the model that we can apply the model.
