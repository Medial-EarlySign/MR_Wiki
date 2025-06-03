# Python binding Troubleshooting
## PROBLEM: "import med" didn't work
 
**Possible cause #1:** If it happened in commandline, You probably didn't use the right Python version.
**Solution:** In bash type the command:
```bash
source /opt/medial/python36/enable
```
and try again.
 
**Possible cause #2:** You didn't compile the binding at all or copiled it using the wrong Python headers.
**Solution: **Recompile the Python binding using the correct python headers and environment:
```bash
# You should probably pull git changes before executing the following steps to get the most recent version.
source /opt/medial/python36/enable
cd $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/
./make.sh
# After compilation, Your Python binding .so file should appear at: $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/medial-python36
# This location will be autmatically added to your python extension search path in the jupyterhub python3 instances and commandline python (/opt/media/python36)
```
**Possible cause #3:** You pulled the source and compiled the binding but the file system cache still sees the old no-working-build and the error message persists.
**Solution:** Execute **drop_cache.sh** and see that the output is 3, then try again
 
### Compiling and running on node-05
Node-05 is currently an exception since we have a cuda version tensorflow (and keras) there, based on python2.7 , the python we use is /use/bin/python .
In order to compile to the following steps in a node-05 window:
1. export PYTHON_INCLUDE_DIR=/usr/include/python2.7
2. export PYTHON_LIBRARY=/usr/lib64/[libpython2.7.so](http://libpython2.7.so)
3.  Not Need anymore
4. run make.sh from MR/Libs/Internal/MedPyExport/generate_binding
 
To use this compiled version use:
```python
#!/usr/bin/python
import sys
# of course change next dir to your named MR
sys.path.insert(0,'/nas1/UsersData/avi/MR/Libs/Internal/MedPyExport/generate_binding/Release/rh-python27')
import med
```
