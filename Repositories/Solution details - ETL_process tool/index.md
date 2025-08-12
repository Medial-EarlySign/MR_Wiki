# Solution details - ETL_process tool
In Tools repository, there is a file called "etl_process.py" Under Tool/RepoLoadUtils/common/ETL_Infra.
****TARGET:****
Implement ETL process which satisfies following requirements:

- Interactive
- Assumes that the user has no prior knowledge of ETL process
- Efficient in loading time, memory handling
- Improve code reuse, minimal configuration files/settings and speedup development. CoC (Convention over Configuration)
- Organized process that is easy to follow and easier to reproduce with logging
****
We assume that most of the actions specific to loading a new dataset are simple,
e.g. renaming of columns, date format conversion etc. Most of this logic can't be reused and most of the time is to define them.
****

- Interactive part should have verbose and informative messages
- Actions common to all ETL processes should be automated
- Configuration files should be kept in one place / under one path
- Specific ETL is allowed to override specific parts of a default configuration
- Verbose logging should be implemented
- Checkpoints should be saved during ETL process
- ETL process should be able to run starting from a specific checkpoint
- Batch loading/processing of the data should be implemented - for example in first run small data batch will be pulled for debugging
- The ETL code should support calling external extensions (define API or at least places in the code where the custom calls should be placed)
- Improve the documentation of the process - each section should be shorter and better divided
- Provide both windows/Unix path + open the file automatically if not canceled            
[High level - important paths/structure](High%20level%20-%20important%20paths)
[ETL process unit](Howto%20guide%20to%20some%20ETL%20elements/ETL%20process%20unit)
[ETL_process TODO](ETL_process%20TODO.md)
 
