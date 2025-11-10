# DataRepository
* How to load a new DataRepository, please follow [ETL Tutorial](ETL%20Tutorial). It is recommanded to use this tool. It contains testing and final formatting that makes the loading easier.
* How to load a new DataRepository without the ETL Tool [Loading a DataRepository](Load%20new%20repository.md)
    - Explanation on [Data Repository Signal config](Repository%20Signals%20file%20format.md) files (definition of the data scheme, name of signals and types)

## ETL Tool - TODOs
- Extend tests
    - Add more numeric test, compare dists to MHS,THIN percentiles. test resolution
- parallel the processing
- Join with BDATE to extract age for stats/filters?