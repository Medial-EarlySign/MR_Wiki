# Setup

To begin working with the ETL infrastructure, you need to clone the repository. 
Note that this is not a PyPI package; it is designed to be used as part of the environment/codebase.

## Clone the Repository

Start by cloning the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) repository from GitHub to a folder on your computer.

## Configure Python to Recognize the Library

### Option 1: Update Your Environment Variable

The easiest way to use the infrastructure is by adding the "**RepoLoadUtils/common**" directory to your `PYTHONPATH` environment variable. This allows you to directly import modules from the ETL infrastructure in any Python file.

### Option 2: Modify Individual Python Files

If you prefer not to modify your environment settings, you can add the following code snippet at the beginning of each Python file that needs access to the ETL infrastructure. This temporarily adds the required directory to the system path, enabling module imports.

```python
import sys
# Replace "ABSOLUTE PATH TO" with the actual path on your computer
sys.path.insert(0, "ABSOLUTE PATH TO RepoLoadUtils/common") 
# Now you can import the needed modules from ETL_Infra
``` 

## Verify the Setup
To confirm everything is set up correctly, run the following command:

```bash
python -c 'import ETL_Infra'
```

Alternatively, if using Option 2, wrap the snippet in a script and add `import ETL_Infra` at the end to verify it works.

## Next Steps

The first step in the ETL process is to create a module or script that fetches data in batches. This method is highly efficient and preferred over returning a single `DataFrame` from a simple function.

Follow the detailed instructions in the [Data Fetcher](01.Data%20Fetching%20step) documentation to begin.