# An envelope script for Causal Inference on Synthetic Data
The script H:/MR/Projects/Shared/CausalEffects/CausalEffectScripts/run_process.py is an envelope for generating synthetic data for causal-inference, applying several methods, and analyzing.
At the moment, the script should be executed on node-05.
The scripts parmeters are:
```bash
run_process.py --help
usage: run_process.py [-h] --config CONFIG [--start START] [--end END]
                      [--show]
Check Causal Effects Approaches on Toy Model
optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  configuration file
  --start START    start stage
  --end END        end stage
  --show           show stages
  --fast           skip slow stages
```
- 
config is the only required parameter. An example of a configuration file is - 
```ini
nSamples=15000
nums=--numA 10 --numB 10 --numC 10
pTreatment=0.25
seed1=123
seed2=22
seed3=11
params=--pOutcome 0.1 --outSigMin 0.08 --outSigMax 0.95 --treatSigWidth 5.0 --outSigWidth 5.0 --outcomePolyDegree 2 --treatmentPolyDegree 2 --treatmentFactor 0.4
dir=/nas1/Work/Users/yaron/CausalEffect/ToyModel_ITE/Test1
```
Note that all keys are required, and no sapces allowed around the assignment sign. All keys are used for generating the synthetic data, and ** is also used for all further steps
- 
** tells the script to list all stages and stop:
```bash
run_process.py --config dummy --show
['Generate', 'Stats', 'Naive.LGBM', 'IPW.LGBM', 'Naive.LGBM.RCT', 'Naive.NN', 'IPW.NN', 'Naive.NN.RCT', 'Quasi.NN', 'Quasi.Full_NN', 'Quasi.LGBM', 'CFR', 'SHAP', 'IPW.SHAP', 'Performance']
```
- 
** and ** allow running only a subset of the script's stages
- slow stages are - IPW.NN and Quasi.Full_NN
The stages of the script perform the following tasks-
<table><tbody>
<tr>
<td><strong>Generate</strong></td>
<td>Generate the synthetic data</td>
</tr>
<tr>
<td><strong>Stats</strong></td>
<td>Some analyses on synthetic data, including generation of true validation ITEs file</td>
</tr>
<tr>
<td><strong>Naive.LGBM → IPW.SHAP</strong></td>
<td>check_toy_model using various methods</td>
</tr>
<tr>
<td><strong>Performance</strong></td>
<td>Check performance of various methods using correlation to true ITE</td>
</tr>
</tbody></table>
A part of the **Stats** stage is running the script H:/MR/Projects/Shared/CausalEffects/CausalEffectScripts/analyze_risk_matrix.py *****  *that generates a PDF file (**) with various graphs. However, due to Python issues we currently do not run it within the envelope script and it should be executed seperately
The output of the envelope script is a file **/Summary which include both config file information, as well as the performance evaluation information:
```
nSamples=15000
nums=--numA 10 --numB 10 --numC 10
pTreatment=0.25
seed1=123
seed2=22
seed3=11
params=--pOutcome 0.1 --outSigMin 0.08 --outSigMax 0.95 --treatSigWidth 5.0 --outSigWidth 5.0 --outcomePolyDegree 2 --treatmentPolyDegree 2 --treatmentFactor 0.4
dir=/nas1/Work/Users/yaron/CausalEffect/ToyModel_ITE/Test1
ITEs.true : 1.000000
ITEs.Model.NN.RCT : 0.536027
ITEs.Model.LGBM.RCT : 0.531990
ITEs.Quasi.Full_NN : 0.315594
ITEs.Quasi.NN : 0.313484
ITEs.Quasi.LGBM : 0.284961
ITEs.CFR : 0.249583
ITEs.Model.LGBM : 0.222051
ITEs.IPW.LGBM : 0.216663
ITEs.shap : 0.201008
ITEs.Model.NN : 0.175503
ITEs.IPW.NN : 0.119160
ITEs.ipw_shap : 0.110271
```
 
 
