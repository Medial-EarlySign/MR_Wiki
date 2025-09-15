# MedBootstrap
**Example Use Function**
```c++
#define TEMP_PATH "/tmp/"
void run_bootstrap_on_samples(const string &samples_path, map<string, map<string, float>> &res, const string &inc_file = "") {
    MedSamples smp;
    if (smp.read_from_file(samples_path) < 0)
        MTHROW_AND_ERR("Couldn't read file %s", samples_path.c_str());
    //Example for creating configuraiton file for cohorts
    ofstream fw(TEMP_PATH "bootstrap_new.params");
    // COHORT_NAME TAB CHOROT_DEFINITION
    // CHOROT_DEFINITION - is list of paramters with min,max range. each param is seprated by ;
    fw << "Time_Window:0-365" << "\t" << "Time-Window:0,365" << endl;
    fw << "Time_Window:0-365,Age:40-80" << "\t" << "Time-Window:0,365;Age:40,80" << endl;
    fw.close();
    map<string, vector<float>> additional_info;
    MedBootstrap boot("sample_ratio=1.0;sample_per_pid=1;loopCnt=500;" "filter_cohort=" + TEMP_PATH + "bootstrap_new.params");
    string addition = "";
    if (!inc_file.empty())
        addition = ";inc_stats_text=" + inc_file;
    boot.roc_Params = ROC_Params("working_point_FPR=0.1,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,10;" + "working_point_SENS=5,10,20,30,40,50,60,70,80,90;score_resolution=0.0001;score_bins=0" + addition);
    if (addition.empty())
        res = boot.booststrap(smp, additional_info);
    else
        res = boot.booststrap(smp, "/home/Repositories/THIN/thin_mar2017/thin.repository");
}
```
Example Code for MedBootstrap (you may look at $MR_ROOT/Projects/Shared/UnitTestingInfra for the testing process)
There is an application which uses this libray - [bootstrap_app](../../Medial%20Tools/bootstrap_app)
 
How to run bootstrap on a custom measurement function:
```c++
//string bootstrap_params - is the init string for bootstrap parameters
//string cohort_file - the file with cohorts definitions
//final_feats - the MedFeature matrix to use in bootstrap, can be also MedSamples (than you can only filter Age,Gender,TimeWindow) in cohorts
 
//the measurement function - has Lazy_Iterator to iterate over label,pred,weight in bootstrap loop
// can also get additional arguments for the function in "params" - can be working points in ROC for example
//the function returns the measurements
map<string, float> calc_acc(Lazy_Iterator *iterator, int thread_num, Measurement_Params *params) {
	map<string, float> res;
	float pred_val, label, weight;
	double total_cnt = 0, sum_prd = 0;
	while (iterator->fetch_next_external(thread_num, label, pred_val, weight)) {
		total_cnt += weight != -1 ? weight : 1;
		sum_prd += (pred_val == label) * (weight != -1 ? weight : 1);
		//sum_lbls += label;
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
b.bootstrap_params.measurements_with_params = {	pair<MeasurementFunctions, Measurement_Params *>(calc_acc, NULL) }; //calc_auc doesn't have additional parameters so I passed NULL
b.bootstrap(final_feats);
b.write_results_to_text_file("/tmp/results.csv");
```
 
### Improvment Ideas:
- add support for more complicated conditions in MedBootstrap itself - for example and,or conditions on the ranges
- add support for calculating bootstrap on multiple predictions on the same samples - it can shortened the running time significantly when comparing/running on same samples with diffrent models\scores. now you need to call bootstrap in a loop for each score and each call will randomize again the bootstrap cohort and samples
 
#### **Cohorts file format:**
 The file format may be in 2 options:
1. COHORT_NAME[TAB]PARAMETERS_DEF - cohort name is string representing cohort name. PARAMETER_DEF is in format: "PARAMETER_NAME:MIN_RANGE,MAX_RANGE;..." the format can repeat itself with ";" between each parameter. the cohort will consist of intersection between all parameters ranges with "and" condition. there is single tab betwwen the name and the defenition. Example Line: 1 year back & age 40-80 Time-Window:0,365;Age:40,80 will create cohort called "1 year back & age 40-80" and will filter out records with (Time-Window>=0 and Time-Window<=365) and (Age>=40 and Age<=80) 
2. MULTI[TAB]PARAMETERS_DEF[TAB]...PARAMETERS_DEF[TAB] - this definition with line starting with MULTI keyword will create all the cartesain options for each parameter definition with the each parameter definition in the next TABs. PARAMETERS_DEF - is same as option 1 format. Example Line: MULTI Time-Window:0,30;Time-Window:30,180 Age:40,60;Age:60,80;Age:40,80 Gender:1,1;Gender:2,2 will create 2*3*2=12 cohorts for each Time-Window, Age, and Gender option 
 
 
