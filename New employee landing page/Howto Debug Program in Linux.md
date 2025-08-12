# Howto Debug Program in Linux

## Step 1 - compile your program with debug symbols "-g" flag
In order to debug program properly, you need to compile the program with debug symbols.
to do that you can use "smake_dbg" instead of "smake_rel" and the new exe will be saved under Linux/Debug.
If the debug mode is very slow you can directly edit CMakeList.txt and add "-g" flag to the CXX_FLAGS so it will compile with optimizations as in release but you can still debug it

## Step 2 - open debugger 
After the compilation has been finished. run

```
gdb EXE_PATH
```

or better tool (wrapper of gdb) with "gui":

```bash
cgdb EXE_PATH
```

in order to jump between code and command line in the gui - use ESC key to focus on code window (you can than scroll up and down) and "i"  to return the command prompt

## Step 3 - define breakpoints and usefull debug stuff:
Some usefull commands used to debug (you may shortend the commands, for example instead of "print" you may write just "p" and "c" instead of "continue").
remember you have history for your commands even after you close the debugger, so using arrows UP, arrows DOWN to visit history may be usefull.

- "catch th" - sets breakpoint when first exception is thrown
- "b FILE_NAME.cpp:LINE_NUMBER" - sets breakpoint in line with file. for example: "b MedModel.cpp:100" will set breakpoint at line 100 in MedModel.cpp.
    - hitting just "b LINENUM" will set breakpoint in line of current file(of stach trace)
    - Conditional breakpoint - you may specify "if CONDITION" in the end of the command to set conditional breakpoint. example: "b MedModel.cpp:100 if pid==5000001"
- "i b" - prints all breakpoints you have
- "d #NUM_BREAKPOINT" - deletes breakpoint by number, without number will delete all
- "bt" - prints backtrace of your program to see all program call. example:
```
bt
#0  medial::io::ProgramArgs_base::parse_parameters (this=this@entry=0x7fffffffd400, argc=argc@entry=1, argv=argv@entry=0x7fffffffd888) at /nas1/UsersData/alon/MR/Libs/Internal/MedUtils/MedUtils/MedUtils.cpp:
360
#1  0x00000000004db6d4 in main (argc=1, argv=0x7fffffffd888) at /nas1/UsersData/alon/MR/Tools/Flow/Flow/Flow.cpp:396
```
- "u" - go up in the stacktrace (who called the function), "d" - do down in the stacktrace (the function the current function called). "sel #NUM" - jump to current NUM stack in backtrace. for example "sel 1" will jump to first item in stacktrace
- "i th" - info threads prints inforamtion about threads. example:
```
i thr
  Id   Target Id         Frame
* 1    Thread 0x7ffff7fcb000 (LWP 14541) "Flow" main (argc=1, argv=0x7fffffffd888) at /nas1/UsersData/alon/MR/Tools/Flow/Flow/Flow.cpp:395
```
- "thr #THREAD_NUM" - go to different thread for debugging different stack trace in other thread
- "r PROGRAM_ARGS" - to start running the program. **you may start the program again at anytime.**
- "i args" - prints function arguments
- "i locals" - prints current function scope with all variables
- "p VAR_NAME" - prints variable value. example:
```
p argv[0]
$2 = 0x7fffffffdc1e "/server/Linux/alon/bins/Flow"
```
- "n" - next step advance program by 1 command
- "s" - step into - advance program by 1 command but step into if calling new function
- "c" - continue program run
- "q" - to quit debugger
- stop jump between threads when debugging multiple threads program - "set scheduler-locking on"

Special prints of STL library:

to access vector (we have old debugger so we can't just access it with []). If we have for example "vector<T> vec" variable, to access i index we should use "vec._M_impl._M_start[i]" to access this position

## Bonus Section

Linux creates crash dump for crashed programs (configuration of which program to run when program crashes can be found here: /proc/sys/kernel/core_pattern). currently uses with abrt tool.
the dumps are located in different places (depend on the node, we have for some reason different configuration path for dumps in each node - no good reason).
The dumps are deleted when new crash dump is created and when we reach the limit quota for dumps, so don't worry, it won't fill up all our storage space.
there is command "show_crashes.sh" in BASH_SCRIPTS - that locate those dump location in the current node.
to open a crash dump, see backtrace and print variables in the stack use gdb/cgdb to open the dump:

```bash
sudo cgdb CRASHED_PROGRAM_BIN_PATH CRASH_DUMP_PATH
# example:
# $> show_crashes.sh
# /home/tmp/abrt/ccpp-2019-02-21-09:54:17-13058/coredump  /server/UsersData/alon/MR/Projects/Shared/But_Why/Linux/Release/TryExplain --base_config /server/Work/Users/alon/But_Why/configs/explain_base.cfg
# $> sudo cgdb /server/UsersData/alon/MR/Projects/Shared/But_Why/Linux/Release/TryExplain /home/tmp/abrt/ccpp-2019-02-21-09:54:17-13058/coredump
```

## Change path to different source code folder
For example:
```
set substitute-path /home/alon-internal/MR_ROOT /nas1/UsersData/Alon/MR
```

## Profiler
how to debug speed.
compile program with -pg flags. g adds debug symbols and p adds gmon.out output for th profiler.
after program ends gmon.out output will apear in your current directory.
run :
```bash
gprof PATH_TO_BIN_APP PATH_TO_GMON.OUT | less
```

set substitute-path /home/foo /tmp/debug/home/foo 

