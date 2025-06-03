# MedSignals / Unified Signals
MedSignals is an internal class in MedRepository, it is used to define different types of signals, and also manages the .signals files which are dictionaries between a signal name and its properties.
Each MedRepository instance contains the sigs signals obeject that allows performing some basic .signals operations.
All the definitions for signals are in the MedSignals.h file .
When a Repository is initialized one of the first things done is reading the repository signals config file (to be pointed to in the repository config file) and initializing all signals definitions.
### What is a signal actually?
A signal type is a class defined in MedSignals.h , it is a placeholder for signals. Signals are names of actual data signals kept in the repository using some specific type. Typical signals examples:
- *BYEAR* , *GENDER* , *TRAIN* : these have only a float value , typically using the *SVal* signal type.
- *Hemoglobin* , *Creatinine* : these have a date and a float value , typically using the *SDateVal* type (In in patients repositories , at the moment using the *STimeVal* type).
- *BP* : has a date and two short values , keeping the diastolic and systolic measures in a blood pressure test. (signal type SDateShort2)
There are several properties we keep for each signal , this can be seen in the SignalInfo class. Among these are:
- *name* : the actual name of the signal
- *type* : the code for its type (must be defined in the enum SigType)
- *sid* : a signal int id code. This is defined in the signals config file. When a repository is built it uses the sid code internally (for example when packing "by_pid" records for a MedPidRepository). Also , the sids provide a fast access to internal indexing tables and save the time needed to search by the string name of a signal. This allows to write faster loops over the data. Of course the sid must be unique. sid numbers are maxed by MAX_SID_NUM (currently 100000 , and seems more than enough...).
- *bytes_len* : the space in bytes it takes to hold a single element in a file or in memory. This is needed when calculating exact starting points of data vectors.
- *n_time_channels* : see below.
- *n_val_channels*
 
