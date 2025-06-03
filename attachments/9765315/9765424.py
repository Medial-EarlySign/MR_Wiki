# imports
import os
import numpy as np
import pandas as pd
import medpython as med
import datetime as dt
import random
import argparse
import subprocess


# Instantiate the parser
parser = argparse.ArgumentParser(description='Create MedSamples files for Rambam readmission model')

# Required argument
parser.add_argument('--out_name',
	required=True, help='out name suffix (required: %(required)s)')
parser.add_argument('--work_dir',
	required=True, help='working directory, where the sample files will be created (required: %(required)s)')

# Optional argument
parser.add_argument('--rep', 
	default='/server/Work/CancerData/Repositories/Rambam/rambam_nov2018_fixed/rambam.repository', 
	help='repository file name (default: %(default)s)')
parser.add_argument('--train_mask', 
	default=1, choices=[1, 2, 3], help='train mask number (choices: %(choices)s) (default: %(default)s)')
parser.add_argument('--use_file', action='store_true',
	help='use a base train / test file flag, requires file_name')
parser.add_argument('--file_name',
	help='out_name of the samples file to use if use_file flag is raised, requires use_file flag')
parser.add_argument('--fast_readmission_cutoff', type=int, default=30,
	help='values below will be cases (in days) (default: %(default)s)')
parser.add_argument('--admission_duration_min_days', type=int, default=1,
	help='shorter admissions will be discarded (default: %(default)s)')
parser.add_argument('--admission_duration_max_days', type=int, default=90,
	help='longer admissions will be discarded (default: %(default)s)')
parser.add_argument('--kid_age_cutoff', type=int, default=30,
	help='admissions that start before the patient is this many years old will be discarded (default: %(default)s)')
parser.add_argument('--admission_year_min', type=int, default=2006,
	help='admissions that start before 1.1 of this year will be discarded (default: %(default)s)')
parser.add_argument('--admission_year_max', type=int, default=2017,
	help='admissions that start after 1.1 of the next year will be discarded (default: %(default)s)')
parser.add_argument('--max_admissions_per_pid', type=int, default=10,
	help='in the training set this many admissions will be randomly chosen for each patient that has more admission (default: %(default)s)')
parser.add_argument('--mid_length_admission_max', type=int, default=178,
	help='in the training set, control readmissions that acurre before this cutoff will be discarded (in days) (default: %(default)s)')
parser.add_argument('--proportion_of_test', type=float, default=0.2, metavar='[0-1]', #TODO fix code in edge cases (only train / test)
	help='proportion of the patients that will go to the test set (disregarded if --use_file flag is raised) (default: %(default)s)')
parser.add_argument('--verbose', action='store_true',
	help='verbose print flag')	
	
# argument parsing
args = parser.parse_args()
if bool(args.use_file) != bool(args.file_name):
    parser.error('--use_file and --file_name must be used together')
working_directory = args.work_dir
out_name = args.out_name
repository_path = args.rep
training_section = args.train_mask
use_train_test_file = args.use_file
train_test_file_name = args.file_name
fast_readmission_cutoff = args.fast_readmission_cutoff
admission_duration_min_days = args.admission_duration_min_days
admission_duration_max_days = args.admission_duration_max_days
kid_age_cutoff = args.kid_age_cutoff
admission_year_min = args.admission_year_min
admission_year_max = args.admission_year_max
max_admissions_per_pid = args.max_admissions_per_pid
mid_length_admission_max = args.mid_length_admission_max
proportion_of_test = args.proportion_of_test
verbose = args.verbose

# parameter setup
signals_list = ['BDATE','DEATH', 'ADMISSION', 'DIAGNOSIS_PRIMARY']

if args.use_file:
	train_pids_path = working_directory + 'train' + train_test_file_name +'.pids'
	test_pids_path = working_directory + 'test' + train_test_file_name +'.pids'
	all_pids_path = working_directory + 'all' + train_test_file_name +'.pids'

print('\narguments:')
print(args, '\n')


# load repository
rep_train = med.PidRepository()
rep_train.read_all(repository_path,[],['TRAIN']) 
train_signal = rep_train.get_sig('TRAIN')

# create a list of the pids that are in the right section
pids_to_train = [row.pid for index, row in train_signal.loc[train_signal.val == training_section].iterrows()]

# creating the working repository 
rep = med.PidRepository()
rep.read_all(repository_path,pids_to_train,signals_list) 

def signal_overview(signal):
    print("\nhead: ") 
    print(signal.head())
    print("\ndescribe: ")
    print(signal.describe())
    print("\nisnull:")
    print(signal.isnull().sum())
def convert_times(col):    
    date_col=dt.datetime(1900,1,1)+pd.TimedeltaIndex(col,unit='m')
    return(date_col)
