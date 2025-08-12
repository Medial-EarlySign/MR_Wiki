# ETL Tutorial

## Overview

This tutorial explains how to use our ETL library, which consists of five core functions and recommended best practices. While you can use the library flexibly, following this guide will help you write maintainable, standardized ETL code. If you have suggestions for improvements, please share them so we can refine our standard together.

---

## Getting Started

1. **Create a Project Directory:**  
   Start by creating an empty directory for your ETL code:  
   [CODE_DIR](../High%20level%20-%20important%20paths/structure/CODE_DIR.md)

2. **Directory Structure:**  
   Your final `CODE_DIR` will look like this:  
   [<img src="/attachments/14811356/14811417.png"/>](#)

3. **Entry Point:**  
   Use a single entry point for your ETL:  
   - Run `python load.py` to execute the full loading process.
   - **Do not** create multiple `load.py` files or use different names. This keeps the workflow simple and consistent.

4. **Initial Setup:**  
   The `configs` and `signal_processing` folders can start empty. The ETL process will create them as needed.

---

## ETL Architecture

Our goal is to automate and reuse as much as possible across different ETL loads. You only need to write the logic specific to your input data format.

- **Note:**  
  There is no standard input format. Your main task is to transform your unique input into our defined output format. Intermediate formats are not needed.

- **Motivation:**  
  The new ETL process reduces code size by ~4x compared to the old approach, eliminates manual steps, and adds automated testing.

---

## ETL Process Steps

The ETL process is divided into three main parts:

1. **[Data Fetching](Data%20Fetching%20step.md):**  
   Write code to read your raw data into a DataFrame. This step is specific to your ETL and should be simple (e.g., `pd.read_csv()` or database queries).

2. **[Data Processing](ETL%20Processing%20Code%20Unit%20Tutorial.md):**  
   Transform the raw DataFrame into the final signal structure. This code is also ETL-specific and may include column renaming, filtering, or unit conversion.

3. **[Manager Script](ETL%20Manager%20Process.md):**  
   Write a short `load.py` script to orchestrate the data fetching and processing steps, and perform the loading. This script should be concise and readable.

---

## Code Documentation

- [Function documentation](http://node-01/ETL_Infra/) is generated using pydoc.
- To build the documentation manually:
  ```
  pushd $ETL_LIB_PATH/docs && make html && popd
  # The documentation will be at:
  $ETL_LIB_PATH/docs/build/html/index.html
  ```
- **Note:**  
  Documentation is updated automatically on each git push to the tools repository.

<img src="/attachments/14811356/14811411.png"/>

---

## More Information

- [High level - important paths/structure](/Repositories/Solution%20details%20-%20ETL_process%20tool/High%20level%20-%20important%20paths_structure)
- [ETL_infra.pptx (external slide deck)](https://medial.sharepoint.com/:p:/r/sites/algoteam/Shared%20Documents/General/genericETL/ETL_infra.pptx?d=wd53c98071ab841049d0472b1178fcb6c&csf=1&web=1&e=yREHdL)

