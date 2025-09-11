# New employee landing page

## Code to load all tools/environment:

```bash title="Start Up Script"
#!/bin/bash

# Path to Boost library
LD_PATH=${HOME}/Documents/MES/Boost/lib
# Path to Git Repo clones
MR_LIBS=${HOME}/Documents/MES/MR_LIBS
MR_TOOLS=${HOME}/Documents/MES/MR_Tools
MR_SCRIPTS=${HOME}/Documents/MES/MR_Scripts

export PATH=$PATH:${MR_TOOLS}/AllTools/Linux/Release:${MR_SCRIPTS}/Python-scripts:${MR_SCRIPTS}/Bash-Scripts:${MR_SCRIPTS}/Perl-scripts
if [ ! -z "$LD_LIBRARY_PATH" ]; then
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${LD_PATH}
else
	export LD_LIBRARY_PATH=${LD_PATH}
fi
export PYTHONPATH=${MR_LIBS}/Internal/MedPyExport/generate_binding/Release/medial-python312:${MR_TOOLS}/RepoLoadUtils/common
```

Please edit LD_PATH, MR_LIBS, MR_TOOLS, MR_SCRIPTS paths 

 

