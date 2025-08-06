# How to Write a PostProcessor

A PostProcessor is a component that takes the feature matrix and prediction results, then applies additional post-processing steps. It is executed after the [MedPredictor](../MedPredictor%20practical%20guide) stage in the pipeline.

PostProcessors in MedModel follow a defined sequence of method calls. Here’s the typical lifecycle:

1. **Constructor**
   - Initializes the PostProcessor object.

2. **init_defaults()**
   - Sets default values for the processor. Make sure to update `processor_type` to indicate the processor type.

3. **Initialization**
   - During learning:  
     Implement `init(map<string, string>& mapper)` to parse parameters from a key-value map (using `SerializableObject::init_from_string`).  
     If your PostProcessor should operate on a specific subset of training samples, set either `use_p` or `use_split`:
     - `use_split`: Uses the "split" stored in MedSamples. All splits (based on patient ID) except the selected one are passed to the full model pipeline; the selected split is reserved for training this PostProcessor.
     - `use_p`: A value between 0 and 1 that determines the proportion of randomly selected patient IDs passed to the PostProcessor. The remainder is processed by the main MedModel pipeline.  
     This mechanism also supports multiple PostProcessors, each working on a different subset of the data.
   - During application:  
     Arguments are loaded from disk. Parameters stored via `ADD_SERIALIZATION_FUNCS` are restored automatically.

4. **Pipeline Integration**
   - `init_post_processor()`:  
     Initializes the PostProcessor using the complete MedModel pipeline, allowing for any necessary adaptations before execution.

5. **Learning Phase**
   - `Learn()`:  
     Implements any learning logic required during training.

6. **Application Phase**
   - `Apply()`:  
     Applies the post-processing logic to the data.

---

## Steps to Implement a PostProcessor

1. **Create Class Files**
   - Create a new `.h` header and `.cpp` source file for your PostProcessor class. Include `PostProcessor.h` in your header.

2. **Set Default Values**
   - Implement `init_defaults()` or set defaults in the constructor.

3. **Parameter Initialization**
   - Override `init(map<string, string>& mapper)` to parse external parameters.

4. **Serialization**
   - Add `MEDSERIALIZE_SUPPORT($CLASS_NAME)` at the end of your header file (replace `$CLASS_NAME`).
   - Add `ADD_CLASS_NAME($CLASS_NAME)` in the public section of your class.
   - Use `ADD_SERIALIZATION_FUNCS` to specify which parameters should be saved after learning. Exclude temporary or repository-specific variables.

5. **Pipeline Adaptation (if needed)**
   - Implement `init_post_processor()` if your PostProcessor needs to adapt based on the full MedModel pipeline.

6. **Define Dependencies and Outputs**
   - Implement `get_input_fields()` and `get_output_fields()` to specify the inputs and outputs of your PostProcessor.  
     - For features, prefix the name with `"feature:"`.
     - For predictions, use `"prediction:X"` (where X is the prediction index, usually 0).
     - For other sample effects, use `"attr:"`, `"str_attr:"`, or `"json:"` as appropriate.  
     The MedModel pipeline uses this information to determine if the PostProcessor is required.

7. **Learning**
   - Implement `Learn()` for any required training logic.

8. **Apply**
   - Implement `Apply()` to perform the post-processing.

9. **Register Your PostProcessor in the Header (`PostProcessor.h`)**
   - Add a new type to `PostProcessorTypes` before `FTR_POSTPROCESS_LAST`. In the documentation comment, specify the name in `PostProcessorTypes` for Doxygen reference.

10. **Register Your PostProcessor in the Source (`PostProcessor.cpp`)**
    - Add your type conversion to `post_processor_name_to_type`
    - Add your class to `PostProcessor::new_polymorphic`
    - Add your class to `PostProcessor::make_processor(MedPredictorTypes model_type)`

---

**Tip:**  
Follow the structure and conventions of existing PostProcessors for consistency and easier integration into the MedModel framework.

