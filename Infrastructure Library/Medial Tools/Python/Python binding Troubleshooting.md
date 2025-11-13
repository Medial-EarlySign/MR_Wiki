# Python Binding Troubleshooting

## Problem 1: `"import med"` does not work

### Possible Cause: MedPython is not in path

Please make sure and print our PYTHONPATH environment variable:
```bash
echo $PYTHONPATH
```
and make sure it points out to a folder that contains `med.py` file. If not, please follow [Setup](index.md#setup)

## Problem 2: MedPython fails to compile

If you encounter errors like the following:

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
To resolve this, delete the `CMakeCache.txt` file using the following command (Change MR_LIBS to the folder you clones MR_LIBS into):

```bash
rm $MR_LIBS/Internal/MedPyExport/generate_binding/CMakeBuild/Linux/Release/CMakeCache.txt
```

## Problem 3: stderr in Jupyter Notebooks

Some API messages are printed to stderr and may not appear in Jupyter notebooks.  
To display these messages, use the `cerr()` utility:

```python
med.cerr()
```