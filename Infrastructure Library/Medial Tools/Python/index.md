# Python

## Quick Start

We provide three libraries for use:

1. **MedPython**: A Python library that integrates with our C library.
2. **ETL Library**: A pure Python utility designed to assist in creating Data Repositories.
3. **AlgoMarker API Wrapper**: A pure Python wrapper for utilizing the AlgoMarker library (limited to predict/apply for implementation setting. Much lighter as opposed to MedPython).

> **Note**: These libraries are not currently available as PyPi packages. To use them, you need to set the `PYTHONPATH` environment variable to their installation paths. For more information: [Setup](#setup)

## Pages

* **MedPython**
    - [Examples](Examples.md): Usage examples for MedPython.
    - [Python Binding Troubleshooting](Python%20binding%20Troubleshooting.md): Guidance for troubleshooting Python bindings in MedPython.
    - [Extend and Develop](Extend%20and%20Develop.md): Instructions for exposing additional C++ APIs to Python.
* **ETL Library**: Refer to the [ETL Tutorial](../../../Tutorials/01.ETL%20Tutorial) for more details.
* **[Python AlgoMarker API Wrapper](Python%20AlgoMarker%20API%20Wrapper.md)**: Documentation for the pure Python wrapper of the AlgoMarker library.

### Setup

1. **Clone the Git Repositories**:
    * [MR_LIBS](https://github.com/Medial-EarlySign/MR_LIBS)
    * [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools)
2. **Set Up MedPython**:
   Follow the instructions in [Setup MedPython](../../../Installation/index.md#4-python-api-for-mes-infrastructure).
3. **Configure Environment Variables**:
   Ensure Python recognizes the libraries by setting the `PYTHONPATH` environment variable. Replace `${MR_LIBS}` with the path to the cloned `MR_LIBS` repository and `${MR_TOOLS}` with the path to the cloned `MR_Tools` repository.

   ```bash
   export PYTHONPATH=${MR_LIBS}/Internal/MedPyExport/generate_binding/Release/medial-python312:${MR_TOOLS}/RepoLoadUtils/common
   ```

The Python AlgoMarker API Wrapper does not require installation. Simply run the script directly when needed.