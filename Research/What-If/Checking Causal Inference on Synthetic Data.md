# Checking Causal Inference on Synthetic Data

The program for testing causal-inference methods on synthetic data is located in - H:\MR\Projects\Shared\CausalEffects\CausalEffectsUtils\check_toy_model

The program parameters are : 

```

check_toy_model --help

Program options:

  --help                                produce help message

  --trainMatrix arg                     train data file (bin)

  --testMatrix arg                      test data file (bin)

  --validationMatrix arg                validation data file (bin)

  --params arg                          serialized true model file

  --validationITE arg                   File of validation ITE

  --out arg                             output file for ITE graph

  --read_models                         read required models from file

  --write_models                        write generated models to file

  --models_prefix arg                   prefix of models for read/write

  --gen_model_params arg (=lightgbm;num_threads=15;num_trees=200;learning_rate=0.05;lambda_l2=0;metric_freq=250;bagging_fraction=0.5;bagging_freq=1;feature_fraction=0.8;max_bin=50;min_data_in_leaf=250;num_leaves=120)

                                        parameters and definition of

                                        classifiers which are not specifically

                                        given

  --gen_reg_params arg (=xgb;alpha=0.1;colsample_bytree=0.5;eta=0.01;gamma=0.5;booster=gbtree;objective=reg:linear;lambda=0.5;max_depth=3;min_child_weight=100;num_round=250;subsample=0.5)

                                        parameters and definition of regressors

                                        which are not specifically given

  --nbootstrap arg (=100)               # of bootstrap rounds

  --nfolds arg (=8)                     # of folds for cross validation

  --gen_nn_params arg (=batch_size=1000;function=relu;max_num_batches=30000;checkpoint_num_batches=250;data=features;keep_prob=0.8;learning_rate=1e-3;nhidden=200;nlayers=2)

                                        parameters for nn regressionscript

  --do_true                             get ITE from true model

  --do_direct                           directly model true ite

  --do_model                            get ITE from single model

  --model_params arg                    parameters and definition of outcome

                                        predictor

  --add_propensity arg (=0)             If True will add propensity score to

                                        direct model for outcome

  --bonus arg (=0)                      bonums for splitting by treatment in

                                        outcome prediction using xgboost

  --do_nn_model                         get ITE from single NN model

  --do_two_models                       get ITE from single model

  --model0_params arg                   parameters and definition of outcome

                                        predictor for untreated

  --mode1_params arg                    parameters and definition of outcome

                                        predictor for treated

  --do_weighted                         get ITE from propensity weighted model

  --prop_params arg                     parameters and defition of propensity

                                        score

  --weighed_model_params arg            parameters and definition of outcome

                                        predictor

  --do_g_comp                           get ITE using g-computation

  --g_comp_params arg                   parameters and definition of outcome

                                        predictor

  --g_comp_prop_params arg              parameters and definition of propensity

                                        predictor

  --g_comp_reg_params arg               parameters and definition of

                                        counter-factuals regressor

  --g_comp_reg_script arg (=/nas1/UsersData/yaron/MR/Tools/quasi_oracle/PythonScripts/ite_predictor.py)

                                        Python script for t-prediction (ITE)

  --g_comp_reg_script_output arg        output for Python script for

                                        counter-factuals regressor

  --g_comp_reg_script_input arg (=g_comp_matrix)

                                        input for Python script for

                                        counter-factuals regressor

  --g_comp_reg_script_params arg        parameters for python script for

                                        counter-factuals regressor

  --g_comp_cf_params arg                parameters and definition of

                                        counter-factuals classifier

  --gNumCopy arg (=10)                  number of copies per sample in

                                        counterfactual matrix

  --gAddTestMatrix                      add test matrix to counter-factual

                                        regression matrix

  --do_two_models_g_comp                get ITE using g-computation

  --g_comp_params0 arg                  parameters and definition of outcome

                                        predictor for treatment=0

  --g_comp_params1 arg                  parameters and definition of outcome

                                        predictor for treatment=1

  --do_nn_quasi_oracle                  get ITE using quasi-oracle

  --do_quasi_oracle                     get ITE using quasi-oracle

  --e_params arg                        Quasi-Oracle e-prediction params

                                        (propensity)

  --m_params arg                        Quasi-Oracle m-prediction params

                                        (outcome without explicit treatment)

  --t_params arg                        Quasi-Oracle t-prediction params (ITE)

  --t_script arg (=/nas1/UsersData/yaron/MR/Tools/quasi_oracle/PythonScripts/ite_predictor.py)

                                        Python script for t-prediction (ITE)

  --t_script_output arg                 output for Python script for

                                        t-predictions (ITE)

  --t_script_input arg (=ite_matrix)    input for Python script for

                                        t-predictions (ITE)

  --t_script_params arg                 parameters for python script for

                                        t-predictions (ITE)

  --do_oracle                           get ITE using an oracle

  --treatment_params arg                serialized treatment model file

  --extend_matrix                       add quadratic features to t-modeling

                                        matrix

  --preds_files_suffix arg              Siffix for predictions files

  --optimization_file arg               File for optimization of t-predictor

                                        parameters

  --summary_file arg                    File for summary of results

  --do_external                         read predictions from csv file

  --preds_file arg                      predictions file (untreated/treated

                                        pairs)

  --do_external_predictor               generate predictions from a

                                        MedPredictor

  --predictor_file arg                  predictor files (ITE from features

                                        without Treatment)

  --do_external_script                  generate predictions using a script

  --script arg                          external script to run

  --script_input arg                    script data input (--data ...)

  --script_params arg                   script parameters

  --script_output arg                   script prediction output (--preds ...)

  --do_cfr                              run counterfactual regression

  --script_dir arg (=.)                 script data directory

  --cfr_train_script arg (=/nas1/UsersData/yaron/MR/Projects/Shared/CausalEffects/CausalEffectScripts/cfrnet-master/cfr_net_train.py)

  --cfr_trans_script arg (=/nas1/UsersData/yaron/MR/Projects/Shared/CausalEffects/CausalEffectScripts/csv2cfr.py)

  --do_shap                             use Shapley values for ITE

  --do_ipw_shap                         use Shapley values on IPW-corrected

                                        model for ITE

  --do_weighted_nn_model                get ITE from propensity weighted NN

                                        model

```

