# Data Fetching Step

The goal of this step is to create a function that returns a **lazy iterator** for data. This function, `fetch_function`, will fetch data in manageable batches, defined by a `batch_size` and a `start_batch` index. This approach is memory-efficient and ideal for large datasets.

```python
def fetch_function(batch_size:int, start_batch:int) -> Generator[pd.DataFrame, None, None]
```

This step happens after [Setup](../00.Setup) and after creating a directory for source code of this current ETL process.
Note: The folder for our current ETL process is refered as `CODE_DIR` and list of files/strucutre can be seen in [CODE_DIR](../../ETL%20Tutorial/High%20level%20-%20important%20paths/CODE_DIR.md). We will start with an empty direcotry and the ETL infrastracture will create some of the files for you.

## Step-by-Step Guide: File-Based Example

This guide uses a file-based example to demonstrate the process, but the same principles apply to other data sources like databases (We also have helper functions for DBs).

### 1. Setup and Imports

First, import the necessary helper libraries. The example uses pre-built functions for file handling.

```python
from ETL_Infra.data_fetcher.files_fetcher import files_fetcher, list_directory_files, big_files_fetcher
```
### 2. List Files Helper Function

Create a helper function to list all relevant files from your raw data directory. This function should return a list of full file paths. You can use a regular expression (`file_regex`) to filter the files. It's a good practice to handle one file type or format at a time.

We will use the helper function `list_files` that does that using regex.
If there are multiple folders, you can write your own code to list full file paths to read/process.

```python
def list_files(file_regex: str)-> list[str]:
    base_path = '/nas1/Data/client_data'
    return list_directory_files(base_path, file_regex)
```
 
### 3. File Path Parsing Function

Next, write a function to read and parse a single file into a Pandas DataFrame. The only **required constraint** is that the resulting DataFrame must include a `pid` (patient identifier) column.

```python
def read_single_file(file_path: str) -> pd.DataFrame:
    """
    Reads a single file into a DataFrame.

    :param file_path: Path to the file to be read.
    :return: DataFrame containing the data.
    """
    df = pd.read_csv(file_path, sep="\t")
    # Ensure the DataFrame contains a "pid" column
    return df
```
### 4. The Data Fetcher Function

The final step is to create the main data fetcher, which acts as a "lazy" generator. 
This function uses the `files_fetcher` helper to read files in batches, returning a concatenated DataFrame for each batch. 
This **lazy execution** is a key feature; data is only loaded when you iterate over the result, which is useful for debugging and fast testing or reruning the full load script again and skiping actaul reading of the data if the processings was already completed.

We will use `list_files` that we wrote before and `read_single_file` and will return a function with desired signature as described in `fetch_function`.

```python
def generic_file_fetcher(
    file_pattern: str,
) -> Callable[[int, int], Generator[pd.DataFrame, None, None]]:
    """
    Creates a file fetcher function that reads files matching the given pattern.

    :param file_pattern: Pattern to match files.
    :return: A function that fetches files in batches based on requested batch size and starting index.
    """
    file_fetcher_function = lambda batch_size, start_batch: files_fetcher(
        list_files(file_pattern),
        batch_size,
        read_single_file,
        start_batch,
    )
    return file_fetcher_function
```
 
### Example Usage

Here’s how you can use the generic_file_fetcher to test and debug your data pipeline. 
This example creates a dummy file and then uses the fetcher to read it in batches.

```python
# Example Usage
import pandas as pd
import os

data = pd.DataFrame(
    {"pid": [1, 2, 3, 4, 5], "value": [1988, 1999, 2000, 2001, 2002]}
)
data["signal"] = "BYEAR"
# Let's store the file somewhere and update `list_files`  to use same path
BASE_PATH = "/tmp"
data.to_csv(f"{BASE_PATH}/res.tsv", sep="\t", index=False)

# Create a data fetcher for the dummy file
func_fetcher = generic_file_fetcher("res.tsv")
file_fetcher = func_fetcher(1, 0)  # Read one file at a time, starting from index 0

print("Iterating on batches:")
for i, df in enumerate(file_fetcher):
    print(f"Batch {i}:\n{df}")
```

### Dummy example

Another dummy example of writing a data fetcher directly, but without helper functions in step 2+3.
Just demonstarting the usage of `yield` in python.
```python
def dummy_data_fethcer_of_fake_data(batch_size, start_batch):
	#In this simple funtion, we ignore the "batch_size, start_batch" and returns lazy iterator with 2 DataFrames
	yield pd.DataFrame({'pid':[1,2,3], 'data':['A','B', 'C']})
	yield pd.DataFrame({'pid':[4,5,6], 'data':['D','E', 'F']})
```
This will result in lazy iterator with 2 batches of dataframe.

### Handling big files

For very large files, you might need to process them by rows rather than by entire files. The `big_files_fetcher` helper function is designed for this. It requires a different type of `read_single_file` function that can handle row-based chunks.

```python
def read_single_file_by_rows(
    filepath: str, batch_size: int, start_from_row: int
) -> Generator[pd.DataFrame, None, None]:
    """
    Parses a file in chunks, yielding DataFrames of specified batch size as number of rows.

    :param filepath: Path to the file to be parsed.
    :param batch_size: Number of rows per batch.
    :param start_from_row: Row index to start reading from.
    :return: Generator yielding DataFrames.
    """
    # manipulate the file reading parameters as needed (keep chunksize and skiprows):
    has_header = True  # Set to False if the file has no header
    header = None
    if has_header and start_from_row > 0: # read header if skiping first row
        header = pd.read_csv(filepath, sep="\t", nrows=0).columns.tolist()
        start_from_row += 1

    df_iterator = pd.read_csv(
        filepath,
        names=header,
        sep="\t",
        skiprows=start_from_row,
        chunksize=batch_size,
    )
    for df in df_iterator:
        # Do manipulations on df if needed or just return `df_iterator`
        yield df
```

This modified function allows the `big_files_fetcher` to read a specified number of rows per batch, moving to the next file only when the current one is exhausted.

Full usage/replacement for `generic_file_fetcher` can be seen here:

```python
def generic_big_files_fetcher(
    file_pattern: str,
) -> Callable[[int, int], Generator[pd.DataFrame, None, None]]:
    """
    Creates a data fetcher function for large files, reading them in batches.
    Iterates over files matching the given pattern and processes them in chunks by reading rows.

    :param file_pattern: Pattern to match files.
    :return: A function that fetches files in batches based on requested batch size, starting index.
    batch_size controls the number of rows read from each file. When file ends, it will read the next file.
    """
    # Use the labs_file_parser_lazy to read files in chunks
    files = list_files(file_pattern)
    data_fetcher_function = lambda batch_size, start_batch: big_files_fetcher(
        files,
        batch_size,
        read_single_file_by_rows,
        has_header=True,
        start_batch=start_batch,
    )
    return data_fetcher_function
```

## Next Step: Process Pipeline

Once you have your data fetcher function, you can pass it as an argument to the next step: creating a process pipeline for each data type.
Follow [this guide](../02.Process%20Pipeline) to continue
