# Repository Viewers

Repository viewers provide a simple graphical interface for viewing patient signals. The system uses a C++ backend server (built with Boost) and the plotly.js library for interactive charts, tables, heatmaps, and more.

## How It Works

- The viewer sends a request to the server.
- The server responds with an HTML page via POST.
- The page is rendered with all graphics.

## Compiling

- Compile AllTools with the `Tools/AllTools/full_build.sh` script.
- The main application is `SimpleHttpServer`, found under `Linux/Release` after building.

## SimpleHttpServer Parameters

- `rep`: Repository to use.
- `plotly_config`: Configuration file (see below); usually, the default is sufficient.
- `server_dir`: Directory for server files (default is usually fine).
- `address`: Server IP (use `ip addr show` to find yours.
- `port`: Server port (avoid 80, 8080, 7090, 8090, 7990; ensure your chosen port is free).

## Configuration File

- Example and definitions: `$MR_ROOT/Libs/Internal/MedPlotly/MedPlotly/BasicConfig.txt`
- Contains default parameters and panel definitions.
- Panels become plots and can contain multiple signals.

### Key Parameters

- `JSDIR`: Directory for JavaScript files.
- `JSFILES`: Main plotly.js file.
- `NULL_ZEROS`: If 1, skips zero values in plots (useful for outliers).
- `LOG_SCALE`: If 1, uses logarithmic axis scaling.
- `WIDTH`/`HEIGHT`: Default panel size.
- `BLOCK_MODE`: If 1 (recommended), arranges graphs in a line if space allows.
- `SIG <sig_name> <parameters>`: Override defaults for specific signals.
- `DRUG_GROUP`: Defines drug groups for the drugs heatmap (see config examples).
- `PANEL`: Defines a panel with name, title, signals, and optional size/params.
- `VIEW`: Lists default panels to show.
- `REP_PROCESSORS`: JSON file for MedModel to configure repository processors.

### Example Configurations

- `BasicConfig`: For THIN, AppleTree repositories.
- `MHSConfig`: For Maccabi, KP.
- `RambamConfig`: For Rambam repository.
- `MimicConfig`: For Mimic repository.

You can create or modify configs as needed. The MedPlotly library parses these files and generates plotly inputs based on panel definitions and user requests.

## Default Servers

- Default servers usually run on node-01. You can start your own in different node.
- If default servers are down, start your own or request a restart.

## Running the Viewers

- Script location: `$MR_ROOT/Projects/Scripts/Bash-Scripts/run_viewer.sh` (included in your PATH).
- To edit server/port list: `$MR_ROOT/Projects/Scripts/Python-scripts/viewers_config.py`

```bash
viewers start
# To stop all viewers:
viewers stop
```

- Viewers run detached from your SSH session (they continue if your session ends).
- No output is printed to your screen.
- Error logs: `/nas1/Work/CancerData/Repositories/viewers_log`

The script to launch servers and display the index page is at `$MR_ROOT/Projects/Scripts/Python-scripts/viewers_runner.py`. This file shows the latest commands for starting servers.

## Viewer Features

- Enter a PID number and press send.
- Mark a specific date (drawn as a vertical black line on graphs).
- Some viewers allow specifying a date range (useful for Rambam and Mimic3 viewers).
- Each graph is interactive (zoom, pan, hover, etc.).
- Select panels/signals from the list or add them in the signal charts box (space, semicolon, or newline separated).

This flexibility lets you view signals not included in the default



