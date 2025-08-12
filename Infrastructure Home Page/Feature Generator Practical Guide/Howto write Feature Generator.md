# How to Write a Feature Generator
A Feature Generator is a processing unit that takes raw input signals directly from a data repository or EMR.
Its process has two main stages:

- It runs all relevant rep processors to pre-process the input signals. This prepares the data before it can be used to generate new features. This is being called by the infrastructure.
- It calls the generate function, which receives this pre-processed, patient-specific data and produces the final output.

Feature Generators in MedModel follow a specific sequence of method calls. Here’s the typical lifecycle:

1. **Constructor**
   - Initializes the Feature Generator object.

2. **init_defaults()**
   - Sets default values for the generator. please update `generator_type` to hold genertor type

3. **Initialization**
   - During learning:  
     `init(map<string, string>& mapper)` parses parameters from a key-value map (using `SerializableObject::init_from_string`).
     Please make sure to update `req_signals` as required input signals for the feature generator
     please set `tags` variable 
   - During application:  
     Arguments are loaded from disk. Parameters stored via `ADD_SERIALIZATION_FUNCS` are restored automatically.

4. **fit_for_repository(MedPidRepository)**
   - Adapts the generator to the repository, e.g., modifies logic if certain signals are missing.

5. **Signal Requirements and Setup**
   - `get_required_signal_ids()`  
     Returns the list of required signal IDs for learning or applying the generator.
   - `set_required_signal_ids(MedDictionarySections)`  
     Stores required signal IDs using dictionary sections.
   - `set_signal_ids(MedSignals)`  
     Stores required signal IDs using signal objects.
   - `init_tables(MedDictionarySections)`  
     Initializes tables and stores needed signal IDs using dictionary sections.
   - `set_names` - stores the output names of the feature generator - please override.
   

6. **Feature Filtering**
   - `filter_features()`  
     Determines if this generator is needed (e.g., after feature selection). Returns `true` if the generator should be kept. Uses by default `names` variable set by `set_names` to check if the feature generator is needed and if one of his output names is needed in the pipeline.

7. **Signal Names**
   - `get_required_signal_names()`  
     Returns all signal names needed to run this generator.

8. **Learning Phase**
   - `learn()`  
     Performs learning logic (called only during training).

9. **Preparation**
   - `prepare()`  
     Prepares features, attributes, and allocates space.

10. **Output Initialization**
    - `get_p_data()`  
      Initializes the address for the generator’s output (useful for parallelism).

11. **Feature Generation**
    - `generate()`  
      Generates the feature for each sample. The infrastructure already execuated all relavent rep processors for the desired input signals the feature generator is using. 

12. **Summary**
    - `make_summary()`  
      Summarizes results after generation (e.g., collects statistics across all data).

---

## Steps to Implement a Feature Generator

1. **Create Class Files**
   - Make a new `.h` header and `.cpp` source file for your feature generator class. Include `"FeatureGenerator.h"` in your header.

2. **Set Default Values**
   - Implement `init_defaults()` or set defaults in the constructor.

3. **Parameter Initialization**
   - Override `init(map<string, string>& mapper)` to parse external parameters.

4. **Serialization**
   - Add `MEDSERIALIZE_SUPPORT($CLASS_NAME)` at the end of your header file (replace `$CLASS_NAME`).
   - Add `ADD_CLASS_NAME($CLASS_NAME)` in the public section of your class.
   - Use `ADD_SERIALIZATION_FUNCS` to specify which parameters should be saved after learning. Exclude temporary or repository-specific variables.

5. **Signal and Table Setup**
   - Implement or override (if needed):
     - `set_names` Update feature generator output features
     - `get_required_signal_ids()` and `get_required_signal_names()` - only if needed. The deafult is to use `req_signals`
     - `set_required_signal_ids(MedDictionarySections)`  - only if needed. The deafult is to use `req_signals`
     - `set_signal_ids(MedSignals)` - only if needed to do more setup. 
     - `init_tables(MedDictionarySections)`
     - `get_required_signal_categories` - if the feature generator uses categorical signals - this will need to list all "required" categorical values the feature generator is using

6. **Feature Filtering**
   - Overide (if needed) `filter_features()` if your generator should be skipped under certain conditions (e.g., after feature selection). The default is to use `names` to identify if the feature generator is needed.

7. **Learning and Preparation**
   - Implement `learn()` for training logic (if needed).
   - Implement `prepare()` to allocate resources and set up attributes.

8. **Feature Generation**
   - Implement `generate()` to produce the feature for each sample.
   - Implement `get_p_data()` if your generator supports parallel output.

9. **Summary**
   - Implement `make_summary()` to collect and report statistics after feature generation.

10. **Register Your Feature Generator in header file** in `FeatureGenerator.h`
   - register a new type in `FeatureGeneratorTypes` before `FTR_GEN_LAST` In the documentation comment, specify the name in `FeatureGeneratorTypes` for Doxygen reference. 

11. **Register Your Feature Generator in cpp file** `FeatureGenerator.cpp`
   - Add your type conversion to `ftr_generator_name_to_type`
   - Add your class to `FeatureGenerator::new_polymorphic`
   - Add your class to `FeatureGenerator::make_processor(FeatureGeneratorTypes generator_type)`

---

**Tip:**  
Follow the structure and naming conventions used in existing feature generators for consistency and easier maintenance.
