# Setup

Just install our MedPython package, it is now part of the PyPi package:
```
pip install medpython
```
or medpython-etl which is just the etl library.

* Code Repository - [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools). You might clone it and work directly from source code. The library code is under `RepoLoadUtils/common/ETL_Infra`. You will need: numpy pandas plotly

## Verify the Setup
To confirm everything is set up correctly, run the following command:

```bash
python -c 'import ETL_Infra'
```

## Next Steps

[Sphinx API Link](https://medial-earlysign.github.io/MR_Tools)

The first step in the ETL process is to create a module or script that fetches data in batches. This method is highly efficient and preferred over returning a single `DataFrame` from a simple function.

Follow the detailed instructions in the [Data Fetcher](../01.Data%20Fetching%20step) documentation to begin.