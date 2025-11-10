## Python Wrapper

1. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   ```
2. Edit `AlgoMarker_python_API/run_server.sh` and update the following:

   - `AM_CONFIG`: Path to the AlgoMarker configuration file.
   - `AM_LIB`: Path to the AlgoMarker shared library. Refer to [AlgoMarker Library](../AlgoMarker_Library.md) for compilation steps.
   - If using the old ColonFlag, follow the steps in the ColonFlag setup page to compile the ICU library. Add the ICU library path to `LD_LIBRARY_PATH` in the script before calling `uvicorn`.
3. Make sure you have all python dependencies installed (The AlgoMarker.py itself has no dependencies if you want to use it directly without FastAPI):
   ```bash
   python -m pip install fastapi
   ```
4. Run the Server `AlgoMarker_python_API/run_server.sh`

For more details follow: [Python AlgoMarker API Wrapper](../../Medial%20Tools/Python/Python%20AlgoMarker%20API%20Wrapper.md)