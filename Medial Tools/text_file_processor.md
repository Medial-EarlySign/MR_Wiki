# text_file_processor
A fast tool to process columnized text file - it's very similar to paste.pl but it's written in C++ (which makes it faster) and has more options.
 
**text_file_processor --help**
```bash
##     ## ######## ########  ####    ###    ##
###   ### ##       ##     ##  ##    ## ##   ##
#### #### ##       ##     ##  ##   ##   ##  ##
## ### ## ######   ##     ##  ##  ##     ## ##
##     ## ##       ##     ##  ##  ######### ##
##     ## ##       ##     ##  ##  ##     ## ##
##     ## ######## ########  #### ##     ## ########
Program General Options:
  --help                help & exit
  --h                   help & exit
  --base_config arg     config file with all arguments - in CMD we override
                        those settings
  --debug               set debuging verbose
Program Options:
  --input arg           the location to read input ("-" for stdin)
  --output arg          the location to write output file  ("-" for stdout)
  --delimeter arg (=    )  the input file delimeter
  --has_header arg (=1) True if the file has header
  --config_parse arg    the config command to parse line
```
 
 
**Example run**
```bash
./text_file_processor --input /server/Work/Users/Alon/Models/outputs/debug.txt --output - --config_parse="0;3;4;7;1;He;file:/server/Work/Users/Alon/Models/outputs/byears.thin2#0#0#1" > /tmp/debug
 
Read 10 keys for dictionary /server/Work/Users/Alon/Models/outputs/byears.thin2 in 0 seconds
Warning: has 4987 not found keys within 17792 rows.
Example:"19099934"
Done Processing 17794 lines in 0 seconds
```
in this example I have used truncated byears file with only 10 patients and thier byear. the program outputs that we have only 10 keys in the byears.thin2 and that for 4987 patients we haven't found a match with example for pid that we couldn't find a match to...
If everything is OK we won't see warnings
 
- the input and output may be "-" to use stdin/stdout.
- you have delimiter option to control input file delimeter (default is TAB)
the config_parse is consists of columns creation based on ";" between each column. you may use one of the tree options to create column:
- specify just a number - and it will copy the input column number
- specify a constant string - in the example "He" that will be filled as a column
- specify columns pasted from file. you need to start with "file:" specify the path to the file and specidy 3 list of numbers seperated by "#" (you may selected multiple columns for example "1,3" will use column 1 + 3). 
  - the first list of number is the columns in the specified file to join with.
  - the second list is the columns in the input to join with
  - the third list is the columns to select from the specified file to paste
 
