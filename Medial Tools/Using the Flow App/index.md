# Using the Flow App
### General
The Flow App Currently contains the options to:

- create a repository, and a transposed repository (by pid)
- print all signals records for a specific pid
- print records for a specific pid,sig
 
The Flow App assumes the latest Mode 3 repository version is used. Many things might work for previous versions, but it is not guaranteed.
 
Git link: [https://github.com/Medial-EarlySign/MR_Tools/tree/main/Flow](https://github.com/Medial-EarlySign/MR_Tools/tree/main/Flow)
### Flow App Options
 
#### General
****
get help message with all options
****
input repository when needed
****
input convert_config file when needed
****
input pid number when needed
****
input signal name when needed
 
#### Creating Repositories
****
Create a repository given a convert config file. The convert config file is given using the --convert conf option
*example:* Flow --rep_create --convert_conf ./ICU.convert_config
 
****
Create a by pid transposed version of a repository. This is a very useful option that allows for a very fast access to a specific pid and all its signals, rather than all the pids for a specific signal which is the default repository. This can dramatically enhance performance when going over a repository, while lowering the memory consumptions in orders of magnitude (for example when going over a selected group of pids, and creating feature vectors for them).
The input repository is given using the --rep option.
*example:* Flow --rep_create_pids --rep ./ICU.repository
 
#### Printing pids and signals
****
Print all records for all signals for a certain pid given in the --pid option. This one uses the default API. The repository is given in the --rep option.
*example:* Flow --rep ./ICU.repository --printall --printall --pid 200001
**
Print all records for all signals for a certain pid given in the --pid option. This one uses the by-PID API, and hence is faster, but requires that it was created. The repository is given in the --rep option.
*example:* Flow --rep ./ICU.repository --pid_printall --pid 200001
****
Print all records for a given signal (–sig) for a certain pid (–pid) for a repository (–rep). This one uses the default API.
*example:* Flow --rep ./ICU.repository --print --pid 200001 --sig Sepsis
****
Print all records for a given signal (–sig) for a certain pid (–pid) for a repository (–rep). This one uses the by-PID API, and hence is faster, but requires that it was created.
*example:* Flow --rep ./ICU.repository --pid_print --pid 200001 --sig Sepsis
**
Print a general statistics for a signal: how many samples are there, for men, for women, avg samples per person, general distribution, rounding info, years and months distributions, etc.
Currently this option will work only on SDateVal type signals and a repository that contains the GENDER and BYEAR signals.
*example:* Flow --rep ./thin.repository --describe --sig Creatinine
 
 
 
 
