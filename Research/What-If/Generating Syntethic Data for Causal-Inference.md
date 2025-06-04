# Generating Syntethic Data for Causal-Inference
The program for generating synthetic data is located in - H:\MR\Projects\Shared\CausalEffects\CausalEffectsUtils\generate_realistic_data
the program implements the following model - 
 
<img src="/attachments/11207537/11207557.png"/>Where - 
- Poly-Tree = Tree with polynomials at the  nodes
- Transformed-input = apply the following transformation before calculating the polynomial (currently n=3 is hard-coded):<img src="/attachments/11207537/11207550.png"/>
- Noisy-Indexing = apply logistic function on value, with minimal/maximal values moved from [0.0,1.0] to [ε,1-ε'], and then use that as probability for deciding on the dichotomic Treatment/Outcome
- +/- = requiring that the first-order contributions of a parameter to the polynomial is set to be positive (negative)
- 
Parameters for running the generation are:
```bash
generate_realistic_data --help
Program options:
  --help                               produce help message
  --seed arg (=12345)                  randomization seed
  --scale arg (=1)                     scale of random features
  --nSamples arg                       number of samples
  --numA arg                           # of variables affecting only treatment
  --numB arg                           # of variables affecting treatment and
                                       outcome (confounders)
  --numC arg                           # of variables affecting only outcome
  --polyDegree arg (=3)                polynom model degree
  --treatmentPolyDegree arg (=1)       polynom model degree for treatment
  --outcomePolyDegree arg (=1)         polynom model degree for outcome
  --pTreatment arg                     probablity of applying treatment
  --treatSigMax arg (=0.899999976)     maximal value of treatment probability
  --treatSigMin arg (=0.0500000007)    minimal value of treatment probability
  --treatSigWidth arg (=0.100000001)   width of treatment sigmoid function
  --pOutcome arg                       probablity of positive outcome
  --outSigMax arg (=0.975000024)       maximal value of output probability
  --outSigMin arg (=0.0250000004)      minimal value of output probability
  --outSigWidth arg (=0.5)             width of output sigmoid function
  --treatmentFactor arg (=0.150000006) Scaling factor of Treatment before
                                       outcome calcluation
  --matrix arg                         output matrix file (bin)
  --params arg                         output params file (bin)
  --output arg                         output log file
  --risk arg                           output risk scores file
```
Note that - 
  - Currently, the depth of the trees is hard-coded as depth=2
  - SigWidth determine the scaling of the logistic function, normalized by the distribution of the input variable. The lower it is, the lower the slope at the step is (i.e., very large widths correspond to step function)
  - Features  are generated as Uniform[0,**]
  - Treatment is scaled by treatmentFactor before application of final polynomial
  - risk is a debugging output matrix giving various intermediate values (e.g. Outcome/Treatment/Risk scores, various probabilities, *etc*.)
  - The models are written into ****.bin and ****.treatment.bin
Additional projects in the same solution include - 
  - 
Generate matrices given the model:
```bash
generate_realistic_data_from_model --help
Program options:
  --help                 produce help message
  --seed arg (=12345)    randomization seed
  --scale arg (=1)       scale of random features
  --nSamples arg         number of samples
  --numA arg             # of variables affecting only treatment
  --numB arg             # of variables affecting treatment and outcome
                         (confounders)
  --numC arg             # of variables affecting only outcome
  --matrix arg           output matrix file (bin)
  --params arg           input model params file (bin)
  --treatment_params arg treatment model params file (bin)
  --output arg           output log file
  --rct_p arg            RCT data. Randomize Treatment with given probability
```
The program generates a random feaures matrix (Uniform[0,**]), either uses ****.treatment.bin to set the treatment or randomly selects it (if ** is given) for a Randomized Controlled Trial scenario, and then uses ****.bin to set the output
 
  - 
Various utilities for handling the synthetic data/model -
```bash
utils --help
Program options:
  --help                produce help message
  --mode arg            what should I do ?
  --matrix arg          matrix to use for evaluation
  --dir arg             directory for outcome and treatment models
  --preds arg           predictions to evaluate
  --epreds arg          e predictions for evaluation
  --mpreds arg          m predictions for evaluation
  --model arg           model to print
  --out arg             output file
  --csv arg             input csv file
  --bin arg             output bin file
```

Possible modes include:
1. **print** - get a human-readable version of a generative model (from *params.**bin*****
2. **getProbs** - generate a vector of the output probabilities given a matrix and a model
3. **getAUC** - get the maximal possible AUC for outcome prediction (known true probabilities)
4. **csv2bin** - translate a *csv* matrix to binary format (serialized MedFeatures)
 
