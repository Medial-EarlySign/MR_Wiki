# Embeddings WalkThrough Example
In this example we will first create an unsupervised embedding space, and then use it as features for predicting the first CVD MI.
All work done here can be found in: /nas1/Work/Users/Avi/test_problems/embedding_example
The code needed for this is either in MR_LIBS or in MR/Projects/Shared/Embeddings.
Quick Jump:
- [Step 1 : Plan](../#EmbeddingsWalkThroughExample-Step1)
- [Step 2: Prepare basic lists , and cohort](../#EmbeddingsWalkThroughExample-Step2)
- [Step 3 : Design and prepare the training dates for embeddings](../#EmbeddingsWalkThroughExample-Step3)
- [Step 4 : Prepare the embed_params files for x and y](../#EmbeddingsWalkThroughExample-Step4)
- [Step 5: Create the x and y matrices](../#EmbeddingsWalkThroughExample-Step5)[Step5](../#EmbeddingsWalkThroughExample-Step5)
- [Step 6: Train the embedding using Keras](../#EmbeddingsWalkThroughExample-Step6)
- [Step 7 : Testing we get the same embeddings in Keras and Infrastructure](../#EmbeddingsWalkThroughExample-Step7)
- [Step 8 : Using Embedding In a MedModel](../#EmbeddingsWalkThroughExample-Step8)
- [Step 9 : Results for MI with/without Embedding , with/without SigDep](../#EmbeddingsWalkThroughExample-Step9)
 
## Step 1 : Plan
Our plan is to use the CVD_MI registry, then use TRAIN=1 group for training/cross validation , and TRAIN=2 group for actual validation.
We will need to sacrifice some data in order to train our embedding. We do it simply by splitting the TRAIN=1 group into two random groups: 1A and 1B , 1A will be used in training our embedding, 1B will be used in training our model.
We will give scores at random times before the outcome (and slice with bootstrap later), say one random sample every 180 days. We will also make sure our samples have at least a BP or LDL or Glucose reading at least 3 years before the sample. This gives us the plan for the outcome training.
For the embedding training - we have lots of options, and it is not clear which is the best.
In this example we will choose the option of using the same dates and outcome times as in the outcome training group, generate a feature rich large x (source) matrix at the sample times, and a large (but smaller) destiny matrix y for the times (outcome [,](/pages/createpage.action?spaceKey=WIK&title=outcome+%2C+outcome%2BT&linkCreation=true&fromPageId=10911804) outcome + T) , T = 1y , which will also include our outcome variable. We will then use the embedded layer as features added to the CVD model and see if we see any improvement in perfomance.
General Vocabulary of terms we use:
- **sparse matrix** : a matrix in which most values are 0 , and hence can be defined by showing only the few non-zero elements. Very efficient in holding large sets of sparse categorial features. We use the MedSparseMat class to handle these objects. Usually we create such matrices with a prefix followed by a suffix :
  - **.smat** : the actual sparse matrix, lines of <line_number>,<column number>,<value>
  - **.meta** : containing the list of pid,time matching each line
  - **.dict** : a dictionary giving the names of the features in each column
  - **.scheme** : the serialized scheme file for this matrix. Allows recreating such matrices with the same rules/dictionaries on a different set of samples.
- **x,y matrices** - the marices we train the embedding on. The embedding will start from the (sparse) features in x[i] vector run through a network of several layers, one of which is the embedding layer, and end up in the y[i] (sparse) vector.
- **embed_params** : a file containing the parameters (init_from_string format) defining how to generate a sparse matrix, for example which categorial signals to use, on which sets in which time windows, etc.
- **scheme file** : a serialized EmbedMatCreator object (from MedEmbed.h) , containing a ready to use object that can be deserialized and used to generate sparse matrices using a predefined set of rules that was learnt.
- **layers file** : a file containing a keras embedding model in a format we can read and use in our infrastructure.
- **outcome training** : the process of training the actual model for the outcome (in this example cvd_mi)
- **embedding training** : the process of preparing the x,y matrices, the scheme files, train a deep learning embedding model in keras, and get the layers file. Scheme and layer files will later be used as a feature generator in the infrastructure.
## Step 2: Prepare basic lists , and cohort
```bash
# creating a cohort file for cvd_mi : first verified mi, censoring cases with other mi's before , and cases with no BP or Glucose or LDL tests
 
/nas1/UsersData/avi/MR/Projects/Shared/Embeddings/Linux/Release/Embeddings --build_example
 
# creating samples for training/testing for TRAIN=1 and TRAIN=2
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --cohort_fname ./cvd_mi.cohort --cohort_sampling "min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=1;min_age=35;max_age=90;min_year=2004;max_year=2017;max_samples_per_id=4" --out_samples ./train_1.samples
 
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --cohort_fname ./cvd_mi.cohort --cohort_sampling "min_control=1;max_control=10;min_case=0;max_case=2;jump_days=180;train_mask=2;min_age=35;max_age=90;min_year=2004;max_year=2017;max_samples_per_id=4" --out_samples ./train_2.samples
 
 
# now filter and match on train_1 samples : making sure samples have needed information, and raising the case to control ratio in learning set
# on the validation set we only apply the filter for needed information
# generate validate_1 validate_2 subsets
 
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --filter_and_match --in_samples ./train_1.samples --out_samples ./validate_1.samples --filter_params "min_sample_time=20040101;max_sample_time=20160101;bfilter=sig_name,BP,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,Glucose,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,LDL,win_from,0,win_to,730,min_Nvals,1;min_bfilter=1"
 
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --filter_and_match --in_samples ./train_2.samples --out_samples ./validate_2.samples --filter_params "min_sample_time=20040101;max_sample_time=20160101;bfilter=sig_name,BP,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,Glucose,win_from,0,win_to,730,min_Nvals,1;bfilter=sig,LDL,win_from,0,win_to,730,min_Nvals,1;min_bfilter=1"
 
# generate learn_1 matched subset and subsamples to 10x
 Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --filter_and_match --in_samples ./validate_1.samples --out_samples ./learn_1.samples --match_params "priceRatio=200;maxRatio=10;verbose=1;strata=time,year,1"
 
# prepare pids groupA (for embedding) and groupB (for model)
less validate_1.samples | awk '(NR>1){print $2}' | uniq | awk '{print $1, 1+(rand()<0.5)}' > train_pids_groups
less train_pids_groups | awk '($2==1){print $1}' > pids_group_A
less train_pids_groups | awk '($2==2){print $1}' > pids_group_B
# prepare validate_1_A , validate_1_B , learn_1_A , learn_1_B
intersect.pl validate_1.samples 1 pids_group_A 0 > validate_1_A.samples
intersect.pl validate_1.samples 1 pids_group_B 0 > validate_1_B.samples
intersect.pl learn_1.samples 1 pids_group_A 0 > learn_1_A.samples
intersect.pl learn_1.samples 1 pids_group_B 0 > learn_1_B.samples
```
 
We now intend to use validate_1_A.samples or learn_1_A.samples to design an embedding training, and then use learn_1_B.samples to train a predictor for cvd_mi, once without embeddings signals, and once with, and compare the results (on validate_2_B in CV, and eventually on validate_2).
## Step 3 : Design and prepare the training dates for embeddings
To train the embedding we need:
1. x matrix , at some points in time, could be random points, or points similar to how we choose validation or learning samples. We will use the pid, time of validate_1_A.samples for that (~1.6M points, ~660K patients)
2. y matrix : lots of options:
  
1. take y to be x : this is exactly learning an autoencoder.
2. simply take the y time to be x time + some translation t from a set T of optional time translations:
    
1. T = {0} (semi-autoencoder) , T={365} (one year forward) , T={730} (two years forward) , T={-365} (one year backwards) etc... 
2. T={0,365,730} , all options or random choice of one for each sample.
We will use two options: semi-autoencoder (T for y is 0), and option 2b , and randomly set the y time to be 1y or 2y ahead from the sampling point.
We keep that in a samples file where the time is the time for x and the outcomeTime is the time for y. Our code later supports this.
```bash
# preparing embedding_1_A.samples (using awk this time)
# we could have started from learn_1_A samples, but decided to be more general and use lots of data, hence starting from validate_1_A
 
less validate_1_A.samples | awk '(/EVENT/){print}(/SAMPLE/){a=1+(rand()>0.5);a=a*10000;print "SAMPLE\t"$2"\t"$3"\t"$4"\t"$3+a"\t"$6}' > embedding_1_A.samples
```
 
## Step 4 : Prepare the embed_params files for x and y
The embed_params file holds all the parameters needed in order to create a sparse matrix for an embedding.
For categorial signals we can choose the sets we are interested in (could be a very large number), and a few more settings such as time windows, if to keep as counts, if to shrink, etc.
For continous signals we can choose the ranges we are interested in.
We can also use a MedModel generated before from a json file and add the features it creates (this option is still in dev/testing)
We could use the same embed_params for x and y matrices, but to make things interesting we will use different plans for the x and y matrices.
some preparations:
```bash
# preparing the list of read codes we'll use to generate features (that's ~97K features !)
less /home/Repositories/THIN/thin_jun2017/dict.read_codes | awk '(/DEF/ && substr($3,0,2)=="G_"){print $3}' > rc.codes

# preparing the list of atc codes we'll use to generate features (~6k features)
less /home/Repositories/THIN/thin_jun2017/dict.drugs_defs | awk '(/DEF/ && substr($3,0,4)=="ATC_"){print $3}' | grep -v ":" > atc.codes
```
 
 
x_embed_params :
```ini
sigs={
# sigs are sig=<> format with | between sigs
# dummy signal is needed to make sure there's at least one entry for each line , helps in matching x,y lines
sig=dummy;type=dummy|
# age category with a binning to 10 groups
sig=BYEAR;type=age;ranges=0,10,20,30,40,50,60,70,80,90,1000;do_shrink=0|
# gender with 2 categories
sig=GENDER;type=continuous;ranges=1,2,3;do_shrink=0|
# RC signals : categorial , use rc.codes list as categories, look at a large (ever) time window, use hierarchy and count each category used
sig=RC;type=categorial;categories=list:rc.codes;win_from=0;win_to=36500;add_hierarchy=1;do_counts=1|
# RC signals : categorial same as previous but for a short (1y) time window
sig=RC;type=categorial;categories=list:rc.codes;win_from=0;win_to=365;add_hierarchy=1;do_counts=1|
# Drug signals , last 2 years
sig=Drug;type=categorial;categories=list:atc.codes;win_from=0;win_to=730;add_hierarchy=1;do_counts=1|
# Adding LDL distribution to bins in last 5 years
sig=LDL;type=continuous;ranges=0,50,70,100,120,150,200,300,10000;do_shrink=0;win_from=0;win_to=1800;do_counts=1|
# Adding Glucose distribution to bins in last 5 years
sig=Glucose;type=continuous;ranges=0,50,70,90,100,110,125,150,200,10000;do_shrink=0;win_from=0;win_to=1800;do_counts=1|
# Adding HbA1C distribution to bins in last 5 years
sig=HbA1C;type=continuous;ranges=0,4.0,5.0,5.7,6.0,6.5,7.0,8.0,10.0,10000;do_shrink=0;win_from=0;win_to=1800|
# Adding Cretinine distribution to bins in last 5 years
sig=Creatinine;type=continuous;ranges=0,0.5,0.8,1.0,1.2,1.5,2.0,3.0,4.0,10000;do_shrink=0;win_from=0;win_to=1800|
# Adding BP distribution to bins in last 5 years
sig=BP;type=continuous;val_chan=0;ranges=0,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,10000;do_shrink=0;win_from=0;win_to=1800|
sig=BP;type=continuous;val_chan=1;ranges=0,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,10000;do_shrink=0;win_from=0;win_to=1800
};
```
 
y_embed params: preferring do_counts=0 as easier to build loss function for.
```ini
sigs={
# sigs are sig=<> format with | between sigs
# dummy signal is needed to make sure there's at least one entry for each line , helps in matching x,y lines
sig=dummy;type=dummy|
# age category with a binning to 10 groups
sig=BYEAR;type=age;ranges=0,10,20,30,40,50,60,70,80,90,1000;do_shrink=0|
# gender with 2 categories
sig=GENDER;type=continuous;ranges=1,2,3;do_shrink=0|
# RC signals : categorial same as previous but for a short (1y) time window
sig=RC;type=categorial;categories=list:rc.codes;win_from=0;win_to=365;add_hierarchy=1;do_counts=0|
# Drug signals , last 2 years
sig=Drug;type=categorial;categories=list:atc.codes;win_from=0;win_to=365;add_hierarchy=1;do_counts=0|
# Adding LDL distribution to bins in last year
sig=LDL;type=continuous;ranges=0,50,70,100,120,150,200,300,10000;do_shrink=0;win_from=0;win_to=365;do_counts=0|
# Adding Glucose distribution to bins in last year
sig=Glucose;type=continuous;ranges=0,50,70,90,100,110,125,150,200,10000;do_shrink=0;win_from=0;win_to=365;do_counts=0|
# Adding HbA1C distribution to bins in last year
sig=HbA1C;type=continuous;ranges=0,4.0,5.0,5.7,6.0,6.5,7.0,8.0,10.0,10000;do_shrink=0;win_from=0;win_to=365;do_counts=0|
# Adding Past/Future Registries: past, 1y ahead, 5y ahead
# In y matrices it is perfectly OK to peek into the future (!) we only use them for training
sig=CVD_MI;type=categorial;categories=CVD_MI_Confirmed_Event,CVD_MI_Untimed_Event,CVD_MI_History;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=CVD_MI;type=categorial;categories=CVD_MI_Confirmed_Event,CVD_MI_Untimed_Event,CVD_MI_History;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_MI;type=categorial;categories=CVD_MI_Confirmed_Event,CVD_MI_Untimed_Event,CVD_MI_History;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_IschemicStroke;type=categorial;categories=CVD_IschemicStroke_Confirmed_Event,CVD_IschemicStroke_Untimed_Event,CVD_IschemicStroke_History;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=CVD_IschemicStroke;type=categorial;categories=CVD_IschemicStroke_Confirmed_Event,CVD_IschemicStroke_Untimed_Event,CVD_IschemicStroke_History;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_IschemicStroke;type=categorial;categories=CVD_IschemicStroke_Confirmed_Event,CVD_IschemicStroke_Untimed_Event,CVD_IschemicStroke_History;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_HemorhagicStroke;type=categorial;categories=CVD_HemorhagicStroke_Confirmed_Event,CVD_HemorhagicStroke_Untimed_Event,CVD_HemorhagicStroke_History;win_from=0;win_to=0;do_counts=10000;do_shrink=0|
sig=CVD_HemorhagicStroke;type=categorial;categories=CVD_HemorhagicStroke_Confirmed_Event,CVD_HemorhagicStroke_Untimed_Event,CVD_HemorhagicStroke_History;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_HemorhagicStroke;type=categorial;categories=CVD_HemorhagicStroke_Confirmed_Event,CVD_HemorhagicStroke_Untimed_Event,CVD_HemorhagicStroke_History;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_HeartFailure;type=categorial;categories=CVD_HeartFailure_First_Indication;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=CVD_HeartFailure;type=categorial;categories=CVD_HeartFailure_First_Indication;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=CVD_HeartFailure;type=categorial;categories=CVD_HeartFailure_First_Indication;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=CKD_State;type=categorial;categories=CKD_State_Normal,CKD_State_Level_1,CKD_State_Level_2,CKD_State_Level_3,CKD_State_Level_4;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=CKD_State;type=categorial;categories=CKD_State_Normal,CKD_State_Level_1,CKD_State_Level_2,CKD_State_Level_3,CKD_State_Level_4;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=CKD_State;type=categorial;categories=CKD_State_Normal,CKD_State_Level_1,CKD_State_Level_2,CKD_State_Level_3,CKD_State_Level_4;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=DM_Registry;type=categorial;categories=DM_Registry_Pre_diabetic,DM_Registry_Diabetic;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=DM_Registry;type=categorial;categories=DM_Registry_Pre_diabetic,DM_Registry_Diabetic;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=DM_Registry;type=categorial;categories=DM_Registry_Pre_diabetic,DM_Registry_Diabetic;win_from=-1825;win_to=0;do_counts=0;do_shrink=0|
sig=HT_Registry;type=categorial;categories=HT_Registry_Hypertensive;win_from=0;win_to=10000;do_counts=0;do_shrink=0|
sig=HT_Registry;type=categorial;categories=HT_Registry_Hypertensive;win_from=-365;win_to=0;do_counts=0;do_shrink=0|
sig=HT_Registry;type=categorial;categories=HT_Registry_Hypertensive;win_from=-1825;win_to=0;do_counts=0;do_shrink=0
};
```
 
## Step 5: Create the x and y matrices
Finally we are ready for this stage. We will start with our samples file, and create 2 matrices from it, the x will use time, the y will use outcomeTime. The matrices will use the embed rules we defined in the previous step, and we will also shrink them to only contain values that appear at least 1e-3 of the samples (to have roughly at least ~1000 cases of it appearing), and less than 0.75 of the samples , to screen to frequent or too rare columns.
Our samples file is the one we prepared before: embedding_1_A.samples (1.6M training points)
To actually create the matrices we use the Embeddings project, with the --gen_mat option.
```bash
# command line to create x matrix
Embeddings --gen_mat --rep <rep> --f_samples ./embedding_1_A.samples --embed "pFile=x_embed_params" --min_p 0.001 --max_p 0.75 --prefix x
 
# files created (ls -l) :
-rwxrwxrwx 1 root root 6521109879 Feb 13 17:58 x.smat			<---- the sparse matrix. And yes, that is a 6.5GB matrix....
-rwxrwxrwx 1 root root   40597062 Feb 13 18:00 x.meta			<---- pid,time for each line (same number of lines as in our samples file)
-rwxrwxrwx 1 root root    1892057 Feb 13 18:00 x.scheme			<---- our serialized x scheme file for this matrix : we will need it when we later create features within a model !
-rwxrwxrwx 1 root root    1256521 Feb 13 18:00 x.dict			<---- the names of all the columns in the shrunk matrix
# and now creating the y matrix
Embeddings --gen_mat --rep <rep> --f_samples ./embedding_1_A.samples --embed "pFile=./y_embed_params" --min_p 0.001 --max_p 0.75 --prefix y
```
 
## Step 6: Train the embedding using Keras
We are now at a state in which we have our x & y matrices ready. Our goal now is to calculate a deep learning model starting from x[i] and ending in y[i], while flowing through a narrow layer with few (say 100-200) neurons. 
To do that use the Embedder.py script, or copy it and change what you need inside. The Embedder.py script allows the following:
1. Train through 3 layers (last is the embedding) 
2. Train through 5 simetric layers with the middle as the embedding layer.
3. Control parameters of network:
  
1. layers sizes
  
2. l1, l2, dropout regularizers on each layer
3. control of extra weight given to cases in the loss function
4. control leaky ReLU function parameters
5. control noise added to embedding layer in training
6. control number of epochs in training, also allow to continue training of a saved model.
7. savind model in a way that can be later used in the infrastructure (.layers file)
8. test modes to generate predictions/embedding layer results on a set of examples (to allow testing vs. the infrastructure)
The Embedder.py script is in the git in .../MR/Projects/Shared/Embeddings/scripts/
 
```bash
# example run training a model
python ./Embedder.py --xfile ./x.smat --yfile ./y.smat --nepochs 5 --dim 400 200 100 --l1 1e-7 0 0 --out_model emodel --train --wgt 10 --dropout 0.0 0.0 0.0 --noise 0.3 --gpu 1 --full_decode
 
# output explained ... : (# lines added to explain)
Using TensorFlow backend.
# full parameter list
('arguments---->', Namespace(dim=[400, 200, 100], dropout=[0.0, 0.0, 0.0], embed=False, full_decode=True, gpu=[1], in_model='', l1=[1e-07, 0.0, 0.0], l2=[0.0, 0.0, 0.0], leaky=[0.1], nepochs=[5], no_shuffle=False, noise=[0.3], out_model=['emodel'], test=False, train=True, wgt=[10.0], xdim=-1, xfile=['./x.smat'], ydim=-1, yfile=['./y.smat']))
# using only gpu 1 , not setting this will allow running on all gpus in parallel, or on another (say gpu 0)
using gpu  1
Train mode
# reading input matrices (can be quite slow, as matrices can be huge)
('reading: ', ['./x.smat'], ['./y.smat'])
reading csv file:  ./x.smat 13:11:18.800850
preparing sparse mat 13:14:27.758752
reading csv file:  ./y.smat 13:14:40.032091
preparing sparse mat 13:15:34.727952
# printing some basic info on sparse matrices x,y : note for example the ratio of 0 to non 0 in x is 43.1 and in y 48.08 (!), showing how sparse they are.
('xtrain : ', (1623366, 11933), <1623366x11933 sparse matrix of type '<type 'numpy.float32'>'
        with 451035611 stored elements in Compressed Sparse Row format>, 'non zero: ', 449412245, 43.10435840038137)
('ytrain : ', (1623366, 3986), <1623366x3986 sparse matrix of type '<type 'numpy.float32'>'
        with 136188699 stored elements in Compressed Sparse Row format>, ' non zero: ', 134565333, 48.08621010881012)
('ORIGDIM----> ', 11933, 3986, -1, -1)
# and now the actual training results
Running model definition
10.0
10.0
Training on xtrain
Train on 1298692 samples, validate on 324674 samples
Epoch 1/5
2019-02-20 13:15:51.200332: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-02-20 13:15:52.226714: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1212] Found device 0 with properties:
name: GeForce GTX 1080 Ti major: 6 minor: 1 memoryClockRate(GHz): 1.582
pciBusID: 0000:81:00.0
totalMemory: 10.92GiB freeMemory: 10.76GiB
2019-02-20 13:15:52.226779: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1312] Adding visible gpu devices: 0
2019-02-20 13:15:52.504954: I tensorflow/core/common_runtime/gpu/gpu_device.cc:993] Creating TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 10415 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1080 Ti, pci bus id: 0000:81:00.0, compute capability: 6.1)
# each epoch has a line , giving results on train and validation, the validation set is always the last 20% of the data.
# see below some more explaining on how to understand the measures and results printed.
1298692/1298692 [==============================] - 249s 192us/step - loss: 0.1734 - w_bin_cross: 0.1637 - espec: 0.0289 - enpv: 0.0039 - ppv: 0.3799 - sens: 0.8203 - val_loss: 0.1578 - val_w_bin_cross: 0.1476 - val_espec: 0.0232 - val_enpv: 0.0037 - val_ppv: 0.4295 - val_sens: 0.8253
Epoch 2/5
1298692/1298692 [==============================] - 302s 233us/step - loss: 0.1339 - w_bin_cross: 0.1238 - espec: 0.0240 - enpv: 0.0028 - ppv: 0.4370 - sens: 0.8735 - val_loss: 0.1362 - val_w_bin_cross: 0.1261 - val_espec: 0.0219 - val_enpv: 0.0030 - val_ppv: 0.4558 - val_sens: 0.8564
Epoch 3/5
1298692/1298692 [==============================] - 329s 253us/step - loss: 0.1221 - w_bin_cross: 0.1120 - espec: 0.0224 - enpv: 0.0024 - ppv: 0.4584 - sens: 0.8885 - val_loss: 0.1345 - val_w_bin_cross: 0.1245 - val_espec: 0.0214 - val_enpv: 0.0029 - val_ppv: 0.4626 - val_sens: 0.8640
# note epoch 4 started to climb back in val_loss ... this might be a sign for a need to better regularize the model, as it seems to start entering an overfit state
Epoch 4/5
1298692/1298692 [==============================] - 304s 234us/step - loss: 0.1156 - w_bin_cross: 0.1056 - espec: 0.0215 - enpv: 0.0023 - ppv: 0.4706 - sens: 0.8967 - val_loss: 0.1542 - val_w_bin_cross: 0.1442 - val_espec: 0.0306 - val_enpv: 0.0025 - val_ppv: 0.3752 - val_sens: 0.8867
# last epoch , seems val_loss started to go down again, so we got a better model at the end. Still loss is smaller than val_loss, showing a potential for better regularizing.
Epoch 5/5
 1298692/1298692 [==============================] - 333s 257us/step - loss: 0.1111 - w_bin_cross: 0.1011 - espec: 0.0209 - enpv: 0.0021 - ppv: 0.4798 - sens: 0.9024 - val_loss: 0.1213 - val_w_bin_cross: 0.1114 - val_espec: 0.0216 - val_enpv: 0.0024 - val_ppv: 0.4627 - val_sens: 0.8862
# now follows is the ending in which the output files are created 
 Writing model to files
('History: ', <keras.callbacks.History object at 0x6fa5690>, {'val_espec': [0.023174003757131564, 0.021862880609978624, 0.021418394041715545, 0.03055855377804435, 0.021563341807379736], 'val_w_bin_cross': [0.14756845901125903, 0.12613012184193115, 0.12453776885398905, 0.14417843291107432, 0.11137183862486143], 'val_sens': [0.8253292080568654, 0.8563854553455446, 0.8639981839122339, 0.8866606718251948, 0.8861758074101623], 'val_enpv': [0.0037238269219488115, 0.003042069682342851, 0.002891325553422261, 0.0024709458833944, 0.0024423540647124592], 'val_ppv': [0.4295036114702129, 0.4557987501766982, 0.4626011239199966, 0.3751608240688261, 0.4627356967393517], 'enpv': [0.003947158052682541, 0.0027687939362956364, 0.002437750546613879, 0.0022583779117050936, 0.002131666025525145], 'val_loss': [0.15775366971853721, 0.13624100354358956, 0.13452252385947847, 0.15421950637508852, 0.12133861386228599], 'ppv': [0.3798841048923378, 0.43695378672384044, 0.4583713526026837, 0.47056864791872133, 0.4798394423932855], 'w_bin_cross': [0.16372003288450798, 0.12379132172316154, 0.11200136639712739, 0.10560965182129696, 0.10111237579286037], 'sens': [0.8202563503519625, 0.8735020021500306, 0.8885229580472642, 0.8966689669803886, 0.9024332567701953], 'loss': [0.17342430566917966, 0.13392729285731664, 0.1220678161909718, 0.11563198370958765, 0.11113599371116904], 'espec': [0.028870824286393815, 0.02403844574438139, 0.02241259005779445, 0.021534086913695155, 0.020883613924218173]})
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         (None, 11933)             0
_________________________________________________________________
dropout_1 (Dropout)          (None, 11933)             0
_________________________________________________________________
dense_1 (Dense)              (None, 400)               4773600
_________________________________________________________________
leaky_re_lu_1 (LeakyReLU)    (None, 400)               0
_________________________________________________________________
dropout_2 (Dropout)          (None, 400)               0
_________________________________________________________________
dense_2 (Dense)              (None, 200)               80200
_________________________________________________________________
leaky_re_lu_2 (LeakyReLU)    (None, 200)               0
_________________________________________________________________
dropout_3 (Dropout)          (None, 200)               0
_________________________________________________________________
dense_3 (Dense)              (None, 100)               20100
_________________________________________________________________
leaky_re_lu_3 (LeakyReLU)    (None, 100)               0
_________________________________________________________________
batch_normalization_1 (Batch (None, 100)               400
_________________________________________________________________
gaussian_noise_1 (GaussianNo (None, 100)               0
_________________________________________________________________
dropout_4 (Dropout)          (None, 100)               0
_________________________________________________________________
dropout_5 (Dropout)          (None, 100)               0
_________________________________________________________________
dense_4 (Dense)              (None, 200)               20200
_________________________________________________________________
leaky_re_lu_4 (LeakyReLU)    (None, 200)               0
_________________________________________________________________
dropout_6 (Dropout)          (None, 200)               0
_________________________________________________________________
dense_5 (Dense)              (None, 400)               80400
_________________________________________________________________
dense_6 (Dense)              (None, 3986)              1598386
=================================================================
Total params: 6,573,286
Trainable params: 6,573,086
Non-trainable params: 200
_________________________________________________________________
Printing model layers
NLAYERS= 19
LAYER type=dropout;name=dropout_1;drop_rate=0.000000
LAYER type=dense;name=dense_1;activation=linear;in_dim=11933;out_dim=400;n_bias=400
LAYER type=leaky;name=leaky_re_lu_1;leaky_alpha=0.100000
LAYER type=dropout;name=dropout_2;drop_rate=0.000000
LAYER type=dense;name=dense_2;activation=linear;in_dim=400;out_dim=200;n_bias=200
LAYER type=leaky;name=leaky_re_lu_2;leaky_alpha=0.100000
LAYER type=dropout;name=dropout_3;drop_rate=0.000000
LAYER type=dense;name=dense_3;activation=linear;in_dim=200;out_dim=100;n_bias=100
LAYER type=leaky;name=leaky_re_lu_3;leaky_alpha=0.100000
LAYER type=batch_normalization;name=batch_normalization_1;dim=100
LAYER type=dropout;name=dropout_4;drop_rate=0.000000
LAYER type=dropout;name=dropout_5;drop_rate=0.000000
LAYER type=dense;name=dense_4;activation=linear;in_dim=100;out_dim=200;n_bias=200
LAYER type=leaky;name=leaky_re_lu_4;leaky_alpha=0.100000
LAYER type=dropout;name=dropout_6;drop_rate=0.000000
LAYER type=dense;name=dense_5;activation=linear;in_dim=200;out_dim=400;n_bias=400
LAYER type=dense;name=dense_6;activation=sigmoid;in_dim=400;out_dim=3986;n_bias=3986
# that's it !! we succesfully trained the model
# at the end these are the files created :
# file created by keras to contain the model structure
-rwxrwxrwx. 1 root root       6599 Feb 20 13:41 emodel.json
# the model parameters in keras bin format
-rwxrwxrwx. 1 root root   78938688 Feb 20 13:41 emodel.h5
# the model parameters in our simple .layers format that can be read using our infrastructure
-rwxrwxrwx. 1 root root   62422454 Feb 20 13:41 emodel.layers
# keeping the command line used to create the model : very useful and important if going to continue training or repeat it
-rwxrwxrwx. 1 root root        170 Feb 20 13:41 emodel_command_line.txt
# history of results on train and validation, can be used to draw charts of model training process
-rwxrwxrwx. 1 root root      35160 Feb 20 13:41 emodel.history
# you can pick up a model you trained and continue its training. Here we use the emodel trained before to continue and save into emodel2
# the model will initialize itself from the emodel.json and emodel.h5 files, and then continue training and save to emodel2
python ./Embedder.py --xfile ./x.smat --yfile ./y.smat --nepochs 5 --out_model emodel2 --in_model emodel --train --gpu 1
 
# skipping ...
 
Epoch 1/5
1298692/1298692 [==============================] - 294s 227us/step - loss: 0.1073 - w_bin_cross: 0.0975 - espec: 0.0204 - enpv: 0.0020 - ppv: 0.4870 - sens: 0.9074 - val_loss: 0.1181 - val_w_bin_cross: 0.1082 - val_espec: 0.0185 - val_enpv: 0.0026 - val_ppv: 0.5010 - val_sens: 0.8770
Epoch 2/5
1298692/1298692 [==============================] - 226s 174us/step - loss: 0.1052 - w_bin_cross: 0.0954 - espec: 0.0202 - enpv: 0.0020 - ppv: 0.4904 - sens: 0.9101 - val_loss: 0.1156 - val_w_bin_cross: 0.1059 - val_espec: 0.0181 - val_enpv: 0.0025 - val_ppv: 0.5089 - val_sens: 0.8804
# ...
# we were able to improve a little more.
 
```
**Which is the Embedding layer?**
The one just before the gaussian noise. We take the third layer, then batch normalize it , so that it is in the N(0,1) distribution on each channel, and then add noise (only in training). This is done in order to make sure our embedding layer gives numbers in a reasonable numerical range, is normalized, and that it is immune to noising each channel, making it a more stable embedding.
 
Some explanation on the model loss and evaluation:
- **Loss function** : we treat the y vector as a binary prediction goal, and to the whole problem as predicting together a vector of binary predictions (in the example above a vector of length 3986). The loss we take is the logloss on each channel , summed over all channels. You will note that our last layer before getting to the y layer is using sigmoid as activation into the y layer, hence predicting a probablily for each channel. Since the y vectors are very sparse we multiply by a weight the cases (y[i][j] == 1) , pushing the model to try better to be right on 1 predictions rather than 0 predictions.
- **Evaluation** : last 20% of x.y matrices (as they appear in the input files) are always used as evaluation data for the embedding training process, and you see that evaluation after each epoch.
- Evaluation metrics (all metrics with val_ prefix are the same but on the validation 20% set). All our done at a point which sets >=0.5 predictions as 1 and the others as 0.
  - loss : overall loss value (as explained above). Big differences between train and validation group hints towards over fit we can try to regilarize (finding the best regularization usually improves results). Note that when using large data sets less regularization is needed. More data is always the best regularizer.
  - w_bin_cross : loss without the regularization terms (l1, l2).
  - ppv : #(true==1 && prob>=0.5) / # (prob >= 0.5) : the probability of being right when predicting positive (larger is better)
  - sens : #(true==1 && prob>=0.5) / # (true == 1) : how many of the positives caught when predicting positive (larger is better)
  - enpv : #(true==1 && prob<0.5) / #(prob<0.5) : the probability for error when predicting negative (lower is better)
  - espec : 1-#(true==0 && prob<0.5)/#(true == 0) : percentage of true negatives not predicted right out of all negatives (lower is better)
 
## Step 7 : Testing we get the same embeddings in Keras and Infrastructure
This is a needed sanity in order to verify the model we trained is indeed the one our infrastructure will use.
```bash
# assuming we prepared t_1.samples : a samples file with a single line
# we first create a sparse mat for this sample, we use the x.scheme file that was created when we first generated the x matrix
Embeddings --gen_mat_from_scheme --f_samples ./t_1.samples --f_scheme ../x.scheme --prefix xtest
 
# this created the xtest.smat file
 
# we can now check it directly with keras using the following line (the model will initialize from the .json and .h35 files):
python ../Embedder.py --embed --in_model ../emodel --xfile ./xtest.smat  
 
# result is :
Using TensorFlow backend.
('arguments---->', Namespace(dim=[400, 200, 100], dropout=[0.0, 0.0, 0.0], embed=True, full_decode=True, gpu=[0], in_model=['../emodel'], l1=[1e-07, 0.0, 0.0], l2=[0.0, 0.0, 0.0], leaky=[0.1], nepochs=-1, no_shuffle=False, noise=[0.3], out_model='', test=False, train=False, wgt=[10.0], xdim=[11933], xfile=['./xtest.smat'], ydim=[3986], yfile='my_y.smat'))
using gpu  0
Embed mode
('reading: ', ['./xtest.smat'])
reading csv file:  ./xtest.smat 18:14:50.269859
preparing sparse mat 18:14:50.275748
('ORIGDIM----> ', 11933, 3986, [11933], [3986])
Running model definition
10.0
10.0
2019-02-20 18:14:50.625090: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-02-20 18:14:51.702925: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1212] Found device 0 with properties:
name: GeForce GTX 1080 Ti major: 6 minor: 1 memoryClockRate(GHz): 1.582
pciBusID: 0000:02:00.0
totalMemory: 10.92GiB freeMemory: 10.76GiB
2019-02-20 18:14:51.702988: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1312] Adding visible gpu devices: 0
2019-02-20 18:14:52.051737: I tensorflow/core/common_runtime/gpu/gpu_device.cc:993] Creating TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 10415 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1080 Ti, pci bus id: 0000:02:00.0, compute capability: 6.1)
Generating an embedding (for testing)
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         (None, 11933)             0
_________________________________________________________________
dropout_1 (Dropout)          (None, 11933)             0
_________________________________________________________________
dense_1 (Dense)              (None, 400)               4773600
_________________________________________________________________
leaky_re_lu_1 (LeakyReLU)    (None, 400)               0
_________________________________________________________________
dropout_2 (Dropout)          (None, 400)               0
_________________________________________________________________
dense_2 (Dense)              (None, 200)               80200
_________________________________________________________________
leaky_re_lu_2 (LeakyReLU)    (None, 200)               0
_________________________________________________________________
dropout_3 (Dropout)          (None, 200)               0
_________________________________________________________________
dense_3 (Dense)              (None, 100)               20100
_________________________________________________________________
leaky_re_lu_3 (LeakyReLU)    (None, 100)               0
_________________________________________________________________
batch_normalization_1 (Batch (None, 100)               400
=================================================================
Total params: 4,874,300
Trainable params: 4,874,100
Non-trainable params: 200
_________________________________________________________________
[[ 0.5779214  -1.1393576  -1.2145319   0.719882    1.152698    2.7561216
   4.7062497  -1.9202161   1.4628897  -0.28924894 -5.909066   -3.8524284
   0.89937544 -1.7450757  -1.6244755   4.2109747   1.8999414   2.4285064
   2.119122   -1.1817946   2.5119438   2.4076338  -1.6450381   2.5745249
   1.3517776   5.6222005   3.1432505   0.97051287 -1.9321308   1.6599026
  -1.135961    4.1045027  -5.8931293  -0.9852152  -0.22657108  3.0653677
   2.6770768   1.325161   -3.7317533   0.78288555  2.749711   -0.71579885
  -0.6447115  -0.54217243  2.1220136   0.16115046  1.6993942   4.197215
  -1.103509   -2.8239236  -2.4093542   1.7677689  -3.7956572   1.0639849
  -4.50788    -0.5759249   1.5213671  -0.01162529  2.6363235  -2.1107693
   4.447809    4.9245405   1.1112337   1.6995897   2.810319   -2.2490163
  -0.57630396  3.6462874   2.2628431   5.652481   -2.4730139   5.1024203
   3.0555716   2.2935085  -1.472085   -0.3556919   0.70053387  3.6700687
   4.944693   -6.186803    1.0003986   3.6284337  -4.352747    3.9384065
  -0.5298457   1.7390456   0.1143899   1.6540909   2.9988813   0.4738245
  -5.7533255   5.286108    4.581069    1.6037283  -0.42494774  2.3381634
  -5.95912     2.1251287   5.0158515  -0.31940365]]
#
# We now want to do the same using our layers file and infrastructure:
# layer 9 is usually the layer of the Embedding if you didn't change the Embedder.py script to run a different network
#
/Embeddings --get_embedding --f_samples ./t_1.samples --f_scheme ../x.scheme --f_layers ../emodel.layers --to_layer 9
 
# results ...
initializing rep /home/Repositories/THIN/thin_jun2017/thin.repository
Read 0 signals, 0 pids :: data  0.000GB :: idx  0.000GB :: tot  0.000GB
Read data time 0.102909 seconds
read_binary_data_alloc [../x.scheme] with crc32 [-63879080]
read_from_file [../x.scheme] with crc32 [-63879080] and size [1892057]
MedSamples: reading ./t_1.samples
WARNING: header line contains unused fields [EVENT_FIELDS,]
[date]=2, [id]=1, [outcome]=3, [outcome_date]=4, [split]=5,
read [1] samples for [1] patient IDs. Skipped [0] records
sorting samples by id, date
Generating sparse mat for 1 lines
Reading layers file ../emodel.layers
ApplyKeras: Reading 0 : LAYER   type=dropout;name=dropout_1;drop_rate=0.000000
ApplyKeras: Reading 1 : LAYER   type=dense;name=dense_1;activation=linear;in_dim=11933;out_dim=400;n_bias=400
ApplyKeras: Reading 2 : LAYER   type=leaky;activation=leaky;name=leaky_re_lu_1;leaky_alpha=0.100000
ApplyKeras: Reading 3 : LAYER   type=dropout;name=dropout_2;drop_rate=0.000000
ApplyKeras: Reading 4 : LAYER   type=dense;name=dense_2;activation=linear;in_dim=400;out_dim=200;n_bias=200
ApplyKeras: Reading 5 : LAYER   type=leaky;activation=leaky;name=leaky_re_lu_2;leaky_alpha=0.100000
ApplyKeras: Reading 6 : LAYER   type=dropout;name=dropout_3;drop_rate=0.000000
ApplyKeras: Reading 7 : LAYER   type=dense;name=dense_3;activation=linear;in_dim=200;out_dim=100;n_bias=100
ApplyKeras: Reading 8 : LAYER   type=leaky;activation=leaky;name=leaky_re_lu_3;leaky_alpha=0.100000
ApplyKeras: Reading 9 : LAYER   type=batch_normalization;name=batch_normalization_1;dim=100
ApplyKeras: Reading 10 : LAYER  type=dropout;name=dropout_4;drop_rate=0.000000
ApplyKeras: Reading 11 : LAYER  type=dropout;name=dropout_5;drop_rate=0.000000
ApplyKeras: Reading 12 : LAYER  type=dense;name=dense_4;activation=linear;in_dim=100;out_dim=200;n_bias=200
ApplyKeras: Reading 13 : LAYER  type=leaky;activation=leaky;name=leaky_re_lu_4;leaky_alpha=0.100000
ApplyKeras: Reading 14 : LAYER  type=dropout;name=dropout_6;drop_rate=0.000000
ApplyKeras: Reading 15 : LAYER  type=dense;name=dense_5;activation=linear;in_dim=200;out_dim=400;n_bias=400
ApplyKeras: Reading 16 : LAYER  type=dense;name=dense_6;activation=sigmoid;in_dim=400;out_dim=3986;n_bias=3986
Embedding[0] :  0.577931, -1.139361, -1.214531, 0.719889, 1.152678, 2.756100, 4.706246, -1.920236, 1.462890, -0.289272, -5.909092, -3.852452, 0.899393, -1.745082, -1.624470, 4.210994, 1.899885, 2.428522, 2.119110, -1.181803, 2.511931, 2.407662, -1.645038, 2.574553, 1.351748, 5.622195, 3.143245, 0.970485, -1.932137, 1.659895, -1.135962, 4.104524, -5.893116, -0.985202, -0.226589, 3.065342, 2.677109, 1.325170, -3.731724, 0.782854, 2.749709, -0.715786, -0.644691, -0.542146, 2.122007, 0.161158, 1.699387, 4.197234, -1.103530, -2.823920, -2.409330, 1.767769, -3.795663, 1.063999, -4.507883, -0.575921, 1.521367, -0.011617, 2.636321, -2.110771, 4.447805, 4.924530, 1.111231, 1.699584, 2.810309, -2.249007, -0.576356, 3.646280, 2.262861, 5.652493, -2.473031, 5.102398, 3.055582, 2.293494, -1.472100, -0.355688, 0.700531, 3.670066, 4.944662, -6.186786, 1.000359, 3.628438, -4.352755, 3.938388, -0.529864, 1.739041, 0.114385, 1.654087, 2.998851, 0.473810, -5.753366, 5.286112, 4.581021, 1.603754, -0.424938, 2.338176, -5.959126, 2.125135, 5.015850, -0.319395,
 
# and as can be easily seen we indeed create the same Embedding !! We're good to go and use this embedding in our infrastructure.
# note we got the same embedding up to ~1e-5 error which is just a numerical error difference. Our embedding is much more stable that this small difference
# since we trained it with added noise 4 orders of magnitude larger.
 
# Another way to test this is to use the Flow --get_json_mat option with the right samples file, and the right json file (see below)
 
```
 
## Step 8 : Using Embedding In a MedModel (Finally !!)
Once we have the .scheme file and the matching .layers file we can generate features using the "embedding" feature generator.
This feature generator will generate for each sample it's sparse x line, then run it through the embedding model , and add the layer output as features in the MedFeatures matrix.
To use embeddings as features add the following to your json
```json
	{ "action_type": 	"feat_generator", "fg_type": "embedding", 
						// the name of the feature will be FTR_<num>.<name_prefix>.col_<embedding column number> , if using several embedding FGs give them different name_prefix names
						"name_prefix" : "Semi_AutoEncoder",
						// your x matrix scheme file
						"f_scheme" : "/nas1/Work/Users/Avi/test_problems/embedding_example/mats/x.scheme",
						// your layers file
						"f_layers" : "/nas1/Work/Users/Avi/test_problems/embedding_example/mats/emodel_auto_xx.layers",
						// layer to use for embedding, typical is 9 if you used the default Embedder.py script
						"to_layer" : "9"},
```
 
## Step 9 : Results for MI with/without Embedding , with/without SigDep
We can now easily train models for our problem. We can use learn_1_B as our training samples and validate_1_B as our cross validation set, and validate_2 as an external test set.
Doing these tests in 4 flavors:
- No categorial signals
  - We used "last", "min", "max", "avg", "last_delta", "last_time" on several time windows 
  - signals : 
"Glucose", "BMI", "HbA1C", "Triglycerides", "LDL", "Cholesterol", "HDL", "Creatinine", "eGFR_CKD_EPI", "Urea", "Proteinuria_State", "ALT", "AST", "ALKP",
 "WBC", "RBC", "Hemoglobin", "Hematocrit", "RDW", "K+", "Na", "GGT", "Bilirubin", "CRP","BP"
  - 
Used also Smoking information, age, gender
- Using Signal Dependency on Drugs and RC (choosing top 100 codes in each) to select correlated read codes.
- Using Embeddings:
  - Embeddings were trained once as an autoencoder (y matrix created at same times of x matrix) and once as a future-encoder in which y matrix was created on times 1 or 2 years a head.
  - Embedding dimension was 100
- Using both SigDep and Embeddings together.
 
Predictor used was the same for all cases: lightgbm with slightly optimized parameters.
Results are given for the 30-730 time window, ages 40-80 , we compare AUCs
<table><tbody>
<tr>
<th>Model</th>
<th>CV AUC</th>
<th>Test AUC</th>
</tr>
<tr>
<td>Labs</td>
<td>0.762</td>
<td>0.763</td>
</tr>
<tr>
<td>+SigDep</td>
<td>0.782</td>
<td>0.782</td>
</tr>
<tr>
<td>+Embeddings</td>
<td>0.785</td>
<td>0.787</td>
</tr>
<tr>
<td>+SigDep +Embeddings</td>
<td>0.787</td>
<td>0.789</td>
</tr>
</tbody></table>
 
CI intervals are more or less +- 0.005
Some points:
- We see a very minor improvement for using Embeddings.
  - This is a nice result , as it verifies the whole concept works.
  - There is a trend towards better results even in this model, and when going to 3y, 5y time windows it gets stronger
- Since the SigDep option is much simpler also when interprating the models , it is not clear Embeddings are preffered in this problem.
- On the other hand the Embedding option is quite general and the same set of features could be used in many different models.
- Also : it may be that finiding/training the right Embedding model will give an even larger boost.
- interestingly there was also a very small improvement trend when using both together:
  - Means most of the information captured by both methods is the same, but still each has some small information parts the other doesn't.
 
 
 
 
