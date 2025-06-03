# Virtual Signals
Given a repository we may need at times to be able to dynamically add new signals to it with new names and new types, and have the ways to push data into them. This is in particular useful when building and calculating features for some problems, as in many cases saving the features or their interim results as a new signal is the most elegant way of calculating what we need.
Typical example : suppose we do not have eGFR calculated in our repository (or have some variant of how to calculate it), and we want to create a set of features based on eGFR , such as last, min, max, avg, etc, in several time windows relative to our samples. In this case the most natural thing to do would be to create a new virtual signal to hold eGFR, have some way of calculating it and pushing its data into the repository, all in memory and not in the real repository, and then simply use it as a signal like any other and get all the natural options to create features.
## Virtual Singals definition in a repository
To define a new virtual signal one simply needs to use the insert_virtual_signal API , found in MedSignals.h :
- int insert_virtual_signal(const string &sig_name, int type) 
  - sig_name : is the new name of the virtual signal, it has to be a new one not used already by the repository
  - type : has to be one of the supported types for signals
This initialization checks for validity and initializes several internal tables to support the new signal.
## Adding Data to a virtual signal
There are two options currently:
1. Use the in_mem mode of a repository : this mode allows adding and deleting data from a repository that is fully kept in memory. See pages describing this (useful at times) mode.
2. Use dynamic records (see into to dynamic records [here](InfraMed%20Library%20page/PidDynamicRec)) and their API to change/add data to a signal : this is the method used in the MedProcessTools library and we shall describe in in greater depth in this page.
In the MedProcessTools library the first stages being run are rep processors stages. Each has a learn and apply method. Currently let's focus on virtual signals that do not need a learn process, but just applying some calculation to create a new signal. The more complex case is not much more complex, it usually means some parameters (or models) need to be learned/trained in the learning process, and they will be used when actually calculating the signal. The most complex cases are virtual cases that are needed for a learn stage of another rep processor or feature generator. These are currently not well supported in the library.
In the library apply stages the library creates a PidDynamicRec for each patient, with all the needed time points , contatining all the signals needed for calculating all the future processors and generators defined in the model. If the repository we use has the virtual signals we need defined already, we get to a point in which all we have to do is add data to a virtual signal in a dynamic rec. This is a simple task:
- Calculate the time channels and value channels for your virtual signal, on all needed time points.
  - Important: to do this correctly you will have to take into account the versions of the dynamic rec, and in case they are different calculate a new set of data for the virtual signal for each version.
- Use one of the following API's in PidDynamicRec:
  - int set_version_data(int sid, int version, void *datap, int len) 
    - sid - the signal id of your virtual signal (it will be assigned one dynamically when defined, and you'll be able to get it using the rep.sigs.sid(string name) API.
    - version - which version to push data to.
    - datap : a pointer to an array of your sig type (best is have a vector<sigType> data; with the correct type and use the pointer &data[0]. Of course this should be filled in with the correct times and values.
    - len : how many items are pushed in.
  - int set_version_universal_data(int sid, int version, int *_times, float *_vals, int len) :
    - sid : signal id
    - version : to push to
    - times , vals : the time and val channels , if there's more than 1 time or value channel for the signal simply put them one after the other for each element.
    - len : how many items are added.
- Note that if you pushed data to some version, and there are other versions that should be similar to it, there's no need in calculating and pushing the data to all versions, but simply point them to the version that was added using :
  - int point_version_to(int sid, int v_src, int v_dst);
 
## Writing a rep processor that creates a virtual signal
One option is to write one such processor from scratch , the other is using the RepCalcSimpleSignals which covers many of the needed cases and saves lots of technical work (see next paragraph)
When writing a rep processor fro a virtual signal from scratch the following steps are needed on top of a typical rep processor
1. Each RepProcessor has a vector called virtual_signals (defined in the base class) that should contain all the virtual signals created by the rep processor. This vector must be initialized in the init() function of the rep processor. Later the (inherited) add_virtual_signals will be called at the right time by the model to actually create these signals.
2. Implement the init(), init_tables(), learn(), apply() , as needed for any rep processor.
3. At the point where the new virtual signal is created :
  
1. loop over the versions in the dynamic rec
2. calculate the new signal from the dynamic rec
3. push it inside to the right version using either the set_version_data or the set_version_universal_data APIs.
## Using the RepCalcSimpleSignals processor for virtual signals
The RepCalcSimpleSignals rep processors is a wrapper that does lots of the work needed for simple virtual signal calculators. You can simply implement a new SimpleCalculator and support it from RepCalcSimpleSignals ::make_calculator. See several simple examples directly in the code.
 
 
 
