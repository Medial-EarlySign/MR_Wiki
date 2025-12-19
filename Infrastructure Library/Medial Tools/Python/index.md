# Python

## Quick Start

We provide three libraries for use:

1. **MedPython**: A Python library that integrates with our C library.
2. **ETL Library**: A pure Python utility designed to assist in creating Data Repositories.
3. **AlgoMarker API Server**: A pure Python server wrapper for utilizing the AlgoMarker library (limited to predict/apply for implementation setting. Much lighter as opposed to MedPython).

> **Note**: These libraries are currently available as PyPi package. To use them, just type pip install medpython. For more information: [Setup](#setup)

## Pages

* **MedPython**
    - [Examples](Examples.md): Usage examples for MedPython.
    - [Python Binding Troubleshooting](Python%20binding%20Troubleshooting.md): Guidance for troubleshooting Python bindings in MedPython.
    - [Extend and Develop](Extend%20and%20Develop.md): Instructions for exposing additional C++ APIs to Python.
* **ETL Library**: Refer to the [ETL Tutorial](../../../Tutorials/01.ETL%20Tutorial) for more details.
* **[Python AlgoMarker API Server](Python%20AlgoMarker%20API%20Server.md)**: Documentation for the pure Python FastAPI server of the AlgoMarker library.

### Setup

#### Using PyPI
```bash
pip install medpython
```

Usage
```python
import med
from AlgoMarker import AlgoMarker
from ETL_Infra import prepare_final_signals, prepare_dicts, finish_prepare_load, create_train_signal
```

More information on usage:

* [ETL_Infra](../../../Tutorials/01.ETL%20Tutorial) 
* [AlgoMarker](Python%20AlgoMarker%20API%20Server.md#simple-usage-example)
* [med library](Examples.md)

### Use From Source Code

1. **Clone the Git Repositories**:
    * git clone [medpython](https://github.com/Medial-EarlySign/medpython).git MR_LIBS
    * git clone [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools).git
2. **Set Up MedPython**:
   Follow the instructions in [Setup MedPython](../../../Installation/index.md#4-python-api-for-mes-infrastructure).
   The **ETL Library** and **AlgoMarker API Server** are pure python code, so you can just configure environment variable of PYTHONPATH to use them from source code. 
3. **Configure Environment Variables**:
   Ensure Python recognizes the libraries by setting the `PYTHONPATH` environment variable. Replace `${MR_TOOLS}` with the path to the cloned `MR_Tools` repository.

   ```bash
   export PYTHONPATH=${MR_TOOLS}/RepoLoadUtils/common
   ```
