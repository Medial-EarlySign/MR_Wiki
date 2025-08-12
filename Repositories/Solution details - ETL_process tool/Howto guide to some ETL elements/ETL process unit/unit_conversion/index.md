# unit_conversion
There is a library unit_conversion.py under ETL_Infra
that has 2 main functions:

- process_unit_conversion - which generates a file with statistics about signals+units sorted by frequency and conversion table. Inputs:
    - fullDF - the dataframe to analyze with "signal" column, "unit" column as name of unit column, and "value_0" as the value
    - outFile - where to store output file of the conversion table config with the stats
    - samples_per_signal - how many examples to fetch for each group
Output: None, writes the conversion file with the stats in outFile - fix_units - which runs the unit conversion. Inputs
    - fullDF -  the dataframe to with "signal" column, "unit" column as name of unit column, and "value_0" as the value
    - inFile - path to conversion config file after editing
Output: dataframe after commiting the unit conversion
 
Recommendations:
To use in labs processing, steps:

1. First time call with ""  "generate_labs_mapping_and_units_config" from etl_process. the input arguments are: (df - the dataframe with "signal" column, "unit" column as name of unit column)
2. Edit the conversion table
3. l and add the usage call with "" "map_and_fix_units" from etl_process: same inputs as in "generate_labs_mapping_and_units_config". Returns the fixed dataframe
 
Example usage inside "labs.py" processings:
```python
generate_labs_mapping_and_units_config(df)
#edit the file and after editing the file, you can comment out the line above to speedup running (no need to recalculate) and run again. Now the next line with "map_and_fix_units" will actually do something
df=map_and_fix_units(df)
```
