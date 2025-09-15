# Virtual Signals

Sometimes, it's necessary to dynamically add new signals to a repository, assigning them unique names and types, and enabling data insertion. This approach is especially useful when calculating features for specific problems, as storing features or intermediate results as new signals often simplifies the process.

**Example:**  
If eGFR is not available in your repository (or you need a different calculation method), and you want to generate features like last, min, max, or average values across various time windows, the best solution is to create a virtual signal for eGFR. You can then calculate its values in memory, add them to the repository, and use this signal like any other for feature generation.

## Defining Virtual Signals

To create a virtual signal, use the `insert_virtual_signal` API from `MedSignals.h`:

- `int insert_virtual_signal(const string &sig_name, int type)` or `int insert_virtual_signal(const string &sig_name, const string& signalSpec)` with generic string definition
    - `sig_name`: The new signal's name (must be unique within the repository)
    - `type`: The signal's data type or signalSpec for [generic signal](../00.InfraMed%20Library%20page/Generic%20(Universal)%20Signal%20Vectors.md) definition

This function validates the input and sets up the necessary internal structures.

## Adding Data to a Virtual Signal

There are two main methods:

1. **In-memory mode:**  
   The repository operates entirely in memory, allowing you to add or remove data freely. Refer to the relevant documentation for details.

2. **Dynamic records:**  
   Use the dynamic records API (see [PidDynamicRec](../00.InfraMed%20Library%20page/PidDynamicRec.md)) to modify or add signal data. This method is used in the MedProcessTools library and is described below.

In MedProcessTools, rep processor stages run first, each with `learn` and `apply` methods. For virtual signals that only require calculation (not learning), you simply need to compute and insert the new signal. More complex cases involve learning parameters or models, which are then used for signal calculation. The most advanced scenarios involve virtual signals needed during the learning stage of another processor or feature generator, which are not fully supported yet.

During the apply stage, the library creates a `PidDynamicRec` for each patient, containing all necessary time points and signals for future processing. If the required virtual signals are already defined, you only need to add data to them:

- Calculate the time and value channels for your virtual signal at all relevant time points.
  - **Note:** If dynamic record versions differ, generate a separate data set for each version.
- Use one of these APIs in `PidDynamicRec`:
    - `int set_version_data(int sid, int version, void *datap, int len)`
        - `sid`: Signal ID (retrieve using `rep.sigs.sid(string name)`)
        - `version`: Target version
        - `datap`: Pointer to an array of the signal's type (e.g., `vector<sigType> data;` and use `&data[0]`)
        - `len`: Number of items
    - `int set_version_universal_data(int sid, int version, int *_times, float *_vals, int len)`
        - `sid`: Signal ID
        - `version`: Target version
        - `_times`, `_vals`: Arrays for time and value channels; if multiple channels exist, arrange them sequentially for each item
        - `len`: Number of items

If multiple versions should share the same data, you can link them using:

- `int point_version_to(int sid, int v_src, int v_dst);`

## Creating a Rep Processor for Virtual Signals

You can either write a processor from scratch or use the [`RepCalcSimpleSignals`](Rep%20Calculator.md) processor, which simplifies many common cases.

**From scratch:**
1. Each `RepProcessor` has a `virtual_signals_generic` vector (defined in the base class) to store all virtual signals it creates. Initialize this vector in the processor's `init()` function. The model will call `add_virtual_signals` at the appropriate time.
2. Implement `init()`, `init_tables()`, `learn()`, and `apply()` as needed.
3. When creating a new virtual signal:
   - Loop over dynamic record versions
   - Calculate the signal from the dynamic record
   - Insert it using either `set_version_data` or `set_version_universal_data`

**Using RepCalcSimpleSignals:**
The `RepCalcSimpleSignals` processor acts as a wrapper for simple virtual signal calculations. You can implement a new `SimpleCalculator` and integrate it via `RepCalcSimpleSignals::make_calculator`. Refer to the code for several straightforward examples.



