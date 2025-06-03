# Feature Generator Practical Guide
Main page for describing Feature Generators We have and how to use them.
****Specific FGs** :**
- Basic : "basic" : generating a wide range of simple (powerful) features such as last, min, max, avg, etc...
- Age : "age"  : generating age , taking into account time units and the birth year / date.
- Singleton : "singleton" : take the value of a time-less signal
- Gender : "gender" : special case of Singleton
- Binned LM : "binnedLM" : creating linear model for esitmating feature in time points
- Smoking : "smoking" : very THIN related : converting THIN basic smoking signals to features.
- KP Smoking : "kp_smoking" : very KP related : converting KP basic smoking signals to features.
- Range : "range" : features related to range signals (such as some registries)
- Drug Intake : "drugIntake" : coverage of prescription times
- Alcohol : "alcohol" : very THIN related : convertin raw alcohol THIN signals to features
- Model : "model" : using a pre trained MedModel to generate features as its predictions.
- Time : "time" : creating sample-time features (e.g. differentiate between times of day, season of year, days of the week, etc.)
- Attributes : "attr" : creating features from Samples attributes (allows "loading" of more data in the Samples file).
- [Signal Dependency](#FeatureGeneratorPracticalGuide-category_depend) : "category depend" : Select categorial features with correlation to the outcome.
- Embedding : "embedding" : Use a pre trained embedding model to generate features.
 
Some more in depth information on Feature Generators
 
**What is a Feature Generator?**
Formally, within our infrastructure a Feature Generator is running after all the rep processors. Each Feature Generator can create a constant number of features for all the given time points to a specific pid given in the dynamic record of the pid, after all rep processors had been applied to it. The features are then added to the right position in the MedFeatures object for the model. In subsequent stages after all FGs were run, Features Processors applied to the MedFeatures matrix will be run (such as imputers, normalizers, etc), and the matrix will be ready for training/prediction.
Several points to remember, esp. when writing a new FG:
- Parallelism : Feature Generators are parallelized on pids in apply stages. So when writing one it should be:
  - Thread Safe : avoid static variables in FG, and if you do use them : guard them.
  - No need to work hard to parallelize inside as it's already very efficiently parallelized from above.
- Empty Learn Stage : many FGs are like that : that is the simplest, you don't need to do anything here.
- Learn Stage : There's an issue here as the FG needs to get all the Samples and the Rep and do the FG training process. The problem is :
  - Remeber you may need to apply the rep processors needed for the FG.
    - Since Rep Processors are currently running on dynamic recs, this may become an issue and needs careful coding.
    - If you are only using signals not affected by previous rep processors, you can indeed work directly with the Samples and Rep.
  - Learn stage is NOT parallelized, hence you should take care of parallelizing it in your Feature Generator code.
- Each FG must fill in the required repository signals list in req_signals. This should be filled in first init() time , and serialized (for actual apply).
 
**Feature Generator init from parameters**
Several things happen in the init() routine:
- parameters are parsed
- names are created (use set_names() for that)
- req_signals are generated.
 
**Feature Generator Learn/Apply Stage sequence**
- Model will first scan to find out which generators need to be run (using MedModel::get_applied_generators()). Only those passing will be actually used.
- As part of the init_all procedure, the following will be called for each generator:
  - set_signal_ids : allowing generator to translate signal names to ids using the rep signals.
  - init_tables : allowing generator to initialize any internal table that requires knowing the dictionaries of the repository.
- Model will collect all required signals, hence every FG must implement the get_required_signal_names() function or fill the req_signals vector
  - The easiest way to ensure this is to make sure the req_signals vector is filled in init() . Make sure you add req_signals to the serialization.
  - If this is done, the default get_required_signal_names() is enough as it will simply add the signals in req_signals.
- In learn stage: The learn() is called, the user is responsible to apply the rep processors of the model inside the specific learn routine.
- In apply stage
  - optional prepare() function getting MedFeatures, rep and samples is called. This is sometimes needed (for example in the Model FG).
  - features is initialized and get_p_data() is called for each generator (usually the default one is good enough)
  - for each pid , all (required) rep processors are invoked by their order, and then all the (reuired) generators. Parallelism is on the pids.
 
 
## Signal Dependency FG ("category_depend")
Using Signal Dependency to generate categorical signal.
chi-square statistical test for independency between outcome and appearance of the category value for Gender+Age stratas. It selects the top k categories with the best p value and Lift. 
It also works on sets and hierarchical categories like ATC, ICD10 
Feature Generator Arguments:
- "signal" - the categorical signal in repository
- "win_from,win_to,time_unit_win" - time window arguments to define time window
- "regex_filter" - filter categories bt name - for example take only "ATC" drug codes. use "ATC_.*"
- "min_age,max_age,age_bin" - Age strata for the statistical test. Also uses gender
- "min_code_cnt" - filters categories below this count of apearences
- "fdr" - p value filter
- 
"lift_below,lift_above" - filters on Lift values of category on average
- 
"max_depth,max_parents" - hierarchical arguments, how many parents to take for each category value (in the example till 5 parentes), and maximal number of parents in that depth
- 
"take_top" - how many features to create, based on the categories. sorted by P value, lift and chi-square score by this order
- 
"stat_test" - chi-square or mcnemar (TODO add support for Cochran–Mantel–Haenszel statistics, fisher excat test). mcnemar is not exactly mcnemar because our data is not pairwise matched,
but manipulated test to mimic this behaivor. from my experience it's more robust and gives better results
- 
"verbose" - if 1 prints the taken categories with Lift, total_count and some stats
 
Example of using CategoryDependencyGenerator:
**Config Example**
 Expand source
```
{
            "action_type":"feat_generator",
            "fg_type":"category_depend",
            "signal":"RC",
			"win_from":"0",
			"win_to":"1825",
			"time_unit_win":"Days",
			"regex_filter":"ICD10_CODE:.*",
			"min_age":"18",
			"max_age":"90",
			"age_bin":"5",
			"min_code_cnt":"1000",
			"fdr":"0.01",
			"lift_below":"0.8",
			"lift_above":"1.2",
			"stat_metric":"mcnemar",
			"max_depth":"5",
			"max_parents":"10",
			"use_fixed_lift":"0",
			"verbose":"1",
			"take_top":"100"
			
}
```
Running train MedModel with this+Age+Gender on death from Flu model with AUC=0.92 compared to Age+Gender only with AUC=0.88
 
TODO:
- Use Stratas instead of fixed:Age,Gender
- Improve logic for filterHirarchy - to use Entropy or better measure to filter parent\child 
- profilling - improve speed
