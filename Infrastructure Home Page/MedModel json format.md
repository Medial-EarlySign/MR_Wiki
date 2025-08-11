# MedModel JSON Format

Refer to `MedModel::init_from_json_file` for implementation details.

## General Fields

Use only the first field, `"model_json_version"`, the rest have default values so change them only if needed:

- `"model_json_version"`: Specify `2`.
- `"serialize_learning_set"`: Boolean (`0` or `1`). If enabled, stores learning samples in the model. Default: `0`.
- `"generate_masks_for_features"`: Boolean (`0` or `1`). If enabled, stores for each feature whether the value was imputed (important for explainers and MASK predictor during calibration). Default: `0`.
- `"max_data_in_mem"`: Maximum size of a vector the machine can hold (default: `MAX_INT`). Limits number of rows × number of features. Larger values split model apply into batches.
- `"take_mean_pred"`: Boolean (`0` or `1`). If enabled, averages predictions; otherwise, uses median. Default: `1`. Currenly relevant only for [Multiple Imputations](PostProcessors%20Practical%20Guide/MultipleImputations.md) mode

You can use these prefixes for referencing files relative to the JSON:

- `path_rel:`: References a file with a relative path, resolves to absolute path from JSON location.
- `file_rel:`: References a file, extracts content line by line into a list of actions (`["line1", "line2", ...]`).
- `comma_rel:`: References a file, extracts content line by line into a comma-separated string (`"line1,line2,..."`).
- `json:`: References another file, adds its content to this JSON as-is.

The parameters in the model can be later changed using [adjust_model](/Medial%20Tools/adjust_model.md)or [change_model](/Medial%20Tools/change_model).
For example, if you are implementing running an existing model in lower memory computer, you might want to lower down `max_data_in_mem`.
[Howto limit memory](/Medial%20Tools/change_model/How%20to%20limit%20memory%20usage%20in%20predict.md)

## Main Model Pipeline

Model pipeline instructions are listed under `"model_actions"` (an array of model components):

```json
{
  "model_json_version": "2",
  "model_actions": [
    // List model components here, each as an object {}
  ]
}
```

### List Expansion

When specifying a list of values for a field, the element is duplicated for each value:

```json
{
  "field_1": "A",
  "field_2": ["val_1", "val_2", "val_3"]
}
```

Is equivalent to:

```json
{ "field_1": "A", "field_2": "val_1" },
{ "field_1": "A", "field_2": "val_2" },
{ "field_1": "A", "field_2": "val_3" }
```

Multiple lists create a cartesian product of all options.

## Model Components

Components inside `"model_actions"` are executed in order. Blocks can be executed in parallel; feature generators are always parallel.

Each component has an `"action_type"` field (default: `"feat_generator"`). Place it first for readability.

Available `action_type` options:

- `rp_set`: Set of [rep_processors](Rep%20Processors%20Practical%20Guide) executed in parallel. Contains `"members"` (array of rep_processors, each with `"rp_type"` and parameters).
- `fp_set`: Set of [feature_processors](FeatureProcessor%20practical%20guide) executed in parallel. Contains `"members"` (array of feature_processors).
- `rep_processor`: Single rep_processor. See [Rep Processors Practical Guide](Rep%20Processors%20Practical%20Guide) or [RepProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/RepProcess_8h.html#a2772b5cb2b32efafbbd8ba9440b9576a).
- `feat_generator`: Feature generator. See [Feature Generator Practical Guide](FeatureProcessor%20practical%20guide) or [FeatureGeneratorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureGenerator_8h.html#a109794c7f375415720a0af5dd3132023).
- `feat_processor`: Feature processor. See [Feature Processor Practical Guide](FeatureProcessor%20practical%20guide) or [FeatureProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/FeatureProcess_8h.html#ae648a97312d7df5b3f5cf01b19887334). To apply on multiple features, add `"tag"` (value to search for features) and `"duplicate": "1"`. This creates a MultiFeatureProcessor that scans all features, generating child processors after filtering by tag.
- `post_processor`: Feature processor. See [PostProcessors Practical Guide](PostProcessors%20Practical%20Guide) or [PostProcessorTypes](https://Medial-EarlySign.github.io/MR_LIBS/PostProcessor_8h.html#a1dab070b8206be89206ff19f321a1cfc).

Example of `"rp_set"` block (similar for `"fp_set"`):

```json
{
  "action_type": "rp_set",
  "members": [
    // List rep processor components here, each as an object with "rp_type" field...
  ]
}
```

## Predictor

In the last part of the JSON, after `"model_actions"`:

- `"predictor"`: Selects MedPredictor to train on the generated matrix. See [MedPredictor practical guide](MedPredictor%20practical%20guide) and [List of options](https://Medial-EarlySign.github.io/MR_LIBS/MedAlgoh.html#ab3f9aacffd8e29e833677299133ac4f0). Examples: `"xgb"` for xgboost, `"lightgbm"` for LightGBM, `"lm"` for linear model, etc.
- `"predictor_params"`: Arguments to initialize the predictor, depending on the chosen predictor.

## Reference Lists

- You can add lists of values at the end for reference in the model_actions. For example, `"diabetes_drugs": "ATC_A______,ATC_...."` can be referenced using `"ref:diabetes_drugs"` in the model_actions.
