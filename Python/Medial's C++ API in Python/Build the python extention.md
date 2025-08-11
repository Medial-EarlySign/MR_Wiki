# Building the Python Extension

To build the Medial C++ API Python extension:

```bash
# Activate the correct Python environment
source /nas1/Work/python-env/python312/bin/activate

# Navigate to the binding directory
cd $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/

# Build the extension
./make-simple.sh

# After compilation, the .so file will be located at:
# $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/medial-python312

# Add this path to PYTHONPATH (or your .bashrc):
export PYTHONPATH=$MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/medial-python312:$PYTHONPATH
```

> **Note:**  
> Ensure `$MR_ROOT` points to the directory where you cloned [MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs).

---

## Known Issues

If you encounter errors like the following after upgrading from CentOS to Ubuntu:

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

This is likely due to an outdated `CMakeCache.txt` file containing old SWIG settings.  
To resolve this, delete the `CMakeCache.txt` file using the following command:

```bash
rm $MR_ROOT/Libs/Internal/MedPyExport/generate_binding/CMakeBuild/Linux/Release/CMakeCache.txt
```