The program uses ** and **** to learn model(s) for evaluation individual treatment effecsts (ITE) and then applies the model(s) on **. The programs outputs include descrptive information in **, as weill as tabular output in **. Each line in ** countains three tab-delimited columns -  

<table><tbody>

<tr>

<th>Method-Name</th>

<th>True-ITE</th>

<th>Estimated-ITE</th>

</tr>

</tbody></table>

The true ITE is either generated from the generative model (if given, in **.bin and **.treatment.bin) or read from file (**)

Methods currently implemented are:

<table><tbody>

<tr>

<th>Method</th>

<th>Description</th>

<th>Comment</th>

</tr>

<tr>

<td><p>do_true</p></td>

<td>true ITE from generative models</td>

<td> </td>

</tr>

<tr>

<td><span>do_direct</span></td>

<td>Learn a regression model to directly evaluate ITE on <em><strong>trainMatrix</strong></em> and apply on <strong><em>validationMatrix</em></strong></td>

<td>This is a <u><strong>debugging</strong></u> method as it assumes true ITE is known for the trainMatrix</td>

</tr>

<tr>

<td><span>do_model</span></td>

<td><span>Learn</span> a naive model ƒ(x,T)→y , and evaluate ITE = <span>ƒ(x,1) - <span>ƒ(x,0)</span></span></td>

<td> </td>

</tr>

<tr>

<td><span>do_nn_model</span></td>

<td>Same as do_model but using external learning/predictions scripts for model</td>

<td>Allows interfacing with TensorFlow</td>

</tr>

<tr>

<td><span>do_two_models</span></td>

<td>Learn two models<span>ƒ<sub>T=1</sub>(x)→y and <span>ƒ</span><sub>T=0</sub><span>(x)→y and evaluate ITE = <span>ƒ</span><sub>T=1</sub><span>(x) - </span><span>ƒ</span><sub>T=0</sub><span>(x)</span></span></span></td>

<td> </td>

</tr>

<tr>

<td><span>do_weighted</span></td>

<td>Use Inverse Propensity Weighting (IPW) to learn <span>ƒ(x,T)→y , and evaluate ITE = </span><span>ƒ(x,1) - ƒ(x,0)</span></td>

<td> </td>

</tr>

<tr>

<td><span>do_weighted_nn_model</span></td>

<td>Same as do_weighted but using <span>external learning/predictions scripts for model</span></td>

<td><span>Allows interfacing with TensorFlow</span></td>

</tr>

<tr>

<td><span>do_g_comp</span></td>

<td><p>Use "G-Computation" - create counter-factuals using a model, and then use them for learning a</p><p>second model.</p></td>

<td>IPW optional for first model</td>

</tr>

<tr>

<td><span>do_two_models_g_comp</span></td>

<td>A combination of do_g_comp &amp; do_two_models</td>

<td> </td>

</tr>

<tr>

<td><p>do_quasi_oracle</p></td>

<td>Evalute ITE using Quasi-Oracle - e* and m* evaluated internally and ITE using an external script</td>

<td>ITE is evaluated using an external script to allow using TensorFlow NN</td>

</tr>

<tr>

<td><p>do_nn_quasi_oracle</p></td>

<td><span>Evalute ITE using Quasi-Oracle - <span>e* and m* also evaluated using external scripts</span></span></td>

<td><span>Allows interfacing with TensorFlow on all stages</span></td>

</tr>

<tr>

<td><span>do_oracle</span></td>

<td>Similar to Quasi-Oracle, only using <strong>true</strong> e and m instead of estimated e* and m*</td>

<td><span>his is a </span><u><strong>debugging</strong></u><span> method as it assumes true e and m are known</span></td>

</tr>

<tr>

<td><span>do_external</span></td>

<td>Import ITE from file and generate <em><strong>out</strong></em> file</td>

<td> </td>

</tr>

<tr>

<td><span>do_external_predictor</span></td>

<td>Read a MedPredictor object and apply on <em><strong>validationMatrix</strong></em> to generate ITE</td>

<td> </td>

</tr>

<tr>

<td><span>do_external_script</span></td>

<td>Apply an external script to generate ITE on <em><strong>validationMatrix</strong></em></td>

<td> </td>

</tr>

<tr>

<td><span>do_cfr</span></td>

<td>Apply Uri Shalit's CounterFactual Regression Methods</td>

<td>Use downloaded scripts</td>

</tr>

<tr>

<td><span>do_shap</span></td>

<td>Use Shapley of naive model <span>ƒ(x,T)→y</span> values as estimators for ITE</td>

<td> </td>

</tr>

<tr>

<td><span>do_ipw_shap</span></td>

<td><span>Use Shapley of IPW-learned model </span><span>ƒ(x,T)→y</span><span> values as estimators for ITE</span></td>

<td> </td>

</tr>

</tbody></table>

 

 