def get_signal(name, verbose=True, translate=True):
    df = rep.get_sig(name, translate=translate)
    df = df.loc[df.pid.isin(pids_to_train)]
    #df.set_index('pid', inplace=True)
    if 'date_end' in df.columns:
        df['date_end']=convert_times(df['date_end'])
    if 'date_start' in df.columns:
        df['date_start']=convert_times(df['date_start'])
    if 'date' in df.columns:
        df['date']=convert_times(df['date'])
    if 'time' in df.columns:
        df['time']=convert_times(df['time'])
    if 'date_end' in df.columns and 'date_start' in df.columns:
        df['duration'] = df.date_end - df.date_start
    if verbose:
        signal_overview(df)
    return df

# create admissions dataframe
# birth date
print('\nloading birth dates')
birth_date = get_signal('BDATE', verbose=False)
birth_date.rename(columns={'time':'birth_date'}, inplace=True)
if verbose:
	signal_overview(birth_date)

# death date
print('\nloading death dates')
death_date = get_signal('DEATH', verbose=False)
death_date.rename(columns={'time':'death_date'}, inplace=True)
if verbose:
	signal_overview(death_date)
	
# admissions
print('\nloading admissions')
admission = get_signal('ADMISSION', verbose=False)
admission['start_year'] = admission.date_start.dt.year
admission['start_month'] = admission.date_start.dt.month
admission['duration_days'] = admission.duration.dt.days
if verbose:
	signal_overview(admission)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))

# remove admissions with a negative duration
print('\nremoving ongoing admissions (negative duration)')
admission_neg_duration = admission[admission.duration < dt.timedelta()].copy()
admission = admission[admission.duration >= dt.timedelta()]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of ongoing admissions:")
	signal_overview(admission_neg_duration)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in ongoing admissions:', len(admission_neg_duration.pid), ' / ', len(set(admission_neg_duration.pid)))


# remove very young pid
print('\nremoving young pids')
admission_age = pd.DataFrame.merge(admission, birth_date, on='pid', how='left')
#admission_age['birth_year_datetime'] = admission_age['birth_year'].apply(lambda x: dt.datetime(int(x), 1,1))
admission_age['age_at_admission'] = admission_age.date_start - admission_age.birth_date
age_at_adult = dt.datetime(1900 + kid_age_cutoff, 1,1) - dt.datetime(1900, 1,1)
admission_kids = admission_age[admission_age.age_at_admission < age_at_adult]
admission_adults = admission_age[admission_age.age_at_admission >= age_at_adult]
admission = admission_adults
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of admissions of young patients:")
	signal_overview(admission_kids)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in young admissions:', len(admission_kids.pid), ' / ', len(set(admission_kids.pid)))


# remove very short admissions
print('\nremoving short admissions')
admission_short = admission[admission.duration < dt.timedelta(days=admission_duration_min_days)]
admission = admission[admission.duration >= dt.timedelta(days=admission_duration_min_days)]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of short admissions:")
	signal_overview(admission_short)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in short admissions:', len(admission_short.pid), ' / ', len(set(admission_short.pid)))


# remove very long admissions
print('\nremoving long admissions')
admission_long = admission[admission.duration >= dt.timedelta(days=admission_duration_max_days)]
admission = admission[admission.duration < dt.timedelta(days=admission_duration_max_days)]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of long admissions:")
	signal_overview(admission_long)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in long admissions:', len(admission_long.pid), ' / ', len(set(admission_long.pid)))


# remove very old admissions
print('\nremoving old admissions')
admission_old = admission[admission.date_start < dt.datetime(year=admission_year_min, month=1, day=1)]
admission = admission[admission.date_start >= dt.datetime(year=admission_year_min, month=1, day=1)]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of old admissions:")
	signal_overview(admission_old)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in old admissions:', len(admission_old.pid), ' / ', len(set(admission_old.pid)))


admission = pd.DataFrame.merge(admission, death_date, on='pid', how='left')

print('\ncalculating fast readmissions')
# find the time between admissions
admission_by_pid = admission.groupby('pid')
time_since_last_admission = []
for name, group in admission_by_pid:
    is_first = True
    for row, data in group.iterrows():
        if is_first:
            is_first = False
            time_since_last_admission.append(pd.Timedelta('nat'))
            time_end = data.date_end
            continue
        time_since_last_admission.append(data.date_start - time_end)
        time_end = data.date_end
time_to_next_admission = list(time_since_last_admission[1:])
time_to_next_admission.append(pd.Timedelta('nat'))
admission['time_since_last_admission'] = pd.Series(time_since_last_admission).values
admission['time_to_next_admission'] = pd.Series(time_to_next_admission).values


