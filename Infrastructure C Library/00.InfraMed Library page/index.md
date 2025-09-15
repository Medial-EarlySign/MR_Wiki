# InfraMed Library page
 
Git Link: [https://github.com/Medial-EarlySign/MR_Libs](https://github.com/Medial-EarlySign/MR_Libs)
### General
The InfraMed Library is a non-sql data structure tailored to hold medical records data.
The main goal is to provide an efficient way to get a vector of time signals (date/time, value) for a pair of patient and signal type (pid , sid).
Main toolsets available in the library:

- Converting a data set to the InfraMed Repository format. (see [here](../../Repositories/Load%20new%20repository.md))
- Adding a signal to the data set, fixing a signal
- Reading a data set or a part of it to memory
- Get the vector of signals for (pid, sid) , date/time sorted
- Create a "by-pid" transposed way of keeping the data
- Get all signals for a pid "by-pid"
- Free/Lock/Unlock/Load mechanisms for signals
- Work with dictionaries 
- Manage versions of data for a signal
- Option to load data in memory to create a repository
 
### The InfraMed data model in 5 sentences.
- each patient has one or more signal vectors.
- each signal is of a specific type.
- In general any type can be added (see more in the MedSignals page) but a signal is composed of a constant number of time channels (0 or more) and a constant number of value channels (0 or more).
- Except for the (new) rep in memory features the library assumes the data is for read-only and updated once in a very long time, so the efficiency of creating a repository is less important.
- The library allows an extremely fast access for a signal vector given a query of a pid + signal_id (or signal name), and this is its main usage.
### General Classes 
It is recommeded to read and understand the following pages explaining the main classes used in the InfraMed library:

- [MedRepository , MedPidRepository](MedRepository.md) : most used classes packing options to read repositories and query them.
- MedConvert : class used when creating a new repository.
- [MedSignals](MedSignals%20_%20Unified%20Signals.md): class used to handle signal files and signal properties, also contains the unified way of accessing signals.
- [MedDictionary , MedDictionarySections](MedDictionary.md) : classes used to read dictionaries and use them
More Advanced:
- [PidDynamicRec](PidDynamicRec.md) : class with an advanced option to hold versions of the same signal.
- InMem repository : the InMemRepData class and its usage in a MedRepository to load data into it.
Even More... (internal important classes and methods):
- IndexTable : class to read data for a specific signal on a subset (or all) pids, with a memory efficient fast index.
- MedSparseVec : a general key,value datastructure. Memory efficient and fast. The baseline for many of the indexes used in a MedRepository.
 
