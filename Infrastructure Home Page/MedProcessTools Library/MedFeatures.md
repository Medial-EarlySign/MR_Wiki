# MedFeatures
### [MedFeatures ](http://node-04/Libs/html/classMedFeatures)is a data structure with helpers for holding features data as a virtual matrix.
MedFeatures [](http://node-04/Libs/html/classMedFeatures)is the data container used by MedModel to for holding the matrix used for learning/predicting.
A MedFeatures object contains a vector of samples (id + date + outcome + ...), a vector of weights (one per sample) and a vector of floats (one value per sample) for each features. Each feature is identified by it's name (a string)
Additional metadata per feature includes a [FeatureAttr ](http://node-04/Libs/html/classFeatureAttr)entry as well as a set of tags (string), which is used by FeatureProcess objects ro decide whether to act on the feature. 
### **Include file is - **
