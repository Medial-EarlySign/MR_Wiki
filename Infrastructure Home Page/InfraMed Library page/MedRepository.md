# MedRepository

### Overview
`MedRepository` and its extension `MedPidRepository` are core classes in the InfraMed library, designed to facilitate reading, managing, and querying repository data. Familiarity with these classes is essential for effective use of the library.

### MedRepository vs. MedPidRepository
`MedPidRepository` builds on `MedRepository` by providing APIs to load a complete patient record ([`PidRec`](PidDynamicRec)). This is particularly useful when iterating over patient IDs and needing all associated data for each one.

### Initializing and Loading Data
There are several ways to initialize and load data into a `MedRepository`:

- **Using `read_all()`**  
  Loads the repository configuration, a list of signal names (or all signals if the list is empty), and a list of patient IDs (or all if empty). The function loads the full cartesian product of requested pids and signals into memory, making the repository ready for queries.

- **Using `init()`**  
  Initializes the repository with the configuration file, loading signals, dictionaries, and file locations, but not the actual data. Data can be loaded later using `load()` and released with `free()`.

- **Using `load()` and `free()`**  
  `load()` loads data for a specific signal and list of pids (or all if the list is empty).  
  `free()` releases memory for a specific signal, which is useful for handling large datasets.

#### Example: Initializing and Loading a Repository
```c++
// Define repository variable
MedRepository rep;

// Repository configuration file
string rep_conf = "/home/Repositories/THIN/thin.repository";

// Option 1: Load all signals and pids
rep.read_all(rep_conf);

// Option 2: Load specific signals and pids
vector<string> sigs = {"BDATE", "GENDER", "Glucose", "HbA1C", "BMI", "Drug"};
vector<int> pids = {5000001, 50000002, 10000000};
rep.read_all(rep_conf, pids, sigs);

// Option 3: Initialize without loading data
rep.init(rep_conf);

// Load a subset of signals and pids
rep.load(sigs, pids);

// Free signals from memory
rep.free(sigs);
rep.free_all_sigs();
```

### Accessing Data in MedRepository
Once data is loaded, you can access it using the `get()` function (Old API), which returns a time-sorted vector of values for a specific pid and signal. The result is a void pointer that should be cast to the appropriate signal type.
Please use `uget()` instead and get a generic signal of type [`UniversalSigVec`](MedSignals%20_%20Unified%20Signals)

#### Example: Accessing Data
```c++
// Repository variable
MedRepository rep;

// Assume repository is initialized and loaded

int pid;
string sig;

// Convert signal name to signal ID for performance
int sid = rep.sigs.sid(sig);

// Output variable for length
int len;

// Access DateVal signal with old API - Don't use it (and almost not exists anymore) 
SDateVal *sdv = (SDateVal *)rep.get(pid, sig, len);
// Access Generic signal with variable time and values channels
UniversalSigVec usv;
rep.uget(pid, sig, usv);


printf("read %d items\n", len);
if (len > 0)
    printf("First item: time %d, val %f. Last item: time %d, val %f\n", sdv[0].date, sdv[0].val, sdv[len-1].date, sdv[len-1].val);

// Faster access using signal ID - please use uget
sdv = (SDateVal *)rep.get(pid, sid, len);
rep.uget(pid, sid, usv);

// Access a different signal type - please use uget
SVal *sv = (SVal *)rep.get(pid, "BDATE", len);
rep.uget(pid, "BDATE", usv);
```

### MedPidRepository: Initialization and Usage
`MedPidRepository` enables loading data for individual pids into memory, which is useful for scanning large repositories with minimal memory usage. Each thread can hold data for a single patient, rather than all data at once.

To use `MedPidRepository`, ensure the repository is transposed during its creation. After setup, use a `PidRec` object to store data for a specific patient ID and access signals with either `get()` or `uget()`.

#### Example: Using MedPidRepository and PidRec
```c++
// Create MedPidRepository and PidRec instances
MedPidRepository pid_rep;
PidRec rec;

// Initialize the repository
pid_rep.init(rep_conf_file);

// Load data for a specific patient
pid_rep.get_pid_rec(pid, rec);

// Access a signal using the legacy API
SDateVal *sdv = rec.get(sig_name, len);

// Access a signal using the recommended API
UniversalSigVec usv;
rec.uget(sig_name, usv);
```

You can also initialize a `PidRec` from an existing `MedRepository` using `init_from_rec()`. This copies the patient record and allows for dynamic modifications.

#### Example: Initializing PidRec from MedRepository
```c++
MedRepository rep;
PidRec rec;

// Repository should be initialized as shown earlier

vector<int> sids; // Leave empty to load all signals
rec.init_from_rec(&rep, pid, sids);
```

### Performance Tips
- Store repositories locally (e.g., `/home/Repositories` on Linux) for optimal speed.
- When processing many patient IDs, use signal IDs instead of names for faster lookups:
  ```c++
  int pid;
  string sig_name;
  int sid = rep.sigs.id(sig_name);
  UniversalSigVec usv;

  for (...) {
      rec.uget(sig_name, usv);
      // ...process data...
  }
  ```
- Load only the signals you need
