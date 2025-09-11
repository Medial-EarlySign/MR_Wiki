## AlgoMarker Configuration Guide

A sample packaging script can be found in GastroFlag:  
[https://github.com/Medial-EarlySign/AM_LGI/blob/main/Extended_model/scripts/pack_algomarker.sh](https://github.com/Medial-EarlySign/AM_LGI/blob/main/Extended_model/scripts/pack_algomarker.sh)

The setup script defines variables for the model, repository, reference matrix, deployment path, and more.

### Typical Steps

1. **Model Adjustments (Optional but Recommended)**
    - Uses tools `Flow`, `adjust_model`, and `change_model` operations to modify the model as needed. For example:
        - `Flow --export_production_model`: Enables verbose outlier reporting (useful for production, but may slow down predictions and increase memory usage).
        - `adjust_model`: Perform operations such as adding virtual signals (e.g., "eGFR") or adding checks (e.g., ensuring a CBC exists on the prediction date and storing the result as an attribute for eligibility filtering).
        - `change_model`: Enable explainability output for AlgoMarker by setting `store_as_json=1`.
    - These steps are optional and depend on your production requirements. If you do not need outlier documentation or explainability, you may skip them.

2. **Copy Model Files**
    - Copy the binary model file to the AlgoMarker directory.
    - Document the original model path and its MD5 checksum (recommended).

3. **Build and Copy the Shared Library**
    - Build the `libdyn_AlgoMarker.so` shared library as described in [AlgoMarker Library Setup](../../New%20employee%20landing%20page/index.md#1-algomarker-library).
    - Copy the compiled library to the AlgoMarker folder under "lib" folder.

4. **Prepare the Repository Configuration**
    - Generate a repository config file containing only the required signals and dictionaries. This defines the signal names, types, and categorical mappings for AlgoMarker.
    - You can copy the config files from the repository used during model training, but it is recommended to clean them up and remove unused signals. A script is available to assist with this from GastroFlag.

5. **Create the AlgoMarker Configuration File (`amconfig`)**
    - See the [Configuration File section](../AlgoMarkers) for details and a full example.
    - Keep `TYPE` as `MEDIAL_INFRA`
    - `NAME` is free text to store name for AlgoMarker and will be returned in discovery call request.
    - The `FILTER` rows allow you to define eligibility rules and warnings. For testing, you may skip these filters.

    Example snippet:
    ```txt
    #################################################################################
    # MedialInfra AlgoMarker config example file
    #################################################################################
    TYPE	MEDIAL_INFRA
    NAME	PRE2D
    REPOSITORY	rep/pre2d.repository
    TIME_UNIT	Date
    MODEL	resources/pre2d.model
    # Eligibility filters and other settings follow...
    ```

    - Filters can enforce rules such as minimum/maximum number of results, allowed values, age ranges, dictionary validation, and outlier limits.
    - See the full example in [Eligibility rules configuration section](../AlgoMarkers)
    - `REPOSITORY` and `MODEL` refer to file paths: `REPOSITORY` is the path to the repository config file (used in Step 4), and `MODEL` is the path to the model binary (used in Step 2). 

      It's recommended to use relative paths and place both files in the same folder hierarchy for simplicity.

6. **Generate Explainability Config (Optional)**
    - If your model supports explainability, create a configuration file (e.g., `resources/explainer.cfg`) to control display settings for each group, such as which signals to show and how many values to fetch.

7. **Create Leaflet/Cutoff Threshold Table (Optional)**
    - Generate a cutoff threshold table config file (e.g., from `bootstrap_app` output) if you want to store thresholds in the AlgoMarker.

8. **Copy Test Script Template (Optional)**
    - Optionally, include a script template for testing AlgoMarker deployments.

