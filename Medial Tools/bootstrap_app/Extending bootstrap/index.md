# Extending bootstrap
The main idea of the bootstrap infrastructure is the ability to extend it to measure some statistical measurement in bootstrap analysis process (repeated experiment with replacement)  - to assest the confidence interval, std, etc.
In order to do that, you need to write function that calculates that measurement/s.
### Function input - you just need to keep that signature and can't change that.
- Lazy_Iterator *iterator - this is iterator that allows you to "fetch" the data for calculating the measurements. (It's lazy iterator to allow it to be efficient without allocating memory for each bootstrap experiment, but with doing the randomization process on the fly)
-  int thread_num - the thread num for parallelism - will be used by the "Lazy_Iterator"
- Measurement_Params *function_params - optional pointer to function parameters (can be null if not given). You can pass parameters to your function in this way
 
**How to use the iterator?**
You need to call "fetch_next" with thread_num, y, pred, w. IT will return true if you didn't reached to end of input. 
If you want to use if outside of "bootstrap.cpp" in the infrastructure, you will need to use "fetch_next_external" instead. The difference is that "fetch_next" is optimized and not exists outside of bootstrap.cpp, so you can't referred to it (The optimization is just slightly speedup).
You can also pass "ret_preds_order" to fetch_next when you have multiple predictions and your measurement function is more complicated (for example in multi label outcomes).
Arguments meanings:
y - it's the label/outcome
pred - the prediction/score
w - weight, if no weights than it's "-1". If your measurment doesn't support weights, please check that "w==-1" and throw error if you received weights
 
function_params - if the function has parameters, please check it is not "null" (if null please use default parameters), cast this object to your parameter object.
Measurement_Params is simple class that you need to extend if you want to specify parameters. For example class "ROC_Params". Example peace of used code in "calc_roc_measures_with_inc":
```c++
map<string, float> calc_roc_measures_with_inc(Lazy_Iterator *iterator, int thread_num, Measurement_Params *function_params) {
    ....
	ROC_Params default_params; //default ctor
	ROC_Params *params = &default_params
	if (function_params != NULL) 
		params = (ROC_Params *)function_params;	
	//Now use "params"
	
	//Example usage of fetching "max_diff_working_point" parameters into max_diff_in_wp
	float max_diff_in_wp = params->max_diff_working_point;
    ....
}
```
 
### Function output
The function returns "map" from string to float. the key of the map is the name of the measurement and the float is the corresponding value. In that way, you can calculate multiple measurements in a single function and give them names. 
When used, the infrastructure will append suffix for each measurement: "_Mean", "_Std", "_CI.Lower.95", "_CI.Upper.95", "_Obs" as in this page: [Bootstrap legend](../Bootstrap%20legend.md)
### Here is a simple example of function that counts how many cases and how many controls exists:
```c++
map<string, float> calc_npos_nneg(Lazy_Iterator *iterator, int thread_num, Measurement_Params *function_params) {
	map<string, float> res;
	map<float, int> cnts;
	float y, w, pred;
	while (iterator->fetch_next(thread_num, y, pred, w))
		cnts[y] += w != -1 ? w : 1;
	res["NPOS"] = (float)cnts[(float)1.0];
	res["NNEG"] = (float)cnts[(float)0];
	return res;
}
```
This function iterates through the data and "counts" how many of each outcome we see in the data and stores it in "cnt" variable. It also supports weights.
 
## How to use the custom function?
****
 Expand source
```c++
#include <MedStat/MedStat/MedBootstrap.h>
 
//Let's assume that you wrote custom function like calc_npos_nneg and you called it: "MY_CUSTOMIZED_MEASURMENT_FUNCTION"
map<string, float> MY_CUSTOMIZED_MEASURMENT_FUNCTION(Lazy_Iterator *iterator, int thread_num, Measurement_Params *function_params) {
....
}
 
//Let's assume you have "arguments" for you function in class Custom_Measurement_Parameters: 
class Custom_Measurement_Parameters : public Measurement_Params {
public:
	int min_bin_size = 0;
	float cases_weight = 1;
	float controls_weight = 1;
};
//Helper function to generate matrix for filtering... Will be only used/needed if you want to generate cohorts and do filtering with bootstrap 
void get_mat(const string &json_model, const string &rep_path, MedSamples &samples, MedModel &mdl) {
	
	if (!json_model.empty())
		mdl.init_from_json_file(json_model);
	else
		MLOG("No json for bootstrap - can only use Time-Window,Age,Gender filters\n");
	bool need_age = true, need_gender = true;
	for (FeatureGenerator *generator : mdl.generators) {
		if (generator->generator_type == FTR_GEN_AGE)
			need_age = false;
		if (generator->generator_type == FTR_GEN_GENDER)
			need_gender = false;
	}
	if (need_age)
		mdl.add_age();
	if (need_gender)
		mdl.add_gender();
	vector<int> pids_to_take;
	samples.get_ids(pids_to_take);
 
	MedPidRepository rep;
	mdl.load_repository(rep_path, pids_to_take, rep, true);
	
	if (mdl.learn(rep, &samples, MedModelStage::MED_MDL_LEARN_REP_PROCESSORS,
		MedModelStage::MED_MDL_APPLY_FTR_PROCESSORS) < 0)
		MTHROW_AND_ERR("Error creating features for filtering\n");
}
 
int main(int argc, char *argv[]) {
	//String argument for controlling bootstrap parameters, as in the example. To see full parameters, refer to "MedBootstrap::init".
	// It has default - so you can keep that empty, skip the call for "bt.bootstrap_params.init_from_string" if you want the default. 
	//You can also change the parameters programically by accessing them: "bt.bootstrap_params.loopCnt=500;"
	string bt_params = "loopcnt=500;sample_per_pid=1"; 
	MedBootstrapResult bt;
	bt.bootstrap_params.init_from_string(bt_params);
 
	//Your custom mearument parameters:
	Custom_Measurement_Parameters custom_args;
 
	string json_model; //optional argument to generate features for filtering cohorts in the bootstrap
	string cohorts_file; // path to bootstrap cohorts definitions. If not specify (no need for json_model, rep_path), will not filter the samples and will create "All" cohort with all samples and no filtering.
	string rep_path; // path to repository in case you need to filter and you specified "cohorts_file" that is not just "Time-Window".
 
	MedSamples	preds; // Your MedSamples with predictions
	preds.read_from_file("YOUR_SAMPLES_PATH");
 
	if (!cohorts_file.empty())
		bt.bootstrap_params.parse_cohort_file(cohorts_file);
	// The measurement functions. The default is vector with single element of "calc_roc_measures_with_inc"
	vector<pair<MeasurementFunctions, Measurement_Params *>> &cl_m = bt.bootstrap_params.measurements_with_params; 
	cl_m.clear(); //clear and remove the default
	cl_m.push_back(pair<MeasurementFunctions, Measurement_Params *>(MY_CUSTOMIZED_MEASURMENT_FUNCTION, &custom_args)); // Add your function and arguments
	
	//create matrix for json, and rep
	MedModel mdl;
	get_mat(json_model, rep_path, smps_preds, mdl);
	MedFeatures &bt_features_matrix = mdl.features;
	
	//Prepare and arrange the features for bootstrap analysis
	vector<float> preds_v, labelsOrig;
	vector<int> pidsOrig, preds_order;
	map<string, vector<float>> bt_data;
	bt.bootstrap_params.prepare_bootstrap(bt_features_matrix, preds_v, labelsOrig, pidsOrig, bt_data, preds_order);
	//run the bootstrap analysis
	bt.bootstrap(preds, bt_data);
	
	//Now you can access results in bt.bootstrap_results. It's map of map. The first index is the "cohort name", second index is "measurement name" and the value is the value
	for (auto &it_cohort : bt.bootstrap_results) {
		const string &cohort_name = it_cohort.first;
		for (auto &it_measurment : it_cohort.second) {
			const string &measurement_name = it_measurment.first;
			float value = it_measurment.second;
			fprintf(stdout, "%s %s %f\n", cohort_name .c_str(), measurement_name.c_str(), value);
		}
	}
}
```
 
 
When executing bootstrap, you can append multiple measurement functions and the bootstrap process will be applied on all functions.
