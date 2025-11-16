
/home/Repositories/MHS/build_Feb2016_Mode_3/maccabi.repository 

```
/home/Repositories/MHS/RepProcessed/static/ BYEAR.tsv GENDER.tsv /home/Repositories/MHS/RepProcessed/dynamic/ Hemoglobin.tsv ... (rest of the signals) 
```

```
/home/Repositories/MHS/RepProcessed/static/ /home/Repositories/MHS/RepProcessed/dynamic/
/nas1/Work/Users/Ilya/Repositories/MHS/RepProcessed/static
/nas1/Work/Users/Ilya/Repositories/MHS/RepProcessed/dynamic
```

```
 /home/Repositories/MHS/RepProcessed/dynamic.feather /home/Repositories/MHS/RepProcessed/static.feather 
/nas1/Work/Users/Ilya/Repositories/MHS/RepProcessed/dynamic.feather
/nas1/Work/Users/Ilya/Repositories/MHS/RepProcessed/static.feather
```
### Training data preparation
#### Convert into the Raindrop input format
M12data_Large/process_scripts/LoadMaccabi.py

```
Repository data 
    /home/Repositories/MHS/RepProcessed/dynamic.feather
    /home/Repositories/MHS/RepProcessed/static.feather
Samples 
    /server/Work/Users/Ilya/LGI/outputs.MHS/Samples.no_exclusions/train.730.1_per_control.samples
NOTE:   
    These are the train samples used by the CRC model
```

```
/home/Ilya/Raindrop/M12data_Large/processed_data/arr_outcomes.npy
/home/Ilya/Raindrop/M12data_Large/processed_data/PTdict_list.npy
/home/Ilya/Raindrop/M12data_Large/processed_data/subsampled_df.pickle
NOTE:   
    Here "subsampled_df.pickle" contains data from the .samples file
```
#### Convert absolute time into days, clean zero-length entries
Convert absolute time into days since 20010101 and remove pids which do not have associated dynamic data TRAINING dataset

```
20221103_Fix_Train_FromScratch.ipynb
```

```
/home/Ilya/Raindrop/M12data_Large/processed_data/
    PTdict_list.npy
    arr_outcomes.npy
    subsampled_df.pickle
```

