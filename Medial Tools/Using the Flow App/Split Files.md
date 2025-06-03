# Split Files
A split file contains a list of pids split into several splits. Keeping the split in a file allows using the exact same split over several runs, or between stages such as creating a matrix with completions and modeling it.
Pids not appearing in the split file should always be assumed to not be used.
 
## Format
 
Comment lines start with # .
File is tab or space delimited.
first line:
NSPLITS <number of splits>
Followed by tupples:
<pid> <split>
 
## The MedSplit Class
Defined in MedFeat/MedOutcome.h , this class contains the basic tools to create splits, and read/write them to files.
