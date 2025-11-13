# 📄 ETL Workflow: The Recommended Tool

Using our ETL tool streamlines data loading by providing a standardized, robust, and reproducible process. 
While manual loading file creation is possible, our tool is highly recommended for its numerous benefits:

  * **Validation and Error Reporting:** The tool performs extensive checks to ensure correct data format, proper sorting, and valid lab values. It provides clear, informative error messages that help you quickly fix issues, saving significant time during the loading process.

  * **Automated Configuration:** It eliminates the need for manual configuration by automatically generating all necessary files for the final loading process. This includes:

      * **[Signals Config](../../Infrastructure%20Library/DataRepository/Repository%20Signals%20file%20format.md)** Defines signal types and units, allowing you to easily add new signals or override existing ones.
      * **[Dictionary Files](../../Infrastructure%20Library/00.InfraMed%20Library%20page/MedDictionary.md)** Automatically creates conversion dictionaries for all categorical signals (e.g., converting strings to numerical values). It can even pull hierarchical data from known ontologies, such as ICD-10 codes, when a specific prefix is used.
      * **[Conversion Config](../../Infrastructure%20Library/DataRepository/Load%20new%20repository.md)** A central configuration file that references all necessary dictionaries, signals, and data files for the load. Will be used by `Flow` app to convert those raw data files into InfraMed Binary format.
      * **[Loading Script](../../Infrastructure%20Library/DataRepository/Load%20new%20repository.md#step-3-load-the-repository)** Generates a final script with a `Flow` to run the entire loading process in one go.

  * **Efficient Batch Processing:** The tool supports batch processing, which is crucial for handling large datasets efficiently and managing memory usage. If a loading process fails, it can resume from the last successful step, preventing the need to restart from the beginning.

  * **Comprehensive Logging:** The tool logs all processing steps, test results, and creates distribution graphs for all signals, providing a clear overview of the data and the loading process.

  * **Code Reusability:** It reuses common data elements and testing procedures, drastically reducing the amount of code you need to write. Our scripts are typically **3-4 times shorter** than older, manual ETL scripts.

[ETL_infra.pptx (slide deck)](../../../SharePoint_Documents/General/genericETL/ETL_infra.pptx)

The code for this infrastructure was written with less strict standards as it is not part of our main production environment. While using the infrastructure is designed to be comfortable, modifying it may be challenging due to this less rigorous policy. Bugs may also be present.

-----

## Best Practices

**Keep it Simple**: Load signals with minimal preprocessing. Handle outliers and clean data within the model itself, not during the ETL stage. 
This approach simplifies implementation, reduces ETL errors, and results in a more robust model. 
Future implementations will be easier with a straightforward ETL process. The only thing to take care of in the ETL is formating and right units for labs - that's it.

-----

## 🚀 Getting Started

The first step is to setup the ETL infrastructure.
Follow the detailed instructions in the [Setup](00.Setup) documentation to begin.
