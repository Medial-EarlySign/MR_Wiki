# Medial Tools

This section provides a list of applications, tools, and executables built on the AlgoMedical library framework:

- [Guide for Common Actions](Guide%20for%20common%20actions)
- [Using the Flow App](Using%20the%20Flow%20App): A versatile application with multiple switches, each triggering a specific action. Below are some of the key functionalities:
    - Load New Repository
    - Train a model
    - Apply a model to generate predictions.
    - Extract feature matrices from the model pipeline.
    - Print specific patient data or signal distributions.
    - Feature Importance with Shapley Values Analysis
    - more...
- [Bootstrap App](bootstrap_app): A tool for bootstrap analysis of prediction and outcome files.
    - [Bootstrap Legend](bootstrap_app/Bootstrap%20legend.md) - The bootsrap output file result legend
    - [Extending Bootstrap](bootstrap_app/Extending%20bootstrap):
        - [Using Harrell C Statistics](bootstrap_app/Extending%20bootstrap/Using%20Harrell%20C%20Statistics.md).
    - [Utility Tools for Processing Bootstrap Results](bootstrap_app/Utility%20tools%20to%20process%20bootstrap%20results.md).
    - [Versions](bootstrap_app/Versions.md).
- [Optimizer](Optimizer.md): A tool for hyperparameter optimization.
- [TestModelExternal](TestModelExternal.md): Compares repositories or samples by building a propensity model to identify differences.
- [Change Model](change_model): Modifies a model without retraining, such as enabling verbose mode for outliers or limiting memory batch size.
    - [How to Limit Memory Usage in Predict](change_model/How%20to%20limit%20memory%20usage%20in%20predict.md).
- [Adjust Model](adjust_model.md): Adds components like rep_processors or post_processors to a model. Some components may require training with MedSamples and a repository.
- [Iterative Feature Selector](Iterative%20Feature%20Selector.md): Iteratively selects features or groups of features in a top-down or bottom-up manner and generates a report.
- [GANs for Imputing Matrices](GANs%20for%20imputing%20matrices):
    - [Training Masked GAN](GANs%20for%20imputing%20matrices/TrainingMaskedGAN.md).
- [Fairness Extraction](Fairness%20extraction.md): Calculates fairness metrics.
- [Model Signals Importance](model_signals_importance.md): Evaluates the importance of signals in an existing model and measures the impact of including or excluding them on performance.
- [Simulator](Simulator.md): Simulates performance by controlling variables such as target population age distribution and key covariates. It also evaluates the impact of signal availability and existence.

## Examples of Simple Applications

To learn how to create your own applications, clone the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository. Navigate to the `MedProcessUtils` directory and explore the following examples:

* `learn` - Application.
* `getMatrix` - Application.
* `predict` - Application.

## Retired Applications

- [Action Outcome Effect](action_outcome_effect.md): A tool for estimating the average treatment or action effect on outcomes. It also supported feature selection, model selection, training, and bootstrap analysis with recovery and step-skipping capabilities.
- [Signals Dependencies](SignalsDependencies.md): Identifies statistical dependencies between registry and signal values within a time window. Useful for selecting categorical signals.
- [Create Registry](create_registry):
    - [Create Membership Registry Example Command](create_registry/Create%20Membership%20registry%20example%20command.md).
- [Find Required Signals](Find%20Required%20Signals.md).
- [Compare AUCs](Compare%20AUC's.md).

