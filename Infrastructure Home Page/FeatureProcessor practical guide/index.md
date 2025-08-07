# FeatureProcessor practical guide
<table><tbody>
<tr>
<td> </td>
</tr>
<tr>
<td><em>FTR_PROCESS_NORMALIZER</em></td>
<td><p>"normalizer" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classFeatureNormalizer.html" rel="nofollow" title="Feature Normalizer. ">FeatureNormalizer</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_IMPUTER</em></td>
<td><p>"imputer" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classFeatureImputer.html" rel="nofollow" title="Feature Imputer to complete missing values. ">FeatureImputer</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_DO_CALC</em></td>
<td><p>"do_calc" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classDoCalcFeatProcessor.html" rel="nofollow" title="User defined calculations on other features. ">DoCalcFeatProcessor</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_UNIVARIATE_SELECTOR</em></td>
<td><p>"univariate_selector" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classUnivariateFeatureSelector.html" rel="nofollow" title="Feature Selector : Univariate. ">UnivariateFeatureSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESSOR_MRMR_SELECTOR</em></td>
<td><p>"mrmr" or "mrmr_selector" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classMRMRFeatureSelector.html" rel="nofollow" title="Feature Selector : MRMR. ">MRMRFeatureSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESSOR_LASSO_SELECTOR</em></td>
<td><p>"lasso" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classLassoSelector.html" rel="nofollow" title="Feature Selector : lasso. ">LassoSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESSOR_TAGS_SELECTOR</em></td>
<td><p>"tags_selector" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classTagFeatureSelector.html" rel="nofollow">TagFeatureSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESSOR_IMPORTANCE_SELECTOR</em></td>
<td><p>"importance_selector" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classImportanceFeatureSelector.html" rel="nofollow" title="ImportanceFeatureSelector - selector which uses feature importance method for sepcific model to rank ...">ImportanceFeatureSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESSOR_ITERATIVE_SELECTOR</em></td>
<td><p>"iterative_selector" applies bottom-up or top-down iteration for feature selection. Creates <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classIterativeFeatureSelector.html" rel="nofollow" title="IterativeFeatureSelector - Apply bottom-up or top-down iteration for feature selection. ">IterativeFeatureSelector</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_REMOVE_DGNRT_FTRS</em></td>
<td><p>"remove_deg" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classDgnrtFeatureRemvoer.html" rel="nofollow" title="Feature Selector : Remove Degenerate features. ">DgnrtFeatureRemvoer</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_ITERATIVE_IMPUTER</em></td>
<td><p>"iterative_imputer" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classIterativeImputer.html" rel="nofollow" title="  IterativeImputer   A general strong imputer that does the following:  (1) Runs a simple stratified ...">IterativeImputer</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_ENCODER_PCA</em></td>
<td><p>"pca" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classFeaturePCA.html" rel="nofollow" title="FeaturePCA - PCA encoder. ">FeaturePCA</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_ONE_HOT</em></td>
<td><p>"one_hot" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classOneHotFeatProcessor.html" rel="nofollow" title="OneHotFeatProcessor: ">OneHotFeatProcessor</a> - make one-hot features from a given feature</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_GET_PROB</em></td>
<td><p>"get_prob" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classGetProbFeatProcessor.html" rel="nofollow" title="GetProbProcessor: ">GetProbFeatProcessor</a> - replace categorical feature with probability of outcome in training set</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_PREDICTOR_IMPUTER</em></td>
<td><p>"predcitor_imputer" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classPredictorImputer.html" rel="nofollow" title="Predictor Imputer - use all features in the matrix to predict value to impute selects randomly a valu...">PredictorImputer</a></p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_MULTIPLIER</em></td>
<td><p>"multiplier" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classMultiplierProcessor.html" rel="nofollow" title="MultiplierProcessor: ">MultiplierProcessor</a> - to multiply feature by other feature</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_RESAMPLE_WITH_MISSING</em></td>
<td><p>"resample_with_missing" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classResampleMissingProcessor.html" rel="nofollow" title="ResampleMissingProcessor: Add missing values to the train matrix for the train process. ">ResampleMissingProcessor</a> - adds missing values to learn matrix</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_DUPLICATE</em></td>
<td><p>"duplicate" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classDuplicateProcessor.html" rel="nofollow" title="Duplicates the samples in Apply only - can be used for multiple imputations to calculate CI adn more...">DuplicateProcessor</a> - duplicates samples in order to do multiple imputations.</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_MISSING_INDICATOR</em></td>
<td><p>"missing_indicator" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classMissingIndicatorProcessor.html" rel="nofollow" title="FeatureMissingIndicator: creates a feature that indicates if a feature is missing or not...">MissingIndicatorProcessor</a> - creates a feature that indicates if a feature is missing or not</p></td>
</tr>
<tr>
<td><em>FTR_PROCESS_BINNING</em></td>
<td><p>"binning" to create <a class="external-link" href="https://Medial-EarlySign.github.io/MR_LIBS/classBinningFeatProcessor.html" rel="nofollow" title="GetProbProcessor: ">BinningFeatProcessor</a> - binning with one hot on the bins</p></td>
</tr>
</tbody></table>

 
- "remove_deg" - removes features that most of the time are same value (or missing) 
```json
{
      "action_type": "fp_set",
      "members": [
        {
          "fp_type": "remove_deg",
          "percentage": "0.999"
        }
      ]
  }
```
- "normalizer" - to normalize features:
```json
 {
      "action_type": "fp_set",
      "members": [
        {
          "fp_type": "normalizer",
          "resolution_only":"0",
		  "resolution":"5",
		  "tag":"need_norm",
		  "duplicate":"1"
        }
      ]
    }
```
  tag + duplicate=1, results in wrapping this feature processor with MultiFeatureProcessors that iterates over all features and filter out features by "tag" to apply this normalization processing. I tagged all the required relevant features with tag "need_norm"
