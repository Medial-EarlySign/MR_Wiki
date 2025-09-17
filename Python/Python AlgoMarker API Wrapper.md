# Python AlgoMarker API Wrapper

This project provides a Python wrapper for the AlgoMarker C library (`libdyn_AlgoMarker.so`). The wrapper allows you to interact with AlgoMarker using Python.

## Location

You can find the Python library and a tool for querying AlgoMarkers in the [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) at this folder `$MR_Tools/AlgoMarker_python_API`

## Files

- **AlgoMarker.py**: Main Python wrapper for the C library. The wrapper will use the new JSON API if available, or fall back to the older API for compatibility.
- **test_algomarker_lib.py**: Utility tool that uses `AlgoMarker.py` to query AlgoMarker.
- **AlgoMarker_minimal.py**: Minimal version of the wrapper with fewer functions.
- **simple_app_example.py**: Example app demonstrating usage of the minimal wrapper.

## Example Usage

Run the utility tool with:

```bash
python $MR_ROOT/Tools/AlgoMarker_python_API/test_algomarker_lib.py \
  --amconfig /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig \
  --output /tmp/results.txt \
  --add_data_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/data.single.json \
  --request_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.single.json \
  --amlib /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lib/libdyn_AlgoMarker.so
```

- `--amlib` (optional): Specify a custom library path.
- If your request JSON includes `"data"`, you can run:

```bash
python $MR_ROOT/Tools/AlgoMarker_python_API/test_algomarker_lib.py \
  --amconfig /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig \
  --output /tmp/results.txt \
  --request_json_path /nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.full.json
```

## Simple Usage Example

```python
from AlgoMarker_minimal import AlgoMarker
import json

ALGOMARKER_PATH = '/nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/lungflag.amconfig'
REQUEST_JSON = '/nas1/Products/LungCancer/QA_Versions/LungFlag3.NEW.2023-07-26.With_ButWhy/examples/req.full.json'

def read_text_file(path):
    with open(path, 'r') as fr:
        return fr.read()

with AlgoMarker(ALGOMARKER_PATH) as algomarker:
    discovery_json = algomarker.discovery()
    print('$> discovery - first 100 characters:')
    print(json.dumps(discovery_json, indent=True)[:100])
    print('$> calculate - first 200 characters:')
    resp = algomarker.calculate(read_text_file(REQUEST_JSON))
    print(json.dumps(resp, indent=True)[:200])

print('All Done')
```

## Running as a FastAPI Server

You can also run the wrapper as a FastAPI server.
This will wrapper `AlgoMarker.py`
You will need to setup fastapi package with:
```bash
python -m pip install fastapi
```

To configure, edit [`run_server.sh`](https://github.com/Medial-EarlySign/MR_Tools/blob/main/AlgoMarker_python_API/run_server.sh):

- Set `AM_CONFIG` to the path of your AlgoMarker `.amconfig` file.
- Set `AM_LIB` to the path of your compiled library (default is `/lib/libdyn_AlgoMarker.so` in the same directory as the amconfig file).

After editing, you can run the script.