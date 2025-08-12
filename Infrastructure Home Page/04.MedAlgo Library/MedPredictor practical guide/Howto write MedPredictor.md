# How to Write a MedPredictor

MedPredictor is Classifier/Regressor that inputs the features matrix and output prediction/s. 
It is being executed after [FeatureProcessors](../03.FeatureProcessor%20practical%20guide)

MedPredictor in MedModel follow a defined sequence of method calls. Here’s the typical lifecycle:

1. **Constructor**
   - Initializes the MedPredictor object.

2. **init_defaults()**
   - Sets default values for the predictor. Be sure to update `classifier_type` to reflect the predictor type.

3. **Initialization**
   - During learning:  
     Implement `init(map<string, string>& mapper)` to parse parameters from a key-value map (using `SerializableObject::init_from_string`).  
     Medial pipeline will initialize `features_count` and `model_features` that when we apply the modle we can make sure all and only needed features are inputed to the model.
     You might want to set `transpose_for_learn`, `transpose_for_predict` - if transpose of features matrix is needed for this type of predictor
     You might want to set (legacy and almost not used. Please use Feature Processors) to normalize the inputs: `normalize_for_learn`, `normalize_y_for_learn`, `normalize_for_predict`
   - During application:  
     Arguments are loaded from disk. Parameters stored via `ADD_SERIALIZATION_FUNCS` are restored automatically.

4. **Learning Phase**
   - `learn()`  
     Implements any learning logic needed during training.

5. **Applying Phase**
   - `apply()`  or `predict_single()` for single patient (more efficient setup for single patient, some preparation are done prior)
     Applies the predictor to calculate the score

## Steps to Implement a MedPredictor

1. **Create Class Files**
   - Create a new `.h` header and `.cpp` source file for your predictor class. Include `MedAlgo.h` in your header.

2. **Set Default Values**
   - Implement `init_defaults()` or set defaults in the constructor.

3. **Parameter Initialization**
   - Override `init(map<string, string>& mapper)` to parse external parameters.

4. **Serialization**
   - Add `MEDSERIALIZE_SUPPORT($CLASS_NAME)` at the end of your header file (replace `$CLASS_NAME`).
   - Add `ADD_CLASS_NAME($CLASS_NAME)` in the public section of your class.
   - Use `ADD_SERIALIZATION_FUNCS` to specify which parameters should be saved after learning. Do not include temporary or repository-specific variables.

5. **Learning**
   - Implement `learn()` for any required training logic.

6. **Apply**
   - Implement `apply()` to calculate the score. If there is more efficient calculate for single call, than also implement `predict_single()`

7. **Register Your Predictor in the Header (`MedAlgo.h`)**
   - Add a new type to `MedPredictorTypes` before `MODEL_LAST`. In the documentation comment, specify the name in `MedPredictorTypes` for Doxygen reference.

9. **Register Your Feature Processor in the Source (`MedAlgo.cpp`)**
   - Add your type conversion to `predictor_type_to_name` dictionary
   - Add your class to `MedPredictor::new_polymorphic`
   - Add your class to `MedPredictor::make_predictor(MedPredictorTypes model_type)`

