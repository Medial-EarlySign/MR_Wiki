
# Extending Bootstrap

The bootstrap infrastructure is designed to be extensible, allowing you to add custom statistical measurements to the bootstrap analysis process (i.e., repeated experiments with replacement) to estimate confidence intervals, standard deviations, and more.

To do this, you simply write a function that computes your desired measurement(s).

## Function Signature

Your measurement function must use the following signature:

- `Lazy_Iterator *iterator`: Used to fetch data for measurement calculation. This iterator is efficient, performing randomization on the fly without allocating memory for each bootstrap experiment.
- `int thread_num`: The thread number for parallel execution, used by the iterator.
- `Measurement_Params *function_params`: Optional pointer to function parameters (can be `nullptr`). Use this to pass custom parameters to your function.

### Using the Iterator

Call `fetch_next(thread_num, y, pred, w)` to iterate through the data. It returns `true` until the end of input is reached.

If you are using your function outside of `bootstrap.cpp`, use `fetch_next_external` instead (the only difference is a minor optimization in `fetch_next`).

For more complex cases (e.g., multi-label outcomes), you can pass `ret_preds_order` to `fetch_next` when you have multiple predictions.

**Argument meanings:**

- `y`: Label/outcome
- `pred`: Prediction/score
- `w`: Weight (`-1` if not used). If your measurement does not support weights, check that `w == -1` and throw an error if weights are present.

**function_params:**
If your function uses parameters, check that `function_params` is not `nullptr` (otherwise use defaults), and cast it to your parameter type. `Measurement_Params` is a simple class you can extend (e.g., `ROC_Params`).

**Example:**
```c++
map<string, float> calc_roc_measures_with_inc(Lazy_Iterator *iterator, int thread_num, Measurement_Params *function_params) {
	ROC_Params default_params;
	ROC_Params *params = &default_params;
	if (function_params != NULL)
		params = (ROC_Params *)function_params;
	// Use params as needed
	float max_diff_in_wp = params->max_diff_working_point;
	// ...
}
```

## Function Output

Your function should return a `map<string, float>`, where each key is the name of a measurement and the value is the result. This allows you to compute multiple measurements in a single function.

The infrastructure will automatically append suffixes to each measurement: `_Mean`, `_Std`, `_CI.Lower.95`, `_CI.Upper.95`, `_Obs`. See: [Bootstrap legend](../Bootstrap%20legend.md)

### Example: Counting Cases and Controls
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
This function counts the number of positive and negative outcomes in the data, supporting weights if present.

## Using Your Custom Function

```c++
#include <MedStat/MedStat/MedBootstrap.h>

// Example custom measurement function
map<string, float> MY_CUSTOMIZED_MEASUREMENT_FUNCTION(Lazy_Iterator *iterator, int thread_num, Measurement_Params *function_params) {
	// ...
}

// Example custom parameter class
class Custom_Measurement_Parameters : public Measurement_Params {
public:
	int min_bin_size = 0;
	float cases_weight = 1;
	float controls_weight = 1;
};

// Helper function to generate matrix for filtering (needed if generating cohorts and filtering with bootstrap)
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
	// Set bootstrap parameters (see MedBootstrap::init for all options)
	string bt_params = "loopcnt=500;sample_per_pid=1";
	MedBootstrapResult bt;
	bt.bootstrap_params.init_from_string(bt_params);

	// Custom measurement parameters
	Custom_Measurement_Parameters custom_args;

	string json_model;    // Optional: for generating features for cohort filtering
	string cohorts_file;  // Path to cohort definitions. If not specified, all samples are used as a single cohort.
	string rep_path;      // Path to repository (needed if filtering by more than Time-Window)

	MedSamples preds;     // Your MedSamples with predictions
	preds.read_from_file("YOUR_SAMPLES_PATH");

	if (!cohorts_file.empty())
		bt.bootstrap_params.parse_cohort_file(cohorts_file);

	// Set measurement functions (default is calc_roc_measures_with_inc)
	vector<pair<MeasurementFunctions, Measurement_Params *>> &cl_m = bt.bootstrap_params.measurements_with_params;
	cl_m.clear();
	cl_m.push_back(pair<MeasurementFunctions, Measurement_Params *>(MY_CUSTOMIZED_MEASUREMENT_FUNCTION, &custom_args));

	// Create matrix for json and repository
	MedModel mdl;
	get_mat(json_model, rep_path, smps_preds, mdl);
	MedFeatures &bt_features_matrix = mdl.features;

	// Prepare features for bootstrap analysis
	vector<float> preds_v, labelsOrig;
	vector<int> pidsOrig, preds_order;
	map<string, vector<float>> bt_data;
	bt.bootstrap_params.prepare_bootstrap(bt_features_matrix, preds_v, labelsOrig, pidsOrig, bt_data, preds_order);
	// Run bootstrap analysis
	bt.bootstrap(preds, bt_data);

	// Access results: bt.bootstrap_results is a map of maps (cohort name -> measurement name -> value)
	for (auto &it_cohort : bt.bootstrap_results) {
		const string &cohort_name = it_cohort.first;
		for (auto &it_measurement : it_cohort.second) {
			const string &measurement_name = it_measurement.first;
			float value = it_measurement.second;
			fprintf(stdout, "%s %s %f\n", cohort_name.c_str(), measurement_name.c_str(), value);
		}
	}
}
```

You can append multiple measurement functions; the bootstrap process will apply all of them.
