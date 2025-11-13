# Training a model

1. Define the model pipeline and components in a MedModel JSON file: [MedModel JSON format](../../Infrastructure%20Library/MedModel%20json%20format.md).
2. Train the model using either:
    * Python: [Train Model Using Python API](../../Infrastructure%20Library/Medial%20Tools/Python/Examples.md#learn-model-from-json-to-generate-matrix)
    * Tools:
        * [Training with Flow](../../Infrastructure%20Library/Medial%20Tools/Using%20the%20Flow%20App/index.md#training-a-model) - simple training run without hyperparameter search
        * [Optimizer](../../Infrastructure%20Library/Medial%20Tools/Optimizer.md) - grid-search-style training with penalties to balance generalization (note: Optuna can be used externally for more flexible tuning)