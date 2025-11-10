# unit_conversion

The `unit_conversion.py` module in **ETL_Infra** provides utilities for managing and applying unit conversions in lab data. It includes two primary functions:


## Functions
`process_unit_conversion`

Generates a statistics file with:

* Signals and units ranked by frequency
* A conversion table for review

**Parameters**: 
* `fullDF`: DataFrame with:
    - `signal` column (signal name)
    - `unit` column (unit name)
    - `value_0` column (numeric value)
* `outFile`: Path to save the conversion table and statistics
* `samples_per_signal`: Number of sample rows per group

**Output:**
* None (writes results to `outFile`)

`fix_units`

Applies unit conversions using a prepared configuration file.

**Parameters**: 
* `fullDF`: DataFrame with `signal`, `unit`, and `value_0` columns
* `inFile`: Path to the unit conversion configuration file

**Output:**
* Returns a DataFrame with units converted

## Recommended Workflow for Lab Data

1. **Generate conversion config** - Run generate_labs_mapping_and_units_config from etl_process with your DataFrame (requires signal and unit columns).
2. **Edit the conversion table** - Review and adjust the generated table as needed.
3. **Apply conversions** - Use `map_and_fix_units` from etl_process with the same inputs to apply conversions.
This returns the updated DataFrame.

## Example usage in `labs.py`:

```python
generate_labs_mapping_and_units_config(df)
# After editing the conversion file, you can comment out the line above to avoid regenerating it.
df=map_and_fix_units(df)
```

## References

* [Example configuration file](config%20file%20of%20unit%20conversion.md)
* [Full code example](Full%20code%20example%20-%20LungFlag%20Taiwan%20labs.md)