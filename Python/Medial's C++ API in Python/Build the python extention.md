# Build the python extention
From anywhere in the shell:
```bash
build_py_wrapper.sh
```
 
## Known issues:
 
If you experience the following error (result of after update to Ubuntu from Centos):
```
[ 27%] Swig compile medpython.i for python
:1: Error: Unable to find 'swig.swg'
:3: Error: Unable to find 'python.swg'
/nas1/UsersData/git/MR/Libs/Internal/MedPyExport/generate_binding/MedPython/medpython.i:8: Error: Unable to find 'exception.i'
/nas1/UsersData/git/MR/Libs/Internal/MedPyExport/generate_binding/MedPython/medpython.i:9: Error: Unable to find 'typemaps.i'
/nas1/UsersData/git/MR/Libs/Internal/MedPyExport/generate_binding/MedPython/medpython.i:10: Error: Unable to find 'std_string.i'
/nas1/UsersData/git/MR/Libs/Internal/MedPyExport/generate_binding/MedPython/medpython.i:11: Error: Unable to find 'std_vector.i'
/nas1/UsersData/git/MR/Libs/Internal/MedPyExport/generate_binding/MedPython/medial-numpy.i:3295: Error: Unable to find 'std_complex.i'
```
Please erase CMakeCache.txt, it contains configuration/cache of older swig settings from centos and this file is not being recreated when rebuilding the python wrapper. 
Run this command:
 
```bash
rm $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/CMakeBuild/Linux/Release/CMakeCache.txt
```
 
## Compile your extension (OLD WAY):
 
```bash
# Make sure all dependent libs have makefiles - NOT NEEDED
# cd $MR_ROOT/Libs/Internal/MedPyExport && new_create_cmake_files.pl
cd $MR_ROOT/Libs/Internal/MedPyExport/generate_binding
# This will start compilation
./make-simple.sh
# Extension files are now at : $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/
```