# remove very new admissions
# note: the needs to be after calculating the time between admissions
print('\nremoving new admissions')
admission_new = admission[admission.date_start > dt.datetime(year=admission_year_max + 1, month=1, day=1)]
admission = admission[admission.date_start <= dt.datetime(year=admission_year_max + 1, month=1, day=1)]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of old admissions:")
	signal_overview(admission_new)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in new admissions:', len(admission_new.pid), ' / ', len(set(admission_new.pid)))


# find fast readmissions
admission['fast_readmission'] = False
admission['fast_readmission'] = admission.time_to_next_admission < dt.timedelta(days = fast_readmission_cutoff)

print('number of fast readmissions:', admission.fast_readmission.sum())


# remove admissions that ended in death (including patients who died on the day of discharge)
admission['time_to_death'] = admission.death_date - admission.date_end
admission_death = admission[admission.time_to_death <= dt.timedelta(days=1)]
admission = admission[(admission.time_to_death > dt.timedelta(days=1)) | (admission.time_to_death.isnull())]

admission['fast_death'] = admission.time_to_death < dt.timedelta(days = fast_readmission_cutoff)
print('number of fast deaths:', admission.fast_death.sum())

admission['fast_readmission'] = admission.fast_death | admission.fast_readmission

print('number of fast readmissions or deaths:', admission.fast_readmission.sum())

# remove chemo
print('\nremoving chemotherapy admissions')
diagnosis_chemo_name = get_signal("DIAGNOSIS_PRIMARY", verbose=False, translate=True)
diagnosis_chemo_name['val'] = diagnosis_chemo_name.val.astype(str)
diagnosis_chemo_name[diagnosis_chemo_name.val.str.contains('CHEMO')]
diagnosis_chemo_name = diagnosis_chemo_name[diagnosis_chemo_name.val.str.contains('CHEMO')]
admission = admission.merge(diagnosis_chemo_name, on='pid', how='left')
admission_chemo = admission[admission.val_y.notnull()]
admission = admission[admission.val_y.isnull()]
if verbose:
	print("fixed admission overview:")
	signal_overview(admission)
	print("\n overview of chemo admissions:")
	signal_overview(admission_chemo)
print('number of admissions / unique pids in fixed admissions:', len(admission.pid), ' / ', len(set(admission.pid)))
print('number of admissions / unique pids in chemo admissions:', len(admission_chemo.pid), ' / ', len(set(admission_chemo.pid)))


# train / test split
print('creating train / test split')
if use_train_test_file:
    all_pids = list(pd.read_csv(all_pids_path, header=None)[0].values)
    pids_for_test = list(pd.read_csv(test_pids_path, header=None)[0].values)
    pids_for_train = list(pd.read_csv(train_pids_path, header=None)[0].values)
else:
    all_pids = list(set(admission.pid))
    num_test_samples = int(len(all_pids) * proportion_of_test)
    pids_for_test = np.random.choice(all_pids, num_test_samples, replace=False)
    pids_for_train = set(all_pids) - set(pids_for_test)
train_pids_path = working_directory + 'train' + out_name +'.pids'
test_pids_path = working_directory + 'test' + out_name +'.pids'
all_pids_path = working_directory + 'all' + out_name +'.pids'
pd.Series(list(pids_for_train)).to_csv(train_pids_path, index=False)
pd.Series(list(pids_for_test)).to_csv(test_pids_path, index=False)
pd.Series(list(all_pids)).to_csv(all_pids_path, index=False)

readmission_for_train = admission[admission.pid.isin(pids_for_train)]
readmission_for_test = admission[admission.pid.isin(pids_for_test)]

# case / control split
print('creating case / control split')
def case_control_split(admission, train=True, use_controls=False):
    if train:
        if not use_controls:
            fast_readmission_for_samples = admission.loc[admission.fast_readmission]
            fast_readmission_for_samples['outcome'] = 1
            # find pids that have no fast readmissions
            case_pids = set(fast_readmission_for_samples.pid)
            admission_pids = set(admission.pid)
            control_pids = admission_pids - case_pids
            not_fast_readmission_for_samples = admission[admission.pid.isin(control_pids)]
            not_fast_readmission_for_samples['outcome'] = 0
            # remove intermediate length readmisions
            not_fast_readmission_for_samples_mid_length = not_fast_readmission_for_samples.loc[not_fast_readmission_for_samples.time_to_next_admission <= dt.timedelta(days=mid_length_admission_max)]
            not_fast_readmission_for_samples = not_fast_readmission_for_samples.loc[(not_fast_readmission_for_samples.time_to_next_admission > dt.timedelta(days=mid_length_admission_max)) |
                                                                       (not_fast_readmission_for_samples.time_to_next_admission.isnull())]
            readmission_for_samples = pd.concat([fast_readmission_for_samples, not_fast_readmission_for_samples])
        else:
            readmission_for_samples = admission
            readmission_for_samples['outcome'] = readmission_for_samples['fast_readmission']
            readmission_for_samples['outcome'] = readmission_for_samples['outcome'].astype(int)
            readmission_for_samples = readmission_for_samples.loc[(readmission_for_samples.time_to_next_admission > dt.timedelta(days=mid_length_admission_max)) |
                                                                 (readmission_for_samples.time_to_next_admission.isnull()) |
                                                                 (readmission_for_samples.fast_readmission)]           
    else:
        readmission_for_samples = admission
        readmission_for_samples['outcome'] = readmission_for_samples['fast_readmission']
        readmission_for_samples['outcome'] = readmission_for_samples['outcome'].astype(int)
    return readmission_for_samples

