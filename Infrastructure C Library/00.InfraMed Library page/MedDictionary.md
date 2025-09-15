# MedDictionary

The `MedDictionary` class provides methods for mapping integer values to strings, which is essential since MedRepository does not support free text and relies on numerical codes for efficiency (e.g., drug names or read codes). This class enables translating these codes back to their textual descriptions.

Additionally, MedDictionary supports defining sets of values and assigning them names, which is useful for organizing hierarchical classifications (such as ICD codes, drug categories, or cancer types). Efficient membership testing for these sets is also provided.

To handle multiple dictionaries with potentially overlapping numerical codes, MedDictionary uses a sections mechanism.

### Dictionary File Format

When loading a repository, dictionary files are read with these rules:

- Ignore empty lines and lines starting with `#` (comments).
- All other lines are tab-delimited.
- **Section definition:**  
  `SECTION <comma-separated list of section names>`  
  Each section can have multiple names. Typically, a section contains all relevant signal names.
- **Value definition:**  
  `DEF <numerical int value> <string>`  
  Multiple names can be assigned to the same value. Each set must have a DEF line for its name. Each int value must be unique.
- **Set membership:**  
  `SET <set name> <member name>`  
  Sets can include other sets, but avoid cyclic definitions.

**Example dictionary file:**
```
# Section definition
SECTION RC_Diagnosis,Cancer_Location,DM_Registry,HT_Registry,CVD_MI,CVD_HeartFailure,CVD_HemorhagicStroke,CVD_IschemicStroke,CKD_State,DEATH

# Value definitions
DEF     0       DM_Registry_Non_diabetic
DEF     1       DM_Registry_Pre_diabetic
DEF     2       DM_Registry_Diabetic

# Set definitions (each set gets a unique int value)
DEF     21000   Colon_Cancer
DEF     21001   CRC_Cancer
DEF     21002   Stomach_Cancer
DEF     21003   Rectum_Cancer

# Set memberships
SET     Colon_Cancer    Digestive Organs,Digestive Organs,Colon
SET     Stomach_Cancer  Digestive Organs,Digestive Organs,Stomach
SET     Rectum_Cancer   Digestive Organs,Digestive Organs,Rectum
SET     CRC_Cancer      Colon_Cancer
SET     CRC_Cancer      Rectum_Cancer
SET     CRC_and_Stomach_Cancer  CRC_Cancer
SET     CRC_and_Stomach_Cancer  Stomach_Cancer
```

### MedDictionary vs. MedDictionarySections

- **MedDictionary:** Handles a single dictionary with one namespace for numerical values.
- **MedDictionarySections:** Manages multiple dictionaries, each in its own section, with APIs for section management.

### Initializing Dictionaries

Dictionaries are automatically initialized when a repository is loaded, using the dictionary files specified in the repository config.  
To manually initialize, use `read(vector<string> &input_dictionary_files)` for either MedDictionary or MedDictionarySections.  
Dictionaries are typically used within a MedRepository, but can be used independently.

### Key Methods

**MedDictionary:**

- `int id(const string &name)`: Get id from name.
- `string name(int id)`: Get name from id (returns the last name if multiple exist).
- `map<int, vector<string>> Id2Names`: Maps id to all its names.
- `int is_in_set(int member_id, int set_id)`: Check if member id is in set.
- `int is_in_set(const string& member, const string& set_name)`: Same as above, using names.
- `int prep_sets_lookup_table(const vector<string> &set_names, vector<char> &lut)`: Creates a fast lookup table for set membership.
- `int prep_sets_indexed_lookup_table(const vector<string> &set_names, vector<unsigned char> &lut)`: Similar, but notes the serial number of the set for each member.

**MedDictionarySections:**

- `int section_id(const string &name)`: Get section id from name.
- `vector<MedDictionary> dicts`: Access a dictionary by section id and use all MedDictionary methods.

### Code Example

```c++
// Initialize repository (which initializes MedDictionarySections)
MedRepository rep;

// Print the name for a drug code
int section_id = rep.dict.section_id("Drug");
cout << "Name of Drug code " << drug_val << " is " << rep.dict.dicts[section_id].name(drug_val);

// Scan a list of patient IDs for drug usage in specific sets
vector<int> pids; // Assume populated
vector<string> drug_sets = {"ATC_B04A_B__", "ATC_C10A_A__", "ATC_B01A____"}; // Example sets

// Prepare lookup table for fast membership testing
vector<char> lut;
rep.dict.dicts[rep.dict.section_id("Drug")].prep_sets_lookup_table(drug_sets, lut);

UniversalSigVec usv;
int drug_sid = rep.sigs.sid("Drug");

// Iterate over patients
for (auto &pid : pids) {
    rep.uget(pid, drug_sid, usv);
    for (int i = 0; i < usv.len; i++) {
        int drug_val = (int)usv.Val(i, 0);
        if (lut[drug_val])
            cout << "Patient " << pid << " is using drug code " << drug_val << " at time " << usv.Time(i,0); // Print usage
    }
}
```
