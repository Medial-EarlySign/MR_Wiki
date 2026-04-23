# Custom AlgoMarker Development

> [!NOTE]  
> In most use cases (all until now), you won't need to write a custom AlgoMarker from scratch. Setting `TYPE = "MEDIAL_INFRA"` in your `.amconfig` and using our existing implementations supports virtually everything you need. You can safely skip this if you're not extending core infrastructure logic.

## How to write a new Custom AlgoMarker

The AlgoMarker base class is `AlgoMarker.h`, found within the AlgoMarker lib in the medial earlysign library git repository [medpython](https://github.com/Medial-EarlySign/medpython/blob/main/Internal/AlgoMarker/AlgoMarker/AlgoMarker.h). To start working, pull it from Git first.

In order to write a new custom AlgoMarker, follow these steps:

1. Write a new class that inherits from `AlgoMarker` (or one of its derived classes). You must implement the following virtual functions:
    *   `virtual int Load(const char *config_f)`: Accepts a config file (or `NULL`) and initializes the AlgoMarker into a working state.
    *   `virtual int Unload()`: Releases all allocated memory and cleans up.
    *   `virtual int AddData(int patient_id, const char *signalName, int TimeStamps_len, long long* TimeStamps, int Values_len, float* Values)`: Adds data sequentially. Data is loaded per PID and specific signalName, followed by the arrays for time/value channels. This is **deprecated** API call.
    *   `virtual int ClearData()`: Clears all currently loaded data in the AlgoMarker.
    *   `virtual int Calculate(AMRequest *request, AMResponses *responses)`: The major API function. Once loaded and populated with data, this routine parses requests and generates responses. This is **deprecated** API call.
    *   `virtual int AddData(int patient_id, const char *signalName, int TimeStamps_len, long long* TimeStamps, int Values_len, float* Values)`: Adds data sequentially. Data is loaded per PID and specific signalName, followed by the arrays for time/value channels.
    *   `virtual int rec_AddDataByType(int DataType, const char *data, vector<string> &messages)`: Adds data from JSON format. New API, but it is recommanded to pass the data directly in `CalculateByType`
    *   `virtual int CalculateByType(int CalculateType, char *request, char **response)`: The major API function. Once loaded and populated with data, this routine parses requests and generates responses from JSON. This is the newer API. This can also load that data within the request.

2. Register the new type for your class in the `AlgoMarkerType` enum.
3. Update the `AlgoMarker::make_algomarker` routine to officially support your new class.
4. Compile your changes! There is NO NEED to touch any of the other API routines – they all rely internally on your implementation of the 5 virtual routines listed in Step 1.

## Compile the AlgoMarker shared library

For a custom or standard setup, follow the [AlgoMarker Library Setup](../../Installation/AlgoMarker_Library.md) to build the `libdyn_AlgoMarker.so` library. 
Once compiled, copy the resulting library into the `lib/` folder of your deployment directory.
