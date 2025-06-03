# MedRepository
### General
The MedRepository and MedPidRepository are wrapper classes with tools to read a repository or part of it and manage that, together with tools to query it.
These are the main classes in the InfraMed library and a must know if you need to use the library.
 
### MedRepository vs. MedPidRepository
MedPidRepository is an extention of MedRepository that allows along the regular APIs the option to load a complete record of a patient into a PidRec.
This is useful when one needs to go over pids, and for each one to load all that data we have for it in the database.
 
### Initializing and loading data into a MedRepository
There are several options to do this:
- Use the read_all() function:
  - read_all() gets :
    - the repository configuration file
    - a vector of signal names or an empty vector to sign loading all signals
    - a vector of pids or an empty vector in case all pids are needed
  - read all will read the cartesian product of pids x signals asked into memory , and once it succesfully returns the repository is ready for querying.
- Use the init() function:
  - init() will get just the configuration file and initialize everything (signals, dictionaries, file locations) except for the data. Data can be loaded later using the load()/free() mechanisms.
- Use load() or free()
  - load() gets a signal name and a list of pids (or all pids signed with an empty list) and load it into memory.
  - free() gets a signal name and frees the data for that signal. This allows memory management in case of handling very large quantities.
Code examples:
**Options to init and load a repository**
```c++
// define a repository variable
MedRepository rep;
 
// repository conf file
string rep_conf = "/home/Repositories/THIN/thin.repository"
 
// in all following rep functionalities we ommit the return code checks for clarity but a return code < 0 signals an error in performing the task
 
//....
// option 1 : read all the repository, all signals and all pids into rep
rep.read_all(rep_conf);
 
//...
// option 2 : read just a subset of pids and signals
vector<string> sigs = {"BYEAR","GENDER","Glucose","HbA1C","BMI","Drug"}; // use sigs = {} to read all signals for the defined pids
vector<int> pids = {5000001, 50000002, 10000000};                          // use pids = {} to read all pids for the defined sigs
rep.read_all(rep_conf, pids, sigs); 
 
//...
//option 3 : just initialize the repository with no signals,pids read yet, but all configuration files (dictionaries, signals, config) loaded
rep.init(rep_conf);
 
//...
// option 3 continued : loading a specific subset
rep.load(sigs,pids);
// option 3 cont. : free signals options
rep.free(sigs);       // free all signals in the vector sigs
rep.free_all_sigs();  // free all signals from memory
 
// ... ready now to reload again
 
 
```
### Accessing the actual data in a MedRepository
After reading the repository or a subset of it into memory we would like to access that data. Currently there is one simple API to do this : the get() function. The get() allows one to get an access to a time sorted vector of values for a specific pid and a specific signal.
It returns a void pointer that should be converted to the right signal type pointer in order to access the data correctly. 
There's another more advances way of accessing the data which is universal and independent of the signal actual type. Please see that explained under the universal singal sections.
Here are some code samples for a simple get:
**MedRepository get examples**
```c++
// repository variable
MedRepository rep;
 
// ... read .. init ... load... get to a state of using the data
 
int pid;    // pid to read in examples
string sig; // signal to read
 
// .. get to a context in which pid,sig are initialized
 
// sid is a signal id - inside loops it is recommended to use it instead of the string name for performance (avoid going through unordered_maps, etc...)
int sid = rep.sigs.sid(sig); // Basic API to convert from string sig to int sid
 
// len is an output: the length of the vector read. The units are actual signal elements (and not byte size). 
int len; 
// Reading a DateVal signal (the most common one in outpatient repositories)
SDateVal *sdv = (SDateVal *)get(pid, sig, len);
 
// using sdv and len 
printf("read %d items\n",len);
if (len > 0)
	printf("First item is : time %d , val %f . Last item is : time %d , val %f\n", sdv[0].date, sdv[0].val, sdv[len-1].date, sdv[len-1].val);
 
// a faster get if sid is prepared
sdv = (SDateVal *)get(pid, sid, len);
 
// Reading a different type like SVal
SVal *sv = (SVal *)get(pid, "BYEAR", len);
 
 
```
 
### MedPidRepository : initialization , loading and usage
MedPidRepository is an extension of the MedRepository which adds options to read single pids into memory instead of a batch of many. This allows for options of scanning the whole repository while maintaining a very low memory signature, as each thread will only hold the data for a single patient at a specific time instead of the process holding ALL the data needed.
In cases where there's enough RAM to hold all the pids x signals needed for a session it may be more efficient to batch load all the data at start as explained above, and use the regular get() option.
In order to use a MedPidRepository a step of transposing the data needs to take place when the building of a new repository is done. See the relevant new repository creation pages for more info.
Assuming that is done and prepared, the usage is via a PidRec element. One first loads the data for a pid (this is ALL the signals for this pid) into a PidRec, different PidRec elements can be read in parallel in different threads. Once the PidRec is read, one can use a get() on it to get the signal vector. This time of course there's no need for pid, but just for the signal needed.
 
**MedPidRepository and PidRec examples**
```c++
// defining a MedPidRepository , and a PidRec
MedPidRepository pid_rep;
PidRec rec;
 
// Initializing a MedPidRec with the init API
pid_rep.init(rep_conf_file);
 
// ... 
 
// reading a record
pid_rep.get_pid_rec(pid, rec);
 
// getting a specific signal (will work also with an sid)
SDateVal *sdv = rec.get(sig_name, len);
 
```
In some cases there's a repository in memory initialized regularly but we still may need to create a PidRec for a specific pid, for example in order to use functions that were written for PidRec records, or when we want to work with dynamic pid records (see their page). There's a simple way to do this, the init_from_rep() API , that also allows us to choose which sids will be loaded into the PidRec. init_from_rep() actually copies the record, so we lose some efficiency when working with it, however, this is needed in a dynamic record that has the option to change a record.
**Initialize a PidRec from a MedRepository**
```c++
MedRepository rep;
PidRec rec;
 
// ... initialize rep as explained above ...
 
// ...
 
// now, initialize rec from rep 
vector<int> sids; // an empty sids vector signs getting all available signals that were loaded to memory in rep
rec.init_from_rec(&rep, pid, sids);
```
 
### Tricks of the trade
Some simple tricks help optimize performance when using the InfraMed Library:
- Use a local copy of your repository ON the machine used. In the linux nodes the standard place to put a repository is /home/Repositories (make sure there's enough disk space left after, get rid of old unused repositories placed there)
- Inside large loops over lots of patient ids try to call get with a signal id rather than a string id, this will save a call to maps inside the get for each patient, and speed up the get().
  - 
For example Instead of calling
```c++
int pid;
string sig_name;
 
// pid looping block
for (...) {
SDateVal *sdv = (SDateVal *)rep.get(pid, sig_name);
...
}
```
Use: 
```c++
int pid;
string sig_name;
int sid = rep.sigs.id(sig_name);
 
// pid looping block
for (...) {
SDateVal *sdv = (SDateVal *)rep.get(pid, sid);
...
}
```
- 
Reading just the subset of signals that will actually be used is faster and saves memory.