```
/home/Ilya/Raindrop/LargeTrain/processed_data/
    PTdict_list.npy
    arr_outcomes.npy
    subsampled_df.pickle
```
### Switch from absolute to relative time (wr.t. sample date)
[http://node-05:9000/notebooks/ilya-internal/20221213_RelativeTimePlusOne.ipynb](http://node-05:9000/notebooks/ilya-internal/20221213_RelativeTimePlusOne.ipynb)

```
/home/Ilya/Raindrop/LargeTrain/processed_data/
```

```
/home/Ilya/Raindrop/LargeTrainRelative/
```
### Add offset 1 to the relative time (to avoid 0 being interpreted as missing data)
```
/home/Ilya/Raindrop/LargeTrainRelative/
```

```
/home/Ilya/Raindrop/LargeTrainRelativePlusOne/
```
### Testing data preparation
#### Reducing to a single cohort
We started from applying the Raindrop model to 
 the WHOLE Test set, see

```
/nas1/UsersData/ilya-internal/PycharmProjects/Raindrop-main/M12data_LargeTest/bootstrap_raindbow_model.sh
```
However, applying the model to the whole test set 
 resulted in high memory consumption (about 100GB had to be allocated)
 Since we are mainly interested in the performance on one specific cohort: 
 "MULTI Time-Window:0,365 Age:40,89", we decided to restrict the test set to this cohort only.
 The Test365 samples file was prepared as follows:

```
1)     Create file "M12data_LargeTest/bootstrap/rainbow.crc.Raw"
    using following command
    [see M12data_LargeTest/bootstrap_rainbow_model.sh]
    bootstrap_app \
    --use_censor 0 \
    --rep /home/Repositories/MHS/build_Feb2016_Mode_3/maccabi.repository \
    --input ${RUN_PATH_FULL_LEAN}/bootstrap/rainbow.crc.preds \
    --output ${RUN_PATH_FULL_LEAN}/bootstrap/rainbow.crc \
    --cohort "${COHORT}" \
    --working_points_pr 1,3,5,7,10,15,20,25,30,35,40,45,50,55,60,65,70,80,90,95,99 \
    --working_points_fpr 1,3,5,7,10,15,20,25,30,35,40,45,50,55,60,65,70,80,90,95,99 \
    --working_points_sens 75,80,85,90,95,97,99 \
    --output_raw
    Input:  /nas1/UsersData/ilya-internal/PycharmProjects/Raindrop-main/M12data_LargeTest/bootstrap/rainbow.crc.preds
    Output:  /nas1/UsersData/ilya-internal/PycharmProjects/Raindrop-main/M12data_LargeTest/bootstrap/rainbow.crc.Raw
2)    Take "rainbow.crc.Raw" as an input and run notebook 20221023_ExtractTestCohort.ipynb to
    create cohort in "samples" file format.
    Code:   http://node-05:9000/notebooks/ilya-internal/20221023_ExtractTestCohort.ipynb
    Input:  M12data_LargeTest/bootstrap/rainbow.crc.Raw 
    Output: M12data_LargeTest/test_cohorts/test_365.samples
```
#### Convert Test365 samples into the Raindrop input format
M12data_LargeTest365/LoadMaccabiTest.py

```
M12data_LargeTest/test_cohorts/test_365.samples
RepProcessed/dynamic.feather 
RepProcessed/static.feather
```

```
M12data_LargeTest365/processed_data/subsampled_df.pickle [contain (probably subsampled) input data]
M12data_LargeTest365/processed_data/PTdict_list.npy
M12data_LargeTest365/processed_data/arr_outcomes.npy
```
#### Convert absolute time into days, clean zero-length entries
Convert absolute time into days since 20010101 and remove pids which do not have associated dynamic data TRAINING dataset

```
20221103_Fix_Test365_FromScratch.ipynb
```

```
 /nas1/UsersData/ilya-internal/PycharmProjects/Raindrop-main/M12data_LargeTest365/processed_data/
```
```
/home/Ilya/Raindrop/LargeTest365/processed_data/
    PTdict_list.npy
    arr_outcomes.npy
    subsampled_df.pickle
```
#### Switch from absolute to relative time (wr.t. sample date)
[http://node-05:9000/notebooks/ilya-internal/20221213_RelativeTimePlusOne.ipynb](http://node-05:9000/notebooks/ilya-internal/20221213_RelativeTimePlusOne.ipynb)

```
/home/Ilya/Raindrop/LargeTest365/processed_data/
```

```
/home/Ilya/Raindrop/LargeTest365Relative/
```
### Modifications applied to the Raindrop code
Original Raindrop code is not well-suited for experimentation 
 for following reasons:

- Raindrop.py contains code specific to handling different datasets.
- Training and testing are done in the same loop
- In order to get a confidence interval for AUC authors train models for five different splits, rather than using Bootstrap
- Many configuration parameters are hardcoded
We made following modifications to the code:

- Strip Raindrop.py of the code not relevant to MHS
- Implement MHS processing based on the code handling Physionet 2012 (denoted P12 in the code). We will denote the code specific to MHS dataset as M12.
- Split the code into RaindropTrain.py and RaindropTest.py
- Add command-line parameters that allow setting configuration parameters from the command line
- Implement model evaluation using Bootstrap, in order to be consistent with the SOTA model evaluation approach.
New files:

- RaindropTrain.py
- RaindropTest.py
Obsoleted files:
- Raindrop.py

### Model evaluation
After the model is applied to the test data during the call to RaindropTest.py we convert predictions into a format expected by the Medial's bootstrap_app.
 The script that implements this conversion is called BootstrapPrepare.py
 Code:

```
code/BootstrapPrepare.py
```
### Script infrastructure for fast experimentation
In order to be able to run experiments fast while logging all the necessary information for retrospective analysis,
 we implemented a folder template which contains all or some of following files:
 train_test_bootstrap.sh this file trains a model, applies it to the test set and then computes AUC with confidence interval using bootstrap_app
 log.txt this file contains logs of the ./train_test_bootstrap.sh invokation
### Experiments
#### LargeRelativeAfterTrainFix/

```
Train model on RELATIVE TIME.
The "fix" mentioned in the folder name is that we make sure relative time is never zero by adding 1. This is necessary since 0 is interpreted as a missing value by the Raindrop code.
AUC     0.829[0.814 - 0.843]
NOTE:
    We also applied model to the test data after EACH epoch
    to see the dynamics of the AUC as a function of epoch.
```
#### LargeRelative_D_OB_16/

```
Based on LargeRelativeAfterTrainFix/
but this time we increase dimension of the observation embedding to
Status:
    There's no performance improvement as compared to D_OB=4
    AUC     0.828[0.811 - 0.842]
```
#### LargeRelative_nlayers_4/

```
Increase the number of TransformerEncoder layers from 2 to 4.
Status:
    There's no performance improvement as compared to 2 layers
    AUC     0.825[0.812 - 0.839]
```
#### LargeMatchedFull/

```
Train classifier based on FULL matching data
We first converted FULL matched data into Relative format
using 20221218_PrepareFullMatched_Data_RelativeTime.ipynb,
the resulting data written to
/home/Ilya/Raindrop/LargeTrainMatchedRelative/
Status:
    AUC     0.814[0.799 - 0.828]
    Performance of the model trained on the matched data 
    is degraded, as compared to the model trained on the unmatched
    data (AUC     0.829[0.814 - 0.843])
```
### TODO
#### Increase dimensionality of the positional embedding
This will increase the time resolution of Raindrop
#### Use inverted time series + collect output of the first position in TraonsformerEncoder (same way it is done when using BERT for classification)
This may help the network focus on the latest observation
#### Train network on data where missing values were fixed using ad-hoc algoritm
Since "observation propagation" stage of the Raindrop algorithm turn out to be degenerate, this may improve the performance
#### Disable observation-propagation stage at all
Since "observation propagation" stage of the Raindrop algorithm turn out to be degenerate, we expect almost no performance degradation here
### Summary
```
Performance of the Raindrop model (AUC 0.829) is significantly below the performance of SOTA CRC model.
```
 
 