Currently a signal must have a constant size. 
### Unified Signals - Part I
The main observation is that in digital medical records almost ALL signals can be modeled as having 0 or more time channels , and then having 0 or more value channels.
Some examples are:
- *BYEAR* : 0 time channels , 1 value channel
- *Creatinine* : 1 time channel , 1 value channel
- *BP* : 1 time channel, 2 value channels
- *DM_Registry* : 2 time channels , 1 value channel
Assuming the time channels can be expressed in an int value , and the value channels can be expressed in a float value, there's a way to read signal times and values without having to KNOW their actual type, in a unified manner. This allows to write a generalized code that works on all types of signals rather than switch into the different types and write for each a new implementation. This is very useful when writing RepProcessors , FeatureGenerators , etc... inside the MedProcessTools infrastructure.
For actual usage and examples of how to use unified signals - see part II
### Current Signal Types
All signals are defined in MedSignals.h. 
Currently the following are defined:
<table><tbody>
<tr>
<th>Signal Type</th>
<th>Time Channels</th>
<th>Value Channels</th>
<th>Actual placeholders</th>
<th>Example Signals Using Type</th>
</tr>
<tr>
<td>SVal</td>
<td>0</td>
<td>1</td>
<td>float</td>
<td>BYEAR , TRAIN, GENDER</td>
</tr>
<tr>
<td>SDateVal</td>
<td>1</td>
<td>1</td>
<td>int : float</td>
<td>Hemoglobin, Creatinine, RC_Diagnosis</td>
</tr>
<tr>
<td>STimeVal</td>
<td>1</td>
<td>1</td>
<td>long long : float</td>
<td>Creatinine (mimic)</td>
</tr>
<tr>
<td>SDateRangeVal</td>
<td>2</td>
<td>1</td>
<td>int,int : float</td>
<td>DM_Registry</td>
</tr>
<tr>
<td>STimeRangeVal</td>
<td>2</td>
<td>1</td>
<td>long long, long long : float</td>
<td>(mimic)</td>
</tr>
<tr>
<td>STimeStamp</td>
<td>0</td>
<td>1</td>
<td>: long long</td>
<td>(mimic)</td>
</tr>
<tr>
<td>SDateVal2</td>
<td>1</td>
<td>2</td>
<td>int : float , unsigned short</td>
<td>Drugs (MHS)</td>
</tr>
<tr>
<td>STimeLongVal</td>
<td>1</td>
<td>1</td>
<td>long long : long long</td>
<td>(mimic)</td>
</tr>
<tr>
<td>SDateShort2</td>
<td>1</td>
<td>2</td>
<td>int : short , short</td>
<td>BP</td>
</tr>
<tr>
<td>SValShort2</td>
<td>0</td>
<td>2</td>
<td>: short , short</td>
<td>(mimic)</td>
</tr>
<tr>
<td>SValShort4</td>
<td>0</td>
<td>4</td>
<td>: short, short, short, short</td>
<td>(mimic)</td>
</tr>
</tbody></table>
### Implementing a new signal
When doing this one needs to add an enum number to this type which will be the one that encodes the type in the signals file etc. Then define the signal and its methods (see below), and then make sure that the MedConvert reads the signal correctly when loading a new repository (search for all the cases other signal types are used in the MedConvert files, and add your new signal parsers in the right places in the same manner.
When implementing the signal class make sure it inherits from UnifiedSig (otherwise, code using unified signals will not be able to run on this type), and implement the following methods:
- n_time_channels()
- n_val_channels()
- time_unit() : default time unit for the signal
- int Time(int chan) : return the time channel asked for , as int
- float Val(int chan) : return the value channel asked for , as float
- SetVal(chan, _val) : set a specific value channel
- Set(int *times, float *vals) : set all time and value channels from time and value arrays
- bool operator< : comperator
- bool operator== : comperator for equality
- operator << : for printing
### Unified Signals - part II
In order to use a unified signal one has to work through an intermidiator class called UniversalSigVec (we'll use the short name usv). The general plan is instead of using get() in a repository in its typical form , we will now use a new API called uget() to "get" the signal into a usv object. The usv object has the following properties:
- We can initialize it to work for a specific signal GIVEN ONLY the enum of the signal type.
- Once initialized we can use it for ugets() and "get" the data into it (there are no copies, it is all playing with pointers and virtual functions and finction pointers
- It has an API to get any value for any time channel or value channel which is the same for all types.
These properties allow a usv to be used to write code which is type independent.
The performance price of using a usv is the initialization time for a specific signal type (in which some function pointers are copied), however when using the same usv with the same type over and over the initialization time is mostly saved as we do most of the work only when the type changes.
Some code examples:
**UniversalSigVec usage examples**
```c++
// repository , usv definitions
MedRepository rep;
UniversalSigVec usv;
 
// ... init rep ... get to the right point in code....
 
rep.uget(pid, sid, usv);
 
// example of printing all time channels and all val channels for the all the elements in the read usv vector
// usv.len holds the number of elements read.
 
for (int i=0; i<usv.len; i++) {
	for (int t_ch=0; t_ch<usv.n_time_channels(); t_ch++)
		cout << " element " << i << " time channel no. " << t_ch << " => " << usv.Time(i, t_ch);
	for (int t_ch=0; t_ch<usv.n_val_channels(); t_ch++)
		cout << " element " << i << " value channel no. " << t_ch << " => " << usv.Val(i, t_ch);
}
 
 
// We can also uget from a PidRec
MedPidRepository pid_rep;
PidRec rec;
 
// ... init pid_rep ....
 
// reading rec
pid_rep.get_pid_rec(pid, rec);
 
// ugetting from rec - no need for pid as this is already for a specific pid
rec.uget(sid, usv);
 
```
 
### Signals Config File
When reading a repository we read also the repository's signal file (can be several files). This file defines the signal names, their internal code, their type , and its format is the following:
- empty lines or lines starting with # are ignored (allowing an easy way to write comments)
- definition lines are tab delimited in the following format:
  - SIGNAL <signal name> <signal code> <signal type> <comment / optional>
example for a few lines:
 
**Example lines from a signals file**
```
SIGNAL  GENDER  100     0       Male=1,Female=2
SIGNAL  BP      920     8
SIGNAL  Hemoglobin      1000    1
SIGNAL  RC      2309    1       Med All ReadCodes ^[0-9A-HJ-NP-U] .no I,O,V,W,X,Y
SIGNAL  Drug    2400    8       Drugs: date, drug code, duration in days, need to use the proper dictionary section
```
 
 
