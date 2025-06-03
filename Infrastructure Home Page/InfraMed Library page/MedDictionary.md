# MedDictionary
The MedDictionary class is a wrapper for several methods needed to connect a numerical int value to a string. Since a MedRepository does not have the ability to hold free text at the moment, and also since it is highly inefficient to do this (for example when using the same long names again and again in Drugs or read codes) MedRepository works currently only with numerical values.
Thus, when for example loading drugs information into the repository we will only load some numerical number representing the specific drug. The dictionary allows us to translate this number into the text describing the drug.
Along with that basic feature, a dictionary allows the definition of sets of values and give them a new name. This is extremely useful when trying to use hierarchies of classifications on the raw data such as for example : read codes or ICD9, ICD10, SnowMed for Diagnosis and procedures, or ATC or BNF for drugs, or specific cancer types in a cancer registry, etc...
Several efficient ways of testing if a given read code is inside a specific set (or group of sets) are given as well.
Another issue dealt with is managing several different dictionaries to work together even if the same numerical code appears in both of them. This is done using the sections mechanism.
### Dictionary files format
The dictionary files are read when a repository is loaded, and have the following format rules:
- Empty lines or lines starting with # are ignored (to allow for comments)
- All other lines are tab delimited
- section definition: SECTION <comma seprated list of names for the section> 
  - yes - each section can have several different names. This is useful, see below on sections and how to use them.
  - our consensus is to have in a section all the signal names that are relevant to it.
- simple value to string name definition: DEF <numerical int value> <string>
  - one can give several names to the same value, all are kept and can be later used.
  - each set defined should have a DEF line as well for the set name.
  - uniqueness from int value to string value is obviously necessary in order to be able to find an int id given the string name.
- defining sets inclusions: SET <set name> <member name>
  - sets of sets are good to go. avoid cyclic definitions.
**Example lines for a signals file**
```
 
# example section line
SECTION RC_Diagnosis,Cancer_Location,DM_Registry,HT_Registry,CVD_MI,CVD_HeartFailure,CVD_HemorhagicStroke,CVD_IschemicStroke,CKD_State,DEATH
 
# example def lines
DEF     0       DM_Registry_Non_diabetic
DEF     1       DM_Registry_Pre_diabetic
DEF     2       DM_Registry_Diabetic
# example set definition
 
# first - sets must get a unique numerical value of their own
DEF     21000   Colon_Cancer
DEF     21001   CRC_Cancer
DEF     21002   Stomach_Cancer
DEF     21003   Rectum_Cancer
# second - sets memberships are defined , note that a set can be a member of another set.
SET     Colon_Cancer    Digestive Organs,Digestive Organs,Colon
SET     Stomach_Cancer  Digestive Organs,Digestive Organs,Stomach
SET     Rectum_Cancer   Digestive Organs,Digestive Organs,Rectum
SET     CRC_Cancer      Colon_Cancer
SET     CRC_Cancer      Rectum_Cancer
SET     CRC_and_Stomach_Cancer  CRC_Cancer
SET     CRC_and_Stomach_Cancer  Stomach_Cancer
 
```
 
### MedDictionary vs. MedDictionarySections
MedDictionary is a class for a single dictionary with a single space of numerical values.
MedDictionarySections is a class holding several dictionaries , each in its own section, and has the API's to manage different sections.
### Initializing dictionaries
When using a med repository, dictionaries are initialized automatically upon initilizing the repository, from the dictionary files given in the repository config file.
The easiest way to initialize a dictionary is to use the read(vector<string> &input_dictionary_files) , these are implemented for both MedDictionary and MedDisctionarySections.
We typically use a dictionary only within a MedRepository context.
However - it is possible to use this mechanism directly for any other need as well.
### Main MedDictionary methods
- int id(const string &name) : from name to id.
- string name(int id) : from id to name : if several names were given to an id, this will return the last of those names.
- map<int, vector<string>> Id2Names : this map maps an id to a vector of ALL its names.
- int is_in_set(int member_id, int set_id) : test if member id is in the set set_id.
- int is_in_set(const string& member, const string& set_name) : same but for string names of member and set
- int prep_sets_lookup_table(const vector<string> &set_names, vector<char> &lut) : when in need of scanning for memberships is_in_set() is a too slow. This method efficiently creates a look up table from all possible ids to 0/1 that can later be used to scan for membership MUCH faster.
- int prep_sets_indexed_lookup_table(const vector<string> &set_names, vector<unsigned char> &lut) : same as previous but the lookup table will note the serial number (up to 255...) of the set the member is contained in. This allows for a scan on several disjoint sets together.
 
### Main MedDictionarySections methods
- int section_id(const string &name) : translates a section name to a section id.
- vector<MedDictionary> dicts : get a direct access to the dictionary given its section_id, from there on ... simply use all the methods of MedDictionary.
 
### Code Examples
**MedDictionary code example **
```c++
MedRepository rep;
 
// init rep ... this initialized the dict inside it which is a MedDictionarySections object ...
 
// print default name of a given drug signal (suppose we read it into an int drug_val)
int section_id = rep.dict.section_id("Drug");
cout << " name of Drug code " << drug_val << " is " << rep.dict.dicts[section_id].name(drug_val);
 
// a more complex example going over a list of pids and find for each one 
// if and when they use a drug included in some list of drug sets.
// to make it more interesting we use a universal signal to read the Drug signal
vector<int> pids;
 
// ... assume pids is populated with a long list of pids
 
vector<string> drug_sets = {"ATC_B04A_B__","ATC_C10A_A__","ATC_B01A____"}; // sets for Statins or Aspirin
 
// first we prepare a look up table to use
vector<char> lut;
rep.dict.dicts[rep.dict.section_id("Drug")].prep_sets_lookup_table(drug_sets, lut);
 
UniversalSigVec usv; // to be used later
int drug_sid = rep.sigs.sid("Drug"); // good practice for efficiency in loops
 
// go over pids
for (auto &pid : pids) {
	// read drugs vector for pid
	rep.uget(pid, drug_sid, usv);
 
	// go over vector and test inclusion in lut
	for (int i=0; i<usv.len; i++) {
		int drug_val = (int)usv.Val(i, 0); // get Value of element i at val channel 0
		if (lut[drug_val]) // actual test the membership criteria ... much faster than the is_in_set() options
			cout << "Patiet " << pid << " is using drug code " << drug_val << " at time " << usv.Time(i,0); // print
	}
}
 
 
```
