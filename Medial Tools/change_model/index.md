# change_model

This tool allows you to **modify components within an existing MedModel** without the need to retrain the entire model. It's an efficient way to make targeted adjustments to a model's pipeline, especially for production, testing, or debugging purposes.
This tool, is part of the [AllTools compilation](../Installation/index.md#3-mes-tools-to-train-and-test-models)

Common use cases include:

* **Modifying Production Settings**: nable special flags in components like `RepBasicOutlierCleaner` to store outlier information. This process is typically slower and more memory-intensive, so you might only want to activate it in production.
* **Controlling Pre-processing**: Temporarily disable or adjust pre-processing steps like normalization or imputation for specific testing or data matrix creation.
* **Adjusting `ButWhy` Explanations**: Change arguments for the explainability component, such as the number of contributors to output, without re-learning the model.

`change_model `supports both **interactive** and **non-interactive** command-line interfaces for controlling and modifying model objects.
 This documentation focuses on the non-interactive use case, which is most common for scripting and automation.

## Arguments

There are two primary methods for using change_model in non-interactive mode: 
a simple one-liner for a single change or a JSON file for multiple, more complex changes.

### Method 1: Single Change via Command Line

For a single, quick modification, use the `--search_object_name` and `--object_command` flags.

#### Example: Disabling Outlier Attribute Storage

This command finds all `RepBasicOutlierCleaner` objects and clears the attributes used for storing outlier information, effectively disabling that feature to improve performance.

```bash
change_model --model_path <model_path> --output_path <output_model_path> --interactive_change 0 --search_object_name RepBasicOutlierCleaner --object_command "nrem_attr=;nrem_suff=;ntrim_attr=;ntrim_suff="
```

* `--model_path`: Path to your existing model file.
* `--output_path`: Path where the modified model will be saved.
* `--interactive_change`: `0` Activates non-interactive mode. Default is `1`
* `--search_object_name`: The name of the object to find and modify. In this case, `RepBasicOutlierCleaner`.
* `--object_command`: A string of semicolon-separated `key=value` pairs to set new parameters. To **delete** an object, use `"DELETE"`.

### Method 2: Multiple Changes via JSON File

For complex or multiple modifications, you can provide a JSON file containing all your change instructions using the `--change_model_file` argument. This file will be used to initiate a `ChangeModelInfo` object, which then executes the requested changes.

#### JSON Change Block Structure

The JSON file contains an array of "change blocks," where each block defines a specific modification.

```json
{ 
  "changes": [
       // Define your change blocks here
  ]
}
```

Each block has the following parameters:

```json
{
    "change_name": "<name_for_logging>",
    "object_type_name": "<The object we seek to change>",
    "json_query_whitelist": [ "<string list of regex items>" ],
    "json_query_blacklist": [ "<string list of regex items>" ],
    "change_command": "<command string>",
    "verbose_level": "<verbosity level for this action (optional)>"
}
```

* `json_query_whitelist`: A list of regular expressions. A component will only be selected if its string representation matches **all** regex strings in this array (AND condition).
* `json_query_blacklist`: A list of regular expressions. A component will be **filtered out** if its string representation matches **any** regex string in this array.

> **Warning!**: Be extremely cautious when modifying a model. Only change things that do not require re-training. For instance, do not remove features that are essential for the classifier to function correctly.

### JSON Examples

#### Example 1: Remove Normalizers and Imputers

This example shows how to selectively remove specific normalizers and all imputers. The first block uses `json_query_whitelist` to target only the `FeatureNormalizer` objects for `Age` and `Gender` while leaving others untouched. The second block removes all `FeatureImputer` objects.

```json
{ 
  "changes": [
       {
			"change_name":"Remove Normalizers",
			"object_type_name":"FeatureNormalizer",
			"json_query_whitelist": [ "Age|Gender" ],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"2"
	   },
	   {
			"change_name":"Remove Imputers",
			"object_type_name":"FeatureImputer",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"2"
	   }
  ]
}
```
### Example 2: Multiple Modifications in One File

This example demonstrates how to perform several changes in a single operation: 

* Removing outlier attributes - that reports on outliers. makes think slower and consume more memory.
* Deleting RepCheckReq objects - that checks eligibility criteria. makes think slower and consume more memory.
* adjusting the `max_data_in_mem` parameter for the `MedModel` object itself, to adjusts the model's memory limit to process larger prediction batches.

```json
{ 
  "changes": [
       {
			"change_name":"Remove attributes from cleaners",
			"object_type_name":"RepBasicOutlierCleaner",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "nrem_attr=;ntrim_attr=;nrem_suff=;ntrim_suff=",
			"verbose_level":"1"
	   },
	   {
			"change_name":"Remove attributes Req",
			"object_type_name":"RepCheckReq",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "DELETE",
			"verbose_level":"1"
	   },
	   {
			"change_name":"MedeModel Memory",
			"object_type_name":"MedModel",
			"json_query_whitelist": [],
			"json_query_blacklist": [],
			"change_command": "max_data_in_mem=0",
			"verbose_level":"1"
	   }
  ]
}
```