readmission_for_train_full = case_control_split(readmission_for_train, train=False)
train_no_downsampling_dataframe_path = working_directory + 'train' + out_name +'_no_downsampling_dataframe.samples'
readmission_for_train_full.to_csv(train_no_downsampling_dataframe_path)
	

readmission_for_train = case_control_split(readmission_for_train, train=True, use_controls=True)
readmission_for_test = case_control_split(readmission_for_test, train=False)


# downsampling patients with many admissions
print('downsampling patients with many admissions')
readmission_for_train = readmission_for_train.groupby('pid').apply(lambda x: 
                 x.loc[np.random.choice(x.index, max_admissions_per_pid, replace=False), :]
                 if len(x) > max_admissions_per_pid else x)

				 
				 
# create splits file
print('creating splits file')
if use_train_test_file:
    all_pids_dataframe = pd.read_csv(working_directory + 'splits'+ train_test_file_name + '.rambam', sep=' ')
else:
    num_pids = len(all_pids)
    random_split = []
    for _ in all_pids:
        random_split.append(random.randint(0,5))
    splits = [('NSPLITS', all_pids),
           ('6', random_split)]

    all_pids_dataframe = pd.DataFrame.from_items(splits)
    all_pids_dataframe = all_pids_dataframe.rename(columns={'pid':'NSPLITS','splits':'6'})
all_pids_dataframe.to_csv(working_directory + 'splits'+ out_name + '.rambam', sep=' ', header=True, index=False)
all_pids_dataframe = all_pids_dataframe.rename(columns={'NSPLITS':'pid','6':'splits'})


# create samples file
print('create samples file')
def add_header(path, remove_first_line=False, first_line='EVENT_FIELDS\tid\ttime\toutcome\toutcomeTime\tsplit\nTIME_UNIT\tMinutes\n'):
    with open(path,'r') as contents:
        if remove_first_line:
            _ = contents.readline()
        save = contents.read()
    with open(path,'w') as contents:
        contents.write(first_line)
    with open(path,'a') as contents:
        contents.write(save)

readmission_for_train = readmission_for_train.merge(all_pids_dataframe, on='pid', how='left')
readmission_for_train['SAMPLE'] = 'SAMPLE'
train_path = working_directory + 'train' + out_name +'.samples'
readmission_for_train.to_csv(train_path, sep='\t', columns=['SAMPLE', 'pid', 'date_end','outcome' ,'date_end','splits'], date_format='%Y%m%d%H%M', header=False, index=False)

add_header(train_path)

readmission_for_test = readmission_for_test.merge(all_pids_dataframe, on='pid', how='left')
readmission_for_test['SAMPLE'] = 'SAMPLE'
test_path = working_directory + 'test' + out_name +'.samples'
readmission_for_test.to_csv(test_path, sep='\t', columns=['SAMPLE', 'pid', 'date_end','outcome' ,'date_end','splits'], date_format='%Y%m%d%H%M', header=False, index=False)

add_header(test_path)

# parameter matching
train_matching_path = working_directory + 'train' + out_name +'_matching.samples'
# there is a problem accessing alias through subprocess, this seems like the most simple way to access the Flow app
subprocess.call(['/server/UsersData/reutf/MR/Tools/Flow/Linux/Release/Flow', '--rep', repository_path, '--filter_and_match', '--in_samples', train_path, '--out_samples', train_matching_path, '--match_params', 'priceRatio=10;maxRatio=10;verbose=1;strata=time,year,1'])

out_samples = pd.read_csv(train_matching_path, sep='\t')

add_header(train_matching_path, remove_first_line=True)

# samples after matching:
out_samples_work = out_samples.copy()
out_samples_work['start_year'] = out_samples_work.time.str.extract(r'([0-9][0-9][0-9][0-9]).*')
out_samples_work = out_samples_work.loc[1:, :]

train_dataframe_path = working_directory + 'train' + out_name +'_dataframe.samples'
readmission_for_train.to_csv(train_dataframe_path)

test_dataframe_path = working_directory + 'test' + out_name +'_dataframe.samples'
readmission_for_test.to_csv(test_dataframe_path)

