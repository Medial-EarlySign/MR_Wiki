# ETL Process – Dynamic Testing of Signals

You can define **both global tests** (applied across all ETL processes) and **local tests** (specific to a given ETL process).  
Local tests can override global tests if they share the same name in the local path.

---

## Test Locations
- **Global tests:** `$MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra/tests`
- **Local tests:** `$CODE_DIR/tests`

The code is executed from  
`$MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra`.  
This means you can use **relative paths** to access config files, dictionaries, etc.

---

## Test Organization
- Each test directory (global or local) contains subdirectories for groups of tests.
- Subdirectory names correspond to either:
    - A **signal name**, or  
    - A **group of signals** (e.g., `"labs"`, `"cbc"`).  
- Only signals matching the directory name will be tested.

---

## Test Function Format
Each test file must include a function called `Test` with the following signature:

```python
def Test(df: pd.DataFrame, si, codedir: str, workdir: str) -> bool:
```

### Arguments:
* df: Input dataframe containing the signal to test
* si: Signal information object
    - si.t_ch: Array of time channel types (i = int, f = float, etc.)
    - si.v_ch: Array of value channel types
* codedir: Path to the ETL code (useful for accessing the config folder)
* workdir: Working directory for storing outputs

### Return value:
* True if the test passes
* False if the test fails

## Example Test
Path:
`$MR_ROOT/Tools/RepoLoadUtils/common/tests/labs/test_non_nulls.py`

```python
import pandas as pd

def Test(df: pd.DataFrame, si, codedir: str, workdir: str):
    if len(df) == 0:
        return True
    cols = [x for x in df.columns if x == "pid" or "value" in x or "time" in x]
    sig_name = df["signal"].iloc[0]
    # si.t_ch - contains array of each time channel type (for example "i" is integer, "f" float). v_ch is the same for value channels.
    signal_columns = ["time_%d" % (i) for i in range(len(si.t_ch))] + [
        "value_%d" % (i) for i in range(len(si.v_ch))
    ]
    signal_columns.append("pid")
    for col in cols:
        if col not in signal_columns:
            print(f"Skip columns {col} which is not needed in signal {sig_name}")
            continue
        null_date_cnt = len(df[df[col].isnull()])
        if null_date_cnt / len(df) > 0.001:
            print(
                "Failed! There are %d(%2.3f%%) missing values for signal %s in col %s"
                % (null_date_cnt, 100 * null_date_cnt / len(df), sig_name, col)
            )
            return False
        if null_date_cnt > 0:
            print(
                "There are %d(%2.3f%%) missing values for signal %s in col %s"
                % (null_date_cnt, 100 * null_date_cnt / len(df), sig_name, col)
            )
        df.drop(df.loc[df[col].isnull()].index, inplace=True)  # clean nulls
        df.reset_index(drop=True, inplace=True)
    print("Done testing nulls in signal %s" % (sig_name))
    return True
```
This test verifies that no more than 1% null values exist in pid, time_0, value_0 for all labs signals.
You can copy it into a local directory and adjust thresholds as needed.

## Plotting Graphs 
To generate HTML plots, use the plot_graph function:

```python
import sys, os
from ETL_Infra.plot_graph import plot_graph
```

* Input:
    - A dataframe with two columns, or
    - A dictionary {name: dataframe} (to plot multiple series)

## Running Tests on Signals
You can run or rerun tests with:

```bash
python $MR_ROOT/Tools/RepoLoadUtils/common/ETL_Infra/run_test_on_sig.py \
  --workdir $WORKDIR \
  --codedir $CODEDIR \
  --signal $SIGNAL
```
* --signal can accept multiple signals (comma-separated).
