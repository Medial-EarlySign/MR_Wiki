# unit_conversion
The `unit_conversion.py` library in ETL_Infra provides two main functions:

* `process_unit_conversion`: Generates a statistics file listing signals and units by frequency, along with a conversion table.
    - `fullDF`: DataFrame containing a "signal" column, a "unit" column (unit names), and a "value_0" column (values)
    - `outFile`: Path to save the output conversion table and statistics
    - `samples_per_signal`: Number of sample rows to include for each group

    Output:
    None (writes the conversion table and stats to outFile)
* `fix_units`: Applies unit conversions based on a configuration file.
    - `fullDF`: DataFrame with "signal", "unit", and "value_0" columns
    - `inFile`: Path to the conversion configuration file

    Output:
    Returns a DataFrame with units converted

## Recommended workflow for lab data processing:*

1. Initially, call `generate_labs_mapping_and_units_config` from `etl_process` with your DataFrame (must have "signal" and "unit" columns).
2. Edit the generated conversion table as needed.
3. Use "map_and_fix_units" from etl_process: same inputs as above) to apply the conversions. This returns the updated DataFrame.
 
Example usage in `labs.py`:

```python
generate_labs_mapping_and_units_config(df)
# After editing the conversion file, you can comment out the line above to avoid regenerating it.
df=map_and_fix_units(df)
```

## Examples

* [Example configuration file](Example%20config_output%20file%20of%20unit%20conversion.md)
* [Full code example](Full%20code%20example%20-%20LungFlag%20Taiwan%20labs.md)