- "imputer" by strata of age+sex+other features. Take median,common, average, sample, etc:
```json
{
"action_type": "fp_set",
"members": [
{
"fp_type": "imputer",
"strata": "Age,0,80,10:Gender,1,2,1",
"moment_type":"common",
"tag":"need_imputer",
"duplicate":"1"
}
]
}
```
- "do_calc" - calculator of some features from others. For example "or" on features, can also "sum" features
```json
{
		"action_type": "fp_set",
		  "members": [
			{
			  "fp_type": "do_calc",
			  "calc_type": "or",
			  "source_feature_names": "Current_Smoker,Ex_Smoker",
			  "name":  "Ex_or_Current_Smoker"
            }
		]
	}
```
- importance_selector - selection of features based on most important features in a model that is trained on the data. 
- iterative_selector - please use the tool to do it, it takes forever!! [Iterative Feature Selector](/Medial%20Tools/Iterative%20Feature%20Selector)
- resample_with_missing - used in training to "generate" more samples with missing values and increasing data size (not doing imputations, that
```json
{
      "action_type": "fp_set",
      "members": [
		{
			 "fp_type": "resample_with_missing",
			 "missing_value":"-65336",
			 "grouping":"BY_SIGNAL_CATEG",
			 "selected_tags":"labs_numeric",
			 //"removed_tags":"",
			 "duplicate_only_with_missing":"0",
			 "add_new_data":"3000000",
			 "sample_masks_with_repeats":"1",
			 "limit_mask_size":"2",
			 "uniform_rand":"0",
			 "use_shuffle":"0",
			 "subsample_train":"3000000",
			 "verbose":"1"
		}
	  ]
	}
```
  No need for duplicate, it is scanning the features by it's own and operating on "selected_tags". add_new_data- - how many new data points to add. grouping is used to generate masks of missing values in groups and not feature by features. This is another feature processor job). similar to data augmentation in imaging
- "binning" - binning feature value - can be specified directly the cutoffs or using some binning_method, equal width, minimal observations in each bin, etc.
```json
{
	"action_type": "fp_set",
	"members": [
		{
			"action_type": "feat_processor",
			"fp_type": "binning",
			"bin_sett": "{bin_cutoffs=0,1,15,30,100}",
			"one_hot": 0,
			"tag": "Smok_Pack_Years_Last", 
			"duplicate": 1
		}
	]
    }
```
- "predcitor_imputer" - much more complicated/smart imputer based on model. Gibbs samplings, masked GAN, univariate sampling from features distributions, etc.. 
```json
{
      "action_type": "fp_set",
      "members": [
        {
          "fp_type": "predictor_imputer",
          "tag":"need_imputer",
		  "duplicate":"0",
		  "gen_type":"GIBBS",
		  "verbose_learn":"1",
		  "verbose_apply":"1",
		  "use_parallel_learn":"0",
		  "use_parallel_apply":"0",
		  "generator_args":"{calibration_save_ratio=0.2;bin_settings={split_method=iterative_merge;min_bin_count=100;binCnt=50};calibration_string={calibration_type=isotonic_regression;verbose=0};predictor_type=lightgbm;predictor_args={objective=multiclass;metric=multi_logloss;verbose=0;num_threads=1;num_trees=10;learning_rate=0.05;lambda_l2=0;metric_freq=50;is_training_metric=false;max_bin=255;min_data_in_leaf=20;feature_fraction=0.8;bagging_fraction=0.25;bagging_freq=4;is_unbalance=true;num_leaves=80;silent=2};selection_count=200000}",
		  "sampling_args":"{burn_in_count=20;jump_between_samples=5;find_real_value_bin=1}"
        }
      ]
    }
```
Instead of GIBBS, GAN, can select:
  - RANDOM_DIST - random value from normal dist around 0,5 (not related to feature dist)
  - UNIVARIATE_DIST - strata by some features, store distribution in each strata. In apply, find strata and select value randomly from dist
  - MISSING - put missing value
  - GAN - generator_args is path to trained model. Please refer to this path to train: [TrainingMaskedGAN](/Medial%20Tools/GANs%20for%20imputing%20matrices/TrainingMaskedGAN)
  - GIBBS - arguments 
    - sampling_args - 
      - burn_in_count - how many round to do in the start and to ignore them till stablize on reasonable vector. 
      - jump_between_samples - how many rounds to do before generating new sample. when continuing to iterate in rounds, after several loops we end up with different sample
      - find_real_value_bin - if true will round values to existing values only from feature values. When you try to see if model can discriminate between real data and generated data, the resolution of the feature values is important. tree can detect different between 3 nd 3.000001. If true this will cause 3.00001 to be 3. No good reason why to turn off
      - samples_count - how many samples to extract
    - generator_args
      - calibration_save_ratio - what percentage of data to keep for clibration to probability. 0.2 (20%) is good number
      - bin_settings - how to split the feature value into bins. The prediction problem will be multi category to those binned values. For example, hemoglobin last : 13.1-13.3, 13.4-13.6, etc... The target will be what's the probability to have hemoglobin in each value range. after having this, we can sample from this distribution bin value for the feature. 
      - calibration_string - how to calibarte. keep as isotonic_regression, it's good
      - predictor_type - predictor type for the multi class prediction
      - predictor_args - arguments for the predictor. please pay attention this is multi category prediction! For example objective for lightGBM is "objective=multiclass"
      - num_class_setup - since this is multiclass, some predictors requires to setup how many classes there are. This argument controls the name of this parameters. In LightGBM for example it's called "num_class"
      - selection_count - down sampling for training those models to speedup