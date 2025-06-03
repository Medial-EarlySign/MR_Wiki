# Repository Viewers
The repository viewers allow for a simple graphical view of signals for a specific patient.
It is based on a backend server based on boost in c++, and the plotly.js package which has options for several nice graphs/charts/tables/heatmaps/etc...
In general the flow of things is a request from the viewer reaches the server and the resulting html page is returned by post, and then it is drawn with all graphics.
### Compiling 
Compile Tools/Tutorials , under linux. (Was not tested on windows... should proabably work with some small adjustments, need update 3 in order to compile it).
The app you need is SimpleHttpServer (you will find it under Linux/Release after compiling).
### SimpleHttpServer Parameters
The app has several parameters controlling the server:
- rep : the repository to use
- plotly_config : a configuration file, explained below, typically you'll just need to use the default one
- server_dir : the directory the server uses for its files. Again - typically can be left to the default (or redirected to the one on your git)
- address : the ip of the server you're running from (use ifconfig to find it if you do not know it. Currently is it 192.168.1.221-224 for nodes 01 to 04)
- port : the port for bringing up the server (choose a number that is NOT 80 , 8080, 7090, 8090, 7990 , and check before that there's no server listening on the port you choose on your node)
 
### Configuration file
See the basic config for an example and definitions at /nas1/UsersData/<your name>/MR/Libs/Internal/MedPlotly/MedPlotly/BasicConfig.txt
It contains some basic needed parameters and defaults, and also allows panel definitions.
A panel will eventually become a plot, it may contain one or more signals to plot.
Short explanations:
- JSDIR : the directory the server pulls javascript files from
- JSFILES : the basic plotly js file the server needs
- NULL_ZEROS : if 1 the default will be to skip 0 values for a signal when plotting it (this is since in many cases there are 0 outliers in the data , and it looks bad when making graphs)
- LOG_SCALE : if 1 scale the axis to log by default, usually looks better
- WIDTH : default width of a panel 
- HEIGHT : default height of a panel
- BLOCK_MODE : if 1 (recommended) will draw graphs in the same line if there's enough space.
- SIG : followed by <sig_name> <parameters> : allows chaning defaults for specific signals.
- DRUG_GROUP : currently tied uniquely to the Drug signal (if available. Works in THIN , Maccabi, KP ). Each line is followed by a name of a group, and then the sets that are included in it. (See examples in basic config files). These will be the groups shown on the drugs heatmap.
- PANEL definition : contains a name, a title, a list of signals to to draw, and one can also change size and params (otherwise defaults will be used). Each signal has also an implicit panel that is the signal name itself, drawing it, so these do not need to be defined.
- VIEW : list the deault panels to show
- REP_PROCESSORS - a json file to MedModel to configure rep_processors to process the repository (virtual signals, panel completers, cleaners...)
In /nas1/UsersData/<your name>/MR/Libs/Internal/MedPlotly/MedPlotly/ you'll find three initial configuration files :
- BasicConfig : works well with THIN, AppleTree repositories
- MHSConfig : for Maccabi, KP
- RambamConfig : for the Rambam repository
- MimicConfig : for the mimic repository
Of course you are invited to create your own configs and improve those that are given.
The code to parse and use these config files is in the MedPlotly library - which basically handles the creation of plotly inputs given the panels definitions and the panels requested by the user.
 
**Default Servers**
****
Typically we'll try to keep default servers running up on node-04 , so if you bring your own server up try to do it on nodes 01-03. These servers may be down ... if so bring up one on your own or report and ask for the servers to come up.
 
Link to all repository Viewers: ****
**To run the viewers:**
it's is locate in MR_SCRIPTS repository $MR_ROOT/Projects/Scripts/Bash-Scripts/run_viewer.sh (it's part of PATH environment variable).
To edit the list of servers\port please edit the file: $MR_ROOT/Projects/Scripts/Python-scripts/viewers_config.py 
```
viewers start
#To close All Viewers
#viewers stop
```
* It is detached from your SSH session - so if your putty crashes, the viewers still run. 
* No output is printed into your screen.
* Last errors are reported in here: /nas1/Work/CancerData/Repositories/viewers_log
 
The script to bring up the servers and show the "index" page can be found in here $MR_ROOT/Projects/Scripts/Python-scripts/viewers_runner.py 
In there you can see the latest command lines to bring up each of these servers and learn how to do it. Again - please do not being up servers on node-04 unless you are the one maintaining the default servers.
If all you need is one of the above repositories with the current viewers, the default servers on node-04 should be fine, and be able to easily serve the whole group.
### Viewers Features
The viewers are very basic and simple to use. Enter the pid number and press send.
More options:
You can mark a specific date (currently only dates supported, not full minutes) , that will be drawn on the graphs as well in a long vertical black line. It helps when one needs to see what happens around a specific date (say the outcome date).
In some of the viewers you can also give a range of dates to draw. This helps mainly in the Rambam and Mimic3 viewers which have short very dense episodes with sometimes years between them, and allows to zoom easily at once on all graphs.
Each graph is a plotly graph: you can zoom in, out, hover over points, moves axises , etc...
You can choose only the panels you want from the list and/or add signals and panels in signal charts box (space or semicolon or newline separated). This is very much needed if you want to see a signal that is not drawn in the default view or one of the panels you chose (there are many such signals).
 
 
 
