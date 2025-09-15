# How to Write a RepProcessor

RepProcessors in MedModel follow a defined lifecycle. Below is the typical sequence of method calls and their purpose:

1. **Constructor**
   - Initializes the RepProcessor object.

2. **init_defaults()**
   - Sets default values for the processor.

3. **Initialization**
   - During learning:  
     `init(map<string, string>& mapper)` parses arguments from a key-value map.
   - During application:  
     Arguments were loaded from disk (based on `ADD_SERIALIZATION_FUNCS`).

4. **fit_for_repository(MedPidRepository)**
   - Adapts the processor to the repository (e.g., creates virtual signals if needed).
   - During learning:
     * `get_required_signal_names()`  
       Identifies which signals are needed for processing.
     * `filter()`
     Determines if the processor should be applied, based on whether it affects any required signals. The list of affected signals is stored in the `aff_signals` variable. You can override the `filter` logic if needed.  

5. **Virtual Signal Management**
   - `add_virtual_signals()`  
     Lists virtual signals to generate and their types.
   - `register_virtual_section_name_id()`  
     Registers categorical virtual signals in the dictionary.

6. **Signal ID Setup**
   - `set_affected_signal_ids(MedDictionarySections)`  
     Defines output signal IDs.
   - `set_required_signal_ids(MedDictionarySections)`  
     Defines input signal IDs.
   - `set_signal_ids(MedSignals)`  
     Sets input/output signal settings (often overlaps with above).

7. **Final Initialization**
   - `init_tables(MedDictionarySections, MedSignals)`  
     Finalizes processor settings using repository data.

8. **Attribute Initialization**
   - `init_attributes()`  
     Sets up additional processor attributes in MedSamples. For example store fields to document outlier cleaning

9. **Signal Requirement**
    - `get_required_signal_names()`  
      (May be called again) Ensures all required signals are fetched.

10. **Application**
    - `conditional_apply(PidDynamicRec, MedIdSamples)`  
      Applies processor logic to patient data in memory. Uses `PidDynamicRec` which is editable in-memory repository for a single patient. It also protects us from changing data for other patients.

11. **Summary**
    - `make_summary()`  
      Generates a summary after processing (e.g., outlier percentages).  
      Useful for parallel execution and feature generation.

---

## Steps to Implement a RepProcessor:

1. Create a new `.h` file for your class and a corresponding `.cpp` file that includes the header. In the header, include `"RepProcess.h"`.
2. Set up default values in `init_defaults()` or the constructor. For example, set `processor_type` using `RepProcessorTypes` (optional).
3. Override `init(map<string, string>& mapper)` to parse external parameters.
4. Set up serialization:
   - Add `MEDSERIALIZE_SUPPORT($CLASS_NAME)` at the end of the `.h` file (replace `$CLASS_NAME`).
   - Add `ADD_CLASS_NAME($CLASS_NAME)` in the public section of your class.
   - Use `ADD_SERIALIZATION_FUNCS` to specify only the parameters that need to be stored on disk after learning. Do not include temporary or repository-specific variables.
5. Configure key variables for pipeline integration:
   - Assign `virtual_signals_generic` after `init` if your processor creates virtual signals.
   - Set `req_signals` to define required/input signals. This helps manage dependencies and ensures prerequisite processors run first. You can set this in `init_tables` or after `init`.
   - Set `aff_signals` to specify output/affected signals, aiding pipeline dependency tracking. This can also be set in `init_tables` or after `init`.
6. Override necessary functions as needed:
   - `register_virtual_section_name_id` (for virtual categorical signals)
   - `init_tables` (for initializing temporary variables using the repository - both in learn\apply)
   - `set_required_signal_ids`, `set_affected_signal_ids` (for custom signal ID logic; usually, using `aff_signals` and `req_signals` is sufficient)
   - `fit_for_repository` (for repository-specific adjustments, e.g., virtual signal checks) (optional).
   - `_learn` (override only if learning logic is needed; default is empty)
   - `_apply` (main logic for applying the processor)
   - `print` (optional for debugging)
   - Any other required virtual functions
7. Register your new RepProcessor in `RepProcess.h`:
   - Add a new type to `RepProcessorTypes` before `REP_PROCESS_LAST`. In the documentation comment, specify the name in `rep_processor_name_to_type` for Doxygen reference.
8. Register your new RepProcessor in `RepProcess.cpp`:
   - Add your class to `rep_processor_name_to_type`
   - Add your class to `RepProcessor::new_polymorphic`
   - Add your class to `RepProcessor::make_processor(RepProcessorTypes processor_type)`
  
