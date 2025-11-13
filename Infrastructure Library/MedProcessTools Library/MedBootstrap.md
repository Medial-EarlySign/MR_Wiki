
# MedBootstrap

## Example Usage

Usage example of `MedBootstrap` within C++ code

```c++
#define TEMP_PATH "/tmp/"
void run_bootstrap_on_samples(const string &samples_path, map<string, map<string, float>> &res, const string &inc_file = "") {
    MedSamples smp;
    if (smp.read_from_file(samples_path) < 0)
        MTHROW_AND_ERR("Couldn't read file %s", samples_path.c_str());
    // Example: create configuration file for cohorts
    ofstream fw(TEMP_PATH "bootstrap_new.params");
    // Format: COHORT_NAME<TAB>COHORT_DEFINITION
    // COHORT_DEFINITION is a list of parameters with min,max range, separated by ';'
    fw << "Time_Window:0-365" << "\t" << "Time-Window:0,365" << endl;
    fw << "Time_Window:0-365,Age:40-80" << "\t" << "Time-Window:0,365;Age:40,80" << endl;
    fw.close();
    map<string, vector<float>> additional_info;
    MedBootstrap boot("sample_ratio=1.0;sample_per_pid=1;loopCnt=500;filter_cohort=" + TEMP_PATH + "bootstrap_new.params");
    string addition = "";
    if (!inc_file.empty())
        addition = ";inc_stats_text=" + inc_file;
    boot.roc_Params = ROC_Params("working_point_FPR=0.1,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,10;" +
        "working_point_SENS=5,10,20,30,40,50,60,70,80,90;score_resolution=0.0001;score_bins=0" + addition);
    if (addition.empty())
        res = boot.booststrap(smp, additional_info);
    else
        res = boot.booststrap(smp, "/home/Repositories/THIN/thin_mar2017/thin.repository");
}
```

An application using `MedBootstrap` is available here: [bootstrap_app](../../Infrastructure%20Library/Medial%20Tools/bootstrap_app)

## Running Bootstrap with a Custom Measurement Function

```c++
// bootstrap_params: initialization string for bootstrap parameters
// cohort_file: file containing cohort definitions
// final_feats: MedFeature matrix or MedSamples (if only filtering Age, Gender, TimeWindow)

// The measurement function uses Lazy_Iterator to iterate over label, pred, weight in the bootstrap loop.
// Additional arguments can be passed in "params" (e.g., ROC working points).
// The function returns the measurements.
map<string, float> calc_acc(Lazy_Iterator *iterator, int thread_num, Measurement_Params *params) {
    map<string, float> res;
    float pred_val, label, weight;
    double total_cnt = 0, sum_prd = 0;
    while (iterator->fetch_next_external(thread_num, label, pred_val, weight)) {
        total_cnt += weight != -1 ? weight : 1;
        sum_prd += (pred_val == label) * (weight != -1 ? weight : 1);
    }
    total_cnt += weight != -1 ? weight : 1;
    sum_prd += (pred_val == label) * (weight != -1 ? weight : 1);
    sum_prd /= total_cnt;
    res["ACCURACY"] = sum_prd;
    return res;
}

MedBootstrapResult b;
b.bootstrap_params.init_from_string(bootstrap_params);
b.bootstrap_params.parse_cohort_file(cohort_file);
MeasurementFunctions boot_function = calc_acc;
b.bootstrap_params.measurements_with_params = { pair<MeasurementFunctions, Measurement_Params *>(calc_acc, NULL) }; // Pass NULL if no extra parameters
b.bootstrap(final_feats);
b.write_results_to_text_file("/tmp/results.csv");
```

## Cohorts File Format

The cohorts file can be defined in two ways:

1. **Single Cohort per Line**
    - Format: `COHORT_NAME<TAB>PARAMETERS_DEF`
    - `COHORT_NAME` is a string for the cohort name.
    - `PARAMETERS_DEF` is: `PARAMETER_NAME:MIN_RANGE,MAX_RANGE;...` (parameters separated by `;`).
    - The cohort is the intersection (AND) of all parameter ranges. There is a single tab between the name and the definition.
    - **Example:**
        ```
        1 year back & age 40-80    Time-Window:0,365;Age:40,80
        ```
        This creates a cohort called "1 year back & age 40-80" and filters records with (Time-Window >= 0 and <= 365) and (Age >= 40 and <= 80).

2. **Multiple Cohorts (Cartesian Product)**
    - Format: `MULTI<TAB>PARAMETERS_DEF<TAB>...PARAMETERS_DEF<TAB>`
    - A line starting with `MULTI` creates all Cartesian combinations for each parameter definition (each in the next tab).
    - `PARAMETERS_DEF` is as above.
    - **Example:**
        ```
        MULTI   Time-Window:0,30;Time-Window:30,180   Age:40,60;Age:60,80;Age:40,80   Gender:1,1;Gender:2,2
        ```
        This creates 2×3×2=12 cohorts for each combination of Time-Window, Age, and Gender options.
 

## Improvement Ideas

- Add support for more complex conditions in MedBootstrap (e.g., AND/OR logic on parameter ranges).
- Enable bootstrap calculation on multiple predictions for the same samples. This would reduce runtime when comparing different models or scores, as currently each call randomizes the bootstrap cohort and samples.