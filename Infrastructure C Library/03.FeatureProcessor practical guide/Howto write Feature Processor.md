# How to Write a Feature Processor

Feature Processors are components that operate on the feature matrix produced by the [Feature Generator](../02.Feature%20Generator%20Practical%20Guide). They take a matrix of features as input, process it (e.g., normalization, feature selection, PCA), and output a transformed feature matrix.

Feature Processors in MedModel follow a defined sequence of method calls. Here’s the typical lifecycle:

1. **Constructor**
   - Initializes the Feature Processor object.

2. **init_defaults()**
   - Sets default values for the processor. Be sure to update `processor_type` to reflect the processor type.

3. **Initialization**
   - During learning:  
     Implement `init(map<string, string>& mapper)` to parse parameters from a key-value map (using `SerializableObject::init_from_string`).  
     If your processor affects a single feature, you may want to use `feature_name` to specify the output feature.
   - During application:  
     Arguments are loaded from disk. Parameters stored via `ADD_SERIALIZATION_FUNCS` are restored automatically.

4. **Repository Setup**
   - Calls `set_feature_name` to configure the processor using repository information.

5. **Feature Filtering**
   - Methods like `update_req_features_vec`, `are_features_affected`, and `filter` determine if this Feature Processor is needed for prediction.  
     If the processor does not affect any required features, it will be skipped.  
     By default, `filter` uses `feature_name` to check if the processor is necessary.

6. **select_learn_matrix**
   - Usually not required. In special cases, you may want to create a copy of the original feature matrix and store it under a different name for use by other processors in the pipeline.

7. **Learning Phase**
   - `learn()`  
     Implements any learning logic needed during training.

8. **Feature Processing**
   - `apply()`  
     Applies the processor logic to the feature matrix.

---

## Steps to Implement a Feature Processor

1. **Create Class Files**
   - Create a new `.h` header and `.cpp` source file for your feature processor class. Include `"FeatureProcess.h"` in your header.

2. **Set Default Values**
   - Implement `init_defaults()` or set defaults in the constructor.

3. **Parameter Initialization**
   - Override `init(map<string, string>& mapper)` to parse external parameters.

4. **Serialization**
   - Add `MEDSERIALIZE_SUPPORT($CLASS_NAME)` at the end of your header file (replace `$CLASS_NAME`).
   - Add `ADD_CLASS_NAME($CLASS_NAME)` in the public section of your class.
   - Use `ADD_SERIALIZATION_FUNCS` to specify which parameters should be saved after learning. Do not include temporary or repository-specific variables.

5. **Custom Setup (if needed)**
   - Implement or override:
     - `filter` (update logic if your processor affects a specific set of features)

6. **Learning**
   - Implement `learn()` for any required training logic.

7. **Apply**
   - Implement `apply()` to process the features.

8. **Register Your Feature Processor in the Header (`FeatureProcess.h`)**
   - Add a new type to `FeatureProcessorTypes` before `FTR_PROCESS_LAST`. In the documentation comment, specify the name in `FeatureProcessorTypes` for Doxygen reference.

9. **Register Your Feature Processor in the Source (`FeatureProcess.cpp`)**
   - Add your type conversion to `feature_processor_name_to_type`
   - Add your class to `FeatureProcessor::new_polymorphic`
   - Add your class to `FeatureProcessor::make_processor(FeatureProcessorTypes processor_type)`

---

**Tip:**  
Follow the structure and naming conventions of existing feature processors for consistency and easier maintenance.
