# adjust_model

This tool, part of the [AllTools compilation](../Installation/index.md#3-mes-tools-to-train-and-test-models), is designed to modify and enhance existing models by adding new components to their processing pipelines. It's especially useful for integrating new functionalities without rebuilding the entire model from scratch.

Common use cases include:

* Adding **Post-Calibration**: You can add a post-calibration component to an existing model to fine-tune its outputs.
* **Adding Explainability**: Easily integrate new modules for model explainability.

## Command Line Interface:

The primary command for using adjust_model is:

```bash
adjust_model --rep <repository_path> --inModel <current_model_path> --out <out_model_path> --samples <path_to_samples_for_training_new_components> --preProcessors <pre_processor_addition_json> --postProcessors <post_processor_addition_json> 
```

### Arguments

* `--rep <repository_path>`: The path to the data repository. Required unless you use --inCsv.
* `--inModel <current_model_path>`: The path to the existing model file you want to modify.
* `--out <out_model_path>`: The path where the new, adjusted model will be saved.
* `--samples <path_to_samples_for_training_new_components>`: The path to the samples used for training the new components. Required if `--learn_rep_proc` is enabled or if `--skip_model_apply` is disabled.
* `--preProcessors <pre_processor_addition_json>`: A JSON string or file containing a list of pre-model processors to add to the pipeline. 
* `--postProcessors <post_processor_addition_json>`: A JSON string or file containing a list of post-model processors to add to the pipeline.

### Optional Flags

* `--inCsv`: Provide your feature matrix directly in CSV format. This is an alternative to using a repository and samples.
* `--learn_rep_proc`: When set to `1`, this flag triggers the `learn` function for the new pre-processors. This is essential for components that require training. **Note:** If you use this flag, you must also provide `--rep` and `--samples`. (Default: 0)
* `--insert_rep_proc_first`: When this flag is enabled, new pre-processors are added at the **beginning** of the existing pipeline. By default, they are appended to the end. (Default: 0)
* `--skip_model_apply`: If `1`, the model's pipeline won't be run to generate a feature matrix and samples. This can be useful for specific operations and can significantly speed up the process. (Default: `0`)
* `--model_changes`: This allows you to include instructions for modifying existing components within the model's pipeline. This can save you from having to use a separate [change_model](change_model) tool.

> **Note:** You can use either `--preProcessors` or `--postProcessors`, or both.

## JSON Templates and Examples

To add new components, you'll provide a JSON object defining the new processors. 
A "block" within this JSON corresponds to a specific processor. 
For example, a block might be a [Calibrator](Guide%20for%20common%20actions/Calibrate%20model,%20and%20calibration%20test.md) processor.


### Adding Pre-Processors
Here is a template for the `--preProcessors` argument. The `"members"` array is where you'll define each processor block.

```json
{ 
  "pre_processors": [
    {
      "action_type": "rp_set",
      "members": [
        // Your processor blocks go here
      ]
    }
  ] 
}
```
 
### Adding Post-Processors
Here is a template for the `--postProcessors` argument.

```json
{ 
  "post_processors": [
    // Your processor blocks go here
  ]
}
```

* [Full example of adding calibration](Guide%20for%20common%20actions/Calibrate%20model,%20and%20calibration%20test.md)

## How to change existing components

If you want to change and not add new components, please refere to [change_model](change_model)