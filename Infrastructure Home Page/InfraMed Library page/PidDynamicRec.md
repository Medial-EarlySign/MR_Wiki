# PidDynamicRec
The PidDynamicRec class offers a more advanced way of accessing the data, that allows not only to read it, but also to change it , and not only that, but also to keep several "versions" of a signal vector.
The need for both the ability to change a signal vector and/or keep several versions of it arises when writing RepProcessors in the MedProcessTools classes. When for example cleaning a signal we may want to change a specific signal or ignore and delete it before moving on to create features, and this forces us to not only read the data for the signal but to actually change it. 
### Why do we need the cumbersum versions at all?
Good question.
When running a RepProcessor algorithm of some kind and deciding to change or delete or add a certain value for a signal at some timepoint T , we may be using data from timepoints t > T. When training and testing models this can cause a serious leak of peeking into the future, as information from future values beyond the time point we changed is used in changing the value at time T. If for example we are planning to test at a timepoint T_test and T_test >= T and we used data from timepoints in which t > T_test we are at a serious problem.
The problem becomes more complex if we plan to test several different time points for some patient. Suppose there are two test points T_test1 and T_test2 to calculate a score, suppose T_test2 > T_test1 , we now have the following problem:
- The "Horizon" for allowed time points to use for RepProcessors for T_test1 is t <= T_test1
- The "Horizon" for allowed time points to use for RepProcessors for T_test2 is t <= T_test2
- It may well be that the value the RepProcessors creates for some t<=T_test1 will be DIFFERENT in those two different Horizons... 
This forces us to keep a "version" which is a snapshot of the data at a certain timepoint assuming it didn't "see" any data beyond its allowed Horizon.
On top of that we need to do this efficiently and be able to hold a large number of versions for a record and let the user who manages it for efficient memory and speed options to do it.
The PidDynamicRec gives a reasonable solution to all these issues.
### Versions numbering 
Version 0 is always kept as the original version that was read from the repository.
Versions 1 and up are versions created using the tools the PidDynamicRec offers and can of course be different from it.
The number of different versions will typically be the number of different timepoints needed for this record (typically the number of different prediction time points). Of course +1 for version 0 that keeps the original.
### Initializing a PidDynamicRec
A PidDynamicRec is a PidRec by inheritance, and is initialized in methods resembling those of a PidRec ( See [here](../MedRepository.html#MedRepository-pid_rec). ) , but there are some changes.
Along with the repository, pid and list of signals to start with one needs to initialize the number of versions to keep in the record (typically this will be the number of different timepoints we want to work with). This can be done using the set_n_versions() method.
The method to do it is:  
int init_from_rep(MedRepository *rep, int pid, vector<int> &sids_to_use, int n_versions)
### Reading From a PidDynamicRec
When reading from a dynamic rec we need to ask for a specific signal as always, but along with it we also ask it in a specific version.
so get() methods look now like:
- void *get(int sid, int version, int &len)
- void *get(string &sig_name, int version, int &len)
and uget() methods look now like:
- void *uget(int sid, int version, UniversalSigVec &_usv)
- *uget(const string &sig_name, int version, UniversalSigVec &_usv)
Remember that for convinience each PidRec holds a usv object for usage inside, this helps threading safely while making sure the usv is initialized the minimal number of times. It can be used to enhance efficiency when needed.
### Making changes to a version in a PidDynamicRec
This is the reason why we work with a PidDynamicRec : creating and maintaining versions that can be different from the original version.
Initially ALL versions point to the original version (the 0 version).
here's the relevant part in the class with all the different methods to do this, with additional comments:
**Creating and changing versions**
```c++
	// creating and changing versions
 
	// sets a version to a given dataset , datap points to the new data vector that should fit the format of the specific signal we deal with (say SDateVal)
	// len is the length is signal units (not bytes) of the new data. The new data will be copied into the dynamic rec and version number 'version' will
	// point to it. This method is the most general and actually allows any change we want. We can work with version 0 to get the original data, and then 
	// create a whole new data vector and load it in as a new version.
	int set_version_data(int sid, int version, void *datap, int len);
 
	// creates a new version 'version' by simply copying the original into it (rather that just pointing)
	int set_version_off_orig(int sid, int version);
 
	// will point version v_dst to the data of version v_src
	int point_version_to(int sid, int v_src, int v_dst);	
 
	// removing element idx from version
	int remove(int sid, int version, int idx);
 
	// removing element idx from version v_in and putting it in v_out
	int remove(int sid, int v_in, int idx, int v_out);	
	// changing element idx in version to hold *new_elem
	int change(int sid, int version, int idx, void *new_elem);	
 
	// changing element idx in v_in to *new_elem, and putting it all in v_out
	int change(int sid, int v_in, int idx, void *new_elem, int v_out);	
 
	// Apply changes and removals in batch:
	// changes is a vector of pairs , each holding the index of the element to change and then a pointer to the new one
	// removes is a vector of ints , the indexes of the elements to remove
	// all operations are done inplace on v_in , all indexes are v_in indexes before any change was done.
	int update(int sid, int v_in, vector<pair<int, void *>>& changes, vector<int>& removes);
 
	// Apply val changes and removals, unified variant
	// Same as above, but in changes we state the actual float value we change.
	// We also give the value channel to change.
	int update(int sid, int v_in, int val_channel, vector<pair<int, float>>& changes, vector<int>& removes); 
```
 
And now to a simple example showing how to take a signal (this case Glucose) , remove all entries that are 0 or negative, and make sure the value is rounded to int(). We will show how to this in different ways.
**PidDynamicRec example**
```c++
MedRepository rep;
int pid;
 
// ... load rep ... set pid to some interesting pid ...
 
// ...
 
// Define a PidDynamicRec and initialize it with 1 more version
PidDynamicRec pdr;
int sid = rep.sigs.sid("Glucose");
vector<int> sids = { sid }; // prepare the sids list we want to work with
pdr.init_from_rep(&rep, pid, sids, 1); // created a very simple dynamic record with just Glucose signal inside it 
 
// get the original version (=version 0) data
UniversalSigVec usv;
pdr.uget(sid, 0, usv);
 
// option1: prepare a new vector and insert it to version 1
vector<SDataVal> new_glu;
for (int i=0; i<usv.len; i++) {
	if (usv.Val(i,0) > 0) {
		SDataVal sdv;
		sdv.date = usv.Time(i,0);
		sdv.val = (float) ((int)usv.Val(i,0));
		new_glu.push_back(sdv);
	}
}
 
pdr.set_version_data(sid, 1, &new_glu[0], (int)new_glu.size()); // use the method to load a whole new version
 
// option2: collect changes and update the rec
vector<pair<int,float>> changes;
vector<int> removes;
for (int i=0; i<usv.len; i++) {
	if (usv.Val(i,0) > 0) {
		pair<int,float> p;
		p.first = i; // index to change
		p.second = (float) ((int)usv.Val(i,0)); // changed value
		new_glu.push_back(sdv);
	} else
		removes.push_back(i); // 0 or negative value ... we remove those
}
 
pdr.update(sid, 1, 0, changes, removes); // giving lists of updates and letting the pdr do them for us
 
// Reading version 1 from the pdr
pdr.uget(sid, 1, usv);
 
// and now we can use usv that holds version 1 with all the changes we wanted
 
 
```
 
### Efficiency, versions pointing and iterating over versions
In many cases all the different time versions are actually identical, for example in all the cases where a calculation is looking ONLY at time point before the given time point. This property can and should be used to make the code more efficient, in the sense of eliminating the time needed to prepare a copy for each version and applying processors/generators on each version, we only need to do this if the versions are different. This is done using the next two mechanisms:
1. A version i can point to a version j : this means version j actually keeps the data , and version i is a soft copy of it, that is only pointing to the data of version j. It will be split into its only at the exact point in which this is needed.
2. When writing a processor that changes versions, we can use the versions iterators which give us in each iteration round the set of the versions that is the same:
  
1. If our operation is not creating new versions: we simply change the "source" version, and all other versions will point to it.
  
2. If our operation changes versions : we need to safely work on the current set and split it to new sets.
Examples, and major related API's
```c++
// Some useful APIS
class PidDynamicRec : public PidRec {
// ...
 
// will point version v_dst to the data of version v_src
int point_version_to(int sid, int v_src, int v_dst);	
 
// test if two versions point to the same place in memory
	int versions_are_the_same(int sid, int v1, int v2);
	int versions_are_the_same(set<int> sids, int v1, int v2); // same for a set of signals
 
// ...
}
 
 
// iterators: iterating on blocks of similar data versions
class differentVersionsIterator : public versionIterator {
	int jVersion;
// ...
	int init(); // initialize iterator
	int next(); // go to next block, note that it will make SURE all the versions are pointed to iVersion, the version that actually holds the data for this block. 
				// hence this iterator is good ONLY if you do not create new versions and need to break the pointings.
				// For other cases use the very similar allVersionsIterator and check versions one by one to make sure what needs to be done.
	bool done() { return iVersion < 0; } // test of loop
	inline int block_first() { return jVersion+1; } // get first version in block (all versions point to it)
	inline int block_last() { return iVersion; } // get last version in block (blocks are always of adjacent versions)
};
 
```
 
Examples for actual iterating over versions
```c++
_apply(PidDynamicRec& rec, vector<int>& time_points, ... ) {
 
	// Example 1 : simple iterating, in a case that does not need to break the versions pointing
	
	differentVersionsIterator vit(rec, reqSignalIds); // initializing iterator with the set of all the needed signals (blocks are always relative to a set of signals)
 
	for (int iver = vit.init(); !vit.done(); iver = vit.next()) {
 
		// now we are in a block of versions starting at:
		// vit.block_first()
		// ending at :
		// iver which is exactly vit.block_last() , and is also the version all other versions will point to.
 
		// put here the code that changes version iver for your signals, and you're all set !!
		
	}
 
}
```
 
 
