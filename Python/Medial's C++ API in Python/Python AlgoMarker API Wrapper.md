# Python AlgoMarker API Wrapper
We have created a python wrapper to the AlgoMarker C library - the "libdyn_AlgoMarker.so" that can use the AlgoMarker API to interact with AlgoMarker.
The python library and a tool to query AlgoMarkers using this library can be found in "tools" repository under $MR_ROOT/Tools/AlgoMarker_python_API
There are 2 files in this directory:
- AlgoMarker.py - which is the library wrapper for the C library in python
- test_algomarker_lib.py - A utility tool that uses this AlgoMarker,py library to query AlgoMarker
A Minimal version
- AlgoMarker_minimal.py - a shorter version of "AlgoMarker.py" with less function for minimal usage - might be shared with customer. 
- simple_app_example.py - a simple app that uses "AlgoMarker_minimal" (can also use AlgoMarker since it includes AlgoMarker_minimal)
Example command usage:
```bash
python $MR_ROOT/Tools/AlgoMarker_python_API/test_algomarker_lib.py --amconfig /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig --output /tmp/results.txt --add_data_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/data.single.json --request_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.single.json --amlib /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lib/libdyn_AlgoMarker.so
 
#Optional parameter --amlib - to load specific library from AlgoMarker. If not will use default library
#Optional request when "data" is inside request:
python $MR_ROOT/Tools/AlgoMarker_python_API/test_algomarker_lib.py --amconfig /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig --output /tmp/results.txt --request_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.full.json
```
 
Simple code of simple_app_example.py usage:
**Simple code usage**
```python
from AlgoMarker_minimal import AlgoMarker
import json
ALGOMARKER_PATH='/nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig'
REQUEST_JSON='/nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.full.json'
def read_text_file(p):
    fr=open(p, 'r')
    res=fr.read()
    fr.close()
    return res
with AlgoMarker(ALGOMARKER_PATH) as algomarker:
    discovery_json=algomarker.discovery()
    print('$> discovery - first 100 characters:')
    print(json.dumps(discovery_json, indent=True)[:100])
    print('$> calculate - first 200 characters:')
    resp=algomarker.calculate(read_text_file(REQUEST_JSON))
    print(json.dumps(resp, indent=True)[:200])
    
print('All Done')
```
