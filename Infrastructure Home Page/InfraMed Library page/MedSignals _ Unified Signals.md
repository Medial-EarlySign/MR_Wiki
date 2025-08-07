# MedSignals / Unified Signals

MedSignals is an internal class in MedRepository that defines signal types and manages `.signals` files—dictionaries mapping signal names to their properties. Each MedRepository instance has a `sigs` object for basic `.signals` operations. All signal definitions are found in `MedSignals.h`.

When initializing a repository, one of the first steps is to read the signals configuration file (specified in the repository config) and set up all signal definitions.

### What is a signal?

A signal type is a class defined in `MedSignals.h` and acts as a placeholder for signals. Signals represent actual data stored in the repository, each with a specific type. For example:

- *BYEAR*, *GENDER*, *TRAIN*: Store a single float value, typically using the `SVal` type, or as a generic signal with one integer value channel: "V(i)"
- *Hemoglobin*, *Creatinine*: Store a date and a float value, using `SDateVal` or `STimeVal`, or as a generic signal with one integer time channel and one float value channel: "T(i),V(f)"
- *BP*: Stores a date and two short values (diastolic and systolic blood pressure), using `SDateShort2`, or as a generic signal: "T(i),V(s,s)"

Each signal has several properties, defined in the `SignalInfo` class:

- *name*: Signal name
- *type*: Type code (from the `SigType` enum) or a generic type string. You can use `get_signal_generic_spec()` on `UniversalSigVec` to get its generic signal string representation.
- *sid*: Unique integer signal ID from the signals config file, used for fast indexing and efficient access. Maximum SID is `MAX_SID_NUM` (currently 100,000).
- *bytes_len*: Number of bytes needed to store one element.
- *n_time_channels*: Number of time channels.
- *n_val_channels*: Number of value channels.

Signals must currently have a fixed size.

### Unified Signals - Part I

Most medical record signals can be described as having zero or more time channels and zero or more value channels. Examples:

- *BYEAR*: 0 time channels, 1 float value channel
- *Creatinine*: 1 integer time channel, 1 float value channel
- *BP*: 1 integer time channel, 2 float value channels
- *DM_Registry*: 2 integer time channels, 1 int/char value channel

When time channels are integers and value channels are floats, signals can be accessed in a unified way, regardless of their type. This allows for generalized code in components like `RepProcessors` and `FeatureGenerators` in MedProcessTools.

See Part II for usage examples.

### Current Signal Types

All signal types are defined in `MedSignals.h`. Available types include:

| Signal Type      | Time Channels | Value Channels | Placeholders                | Example Signals         |
|------------------|--------------|---------------|-----------------------------|------------------------|
| SVal             | 0            | 1             | float                       | BYEAR, TRAIN, GENDER   |
| SDateVal         | 1            | 1             | int : float                 | Hemoglobin, Creatinine |
| STimeVal         | 1            | 1             | long long : float           | Creatinine (mimic)     |
| SDateRangeVal    | 2            | 1             | int, int : float            | DM_Registry            |
| STimeRangeVal    | 2            | 1             | long long, long long : float| (mimic)                |
| STimeStamp       | 0            | 1             | : long long                 | (mimic)                |
| SDateVal2        | 1            | 2             | int : float, unsigned short | Drugs (MHS)            |
| STimeLongVal     | 1            | 1             | long long : long long       | (mimic)                |
| SDateShort2      | 1            | 2             | int : short, short          | BP                     |
| SValShort2       | 0            | 2             | : short, short              | (mimic)                |
| SValShort4       | 0            | 4             | : short, short, short, short| (mimic)                |

### Adding a New Signal Type

To add a new legacy signal type:

1. Add an enum value for the type (used for encoding in the signals file).
2. Define the signal class and its methods.
3. Update `MedConvert` to read the new signal type (add parsing logic if needed).
4. Make sure the new signal class inherits from `UnifiedSig` for unified signal compatibility.
5. Implement these methods:
   - `n_time_channels()`
   - `n_val_channels()`
   - `time_unit()`
   - `int Time(int chan)`
   - `float Val(int chan)`
   - `SetVal(chan, _val)`
   - `Set(int *times, float *vals)`
   - Comparison operators (`<`, `==`)
   - Output operator (`<<`)

### Unified Signals - Part II

To work with unified signals, use the `UniversalSigVec` (`usv`) class. Instead of the standard `get()` method, use `uget()` to load signal data into a `usv` object. Key features:

- Initialize for a specific signal type using only the enum.
- Use `uget()` to load data (no copies; uses pointers and virtual functions).
- Access any time or value channel uniformly across all signal types.

This lets you write type-independent code. Initialization has a performance cost, but repeated use with the same type is efficient.

#### Example Usage

```c++
// Initialize repository and UniversalSigVec
MedRepository rep;
UniversalSigVec usv;

// ... initialize repository ...

rep.uget(pid, sid, usv);

// Print all time and value channels for each element
for (int i = 0; i < usv.len; i++) {
    for (int t_ch = 0; t_ch < usv.n_time_channels(); t_ch++)
        cout << "Element " << i << ", time channel " << t_ch << ": " << usv.Time(i, t_ch);
    for (int v_ch = 0; v_ch < usv.n_val_channels(); v_ch++)
        cout << "Element " << i << ", value channel " << v_ch << ": " << usv.Val(i, v_ch);
}

// Usage with PidRec
MedPidRepository pid_rep;
PidRec rec;

// ... initialize pid_rep ...

pid_rep.get_pid_rec(pid, rec);
rec.uget(sid, usv);
```

### Signals Config File

For details on the [signals file](/Repositories/Signal/Repository%20Signals%20file%20format)

