# Feature Importance
The Feature Importance is **virtual** function of MedPredictor called **calc_feature_importance**.
If you want to support Feature Importance for your predicotr you need to implement the virtual function: [calc_feature_importance](https://Medial-EarlySign.github.io/MR_LIBS/classMedPredictor.html#acd85e157d4b8fa20e8aa91a94e9fde2e)
Some notes:
- This function must be called after learn method only! otherwise and exception will be raised.
- The functions returns the features importance score in vector with same order of the learned features matrix order (sorted by ABC because we use map object).
Currently the method is implemented by:
- QRF - no additional parameters are required to run
- LightGBM - has a parameter "importance_type" which has 2 options: 
  - "gain" - the average gain of the feature when it is used in trees (in each split of tree node we have loss gain - averaging that)
  - "frequency" - the number of times a feature is used to split the data across all trees
- XGB - has a parameter "importance_type" which has 3 options: 
  - "gain" - the average gain of the feature when it is used in trees (in each split of tree node we have loss gain - averaging that)
  - "gain_total" - sum of gain the of the feature when it is used in trees (not normalized by number of appearances)
  - "weight" - the number of times a feature is used to split the data across all trees
  - "cover" - the average coverage of the feature when it is used in trees. it sums the number of samples in the leaves that in their path have this feature (so this feature was used to split and deciede on this observations). it calc's the average coverage
 
Example run for XGB
```c++
vector<float> feautres_scores;
MedPredictor *predictor = MedPredicotr::make_predictor("xgb"); //load trained model
MedFeatures data; //data.read_from_file(matrix_file); //load dataMatrix or already trained model
//predictor->learn(data); //or load trained model, otherwise it will throw exception
 
//now do learn and run again
predictor->calc_feature_importance(feautres_scores, "importance_type=gain"); //the second argument is additional parameters for feature importance
//sort and print features
map<string, vector<float>>::iterator it = data.data.begin();
vector<pair<string, float>> ranked((int)feautres_scores.size());
for (size_t i = 0; i < feautres_scores.size(); ++i) {
	ranked[i] = pair<string, float>(it->first, feautres_scores[i]);
	++it;
}
sort(ranked.begin(), ranked.end(), [](const pair<string, float> &c1, const pair<string, float> &c2)
{
	return c1.second > c2.second;
});
for (size_t i = 0; i < ranked.size(); ++i)
	printf("FEATURE %s : %2.3f\n", ranked[i].first.c_str(), ranked[i].second);
 
//QRF- have no additional options - empty string
//XGB - has parameter - "importance_type" with those options: "gain,weight,cover"
//LightGBM  - has parameter "importance_type" with those options: "frequency,gain". gain is like xgboost and frequency is like weight in xgboost
 
 
```
Using FeatureImportance as Selector:
cat /server/Work/Users/Alon/UnitTesting/examples/"general config files"/importance_example.json
```json
"process":{
            "process_set":"3",
            "fp_type":"importance_selector",
			"duplicate":"no",
			"numToSelect":"10",
			"predictor":"qrf",
			"predictor_params":"{type=categorical_entropy;ntrees=100;min_node=20;n_categ=2;get_only_this_categ=1;learn_nthreads=40;predict_nthreads=40;ntry=100;maxq=5000;spread=0.1}",
			"importance_params":"{}" //you may pass other parameters for feature importance in here. for example importance_type=gain
        }
```
