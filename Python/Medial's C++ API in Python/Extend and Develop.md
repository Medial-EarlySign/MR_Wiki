# Extending and Developing the Medial C++ API for Python

This document outlines the low-level C++ details required to further develop the Python bindings for our API.

## Objectives

The goals are to:

1. Use our API from Python.
2. Employ Python as a "Glue Language".
3. Enable prototyping, exploration, and discovery in Python.
4. Ensure interoperability with other frameworks.
5. Minimize maintenance overhead when updating code.

## Implementation Approach

For maintainability, **SWIG** is chosen as the binding solution. Other options considered:

- **Cython**: Adds another language to the process.
- **Boost::python**: Limited support/resources; requires special definitions for each exported member.
- **ctypes**: Direct C calls, but parameter definitions are error-prone and may lack binary compatibility across platforms.

**Why SWIG?**

- Mature project with extensive resources. TensorFlow uses SWIG for example.
- Handles memory and ownership complexities.
- Good NumPy support.

### Our Implementation: "MedPyExport"

- Located in `$MR_ROOT/Libs/Internal/MedPyExport`.
- Wraps classes and exports only necessary functions for Python.
- Minimal learning curve for contributors familiar with C++.
- SWIG interface files (`.i`) are auto-generated during build.

#### Notes & Pitfalls

- Always use `std::vector` for vectors.
- Restart Jupyter Notebook after adding new functions/classes to reload wrappers.
- Use distinct names for NumPy parameters of different types.
- Method overloading is not supported (may be possible to implement).
- Avoid "big-data" loops; use NumPy/Pandas for vectorized operations.
- Build system is separate from the main CMake files.
- No direct Pandas DataFrame conversion yet.
- SWIG scans only simple C++ headers; keep implementation in `.cpp` files.
- Compilation works on both Windows and Linux (tested execution on Linux/Jupyter).

## Build System

- Targeted for Linux machines
- Windows compilation works but does not produce a Python-loadable binary.
- Uses a specialized CMake file for SWIG integration.

## Directory Structure

Located in `$MR_ROOT/Libs/Internal/MedPyExport`:

- `MedPyExport`: Source files.
- `generate_binding`: CMake and binding generation files.
  - `MedPython`: SWIG interface files.
    - `scripts`: Helper scripts for compilation.

## Key Files

- `make.sh`: Bash script to start CMake build.
- `MedPython/MedPython.i`: Main SWIG interface.
- `MedPython/medial-numpy.i`: NumPy SWIG interface.
- `MedPython/MedPython.h`: Entry point for headers scanned by SWIG.
- `MedPython/MedPython.c`: Entry point for C files scanned by SWIG.
- `MedPython/pythoncode.i`: Python code for the binding.
- `MedPython/scripts/make_apply.py`: Script to generate NumPy apply directives.
- `MedPython/apply_directives.i`: Auto-generated SWIG directives.

## Extending the Code

### Example: Exporting a Class

```c++
// .h file for the class 'PidRepository'
#include "MedPyCommon.h"
class MedPidRepository;
class MPPidRepository {
public:
    MedPidRepository* o;
    // ...
};
```

- Include `MedPyCommon.h` for utilities/macros.
- Exported class names start with `MP` to avoid conflicts.
- Use a pointer to the wrapped object.
- Keep headers simple for SWIG; implementation in `.cpp` files.

Add all exported headers to `MedPyExport.h`:

```c++
#ifndef __MED_PY_EXPORT_H
#define __MED_PY_EXPORT_H
#include "MedPyExportExample.h"
#include "MPPidRepository.h"
#include "MPDictionary.h"
// ...
#endif
```

**Python Usage:**

```python
import medpython as med
rep = med.PidRepository()
```

### Adding a New Class

```c++
class MPPidRepository {
public:
    MedPidRepository* o;
    MPPidRepository();
    ~MPPidRepository();
    int read_all(const string &conf_fname);
    string dict_name(int section_id, int id);
    std::vector<bool> dict_prep_sets_lookup_table(int section_id, const std::vector<std::string> &set_names);
    // ...
};
```

- Basic types are mapped automatically.
- Use `std::vector` for vectors.

**Implementation Example:**

```c++
#include "MPPidRepository.h"
#include "InfraMed/InfraMed/MedPidRepository.h"
MPPidRepository::MPPidRepository() : o(new MedPidRepository()) {}
MPPidRepository::~MPPidRepository() { delete o; }
int MPPidRepository::read_all(const std::string &conf_fname) { return o->read_all(conf_fname); }
string MPPidRepository::dict_name(int section_id, int id) { return o->dict.name(section_id, id); }
```

### Properties

Implement getter/setter methods with `MEDPY_GET_` and `MEDPY_SET_` prefixes:

```c++
class MPSamples {
    int MEDPY_GET_time_unit();
    void MEDPY_SET_time_unit(int new_time_unit);
};
```

**Python Usage:**

```python
>>> s = med.Samples()
>>> s.time_unit
1
```

- Omit the setter for read-only properties.

### Static Const Variables

Mapped to class variables in Python:

```c++
class MPTime {
public:
    static const int Undefined;
    static const int Date;
    static const int Years;
};
```

**Implementation:**

```c++
const int MPTime::Undefined = MedTime::Undefined;
const int MPTime::Date = MedTime::Date;
```

**Python Usage:**

```python
print(med.Time.Date)
```

### Iterators

**Array Iterator Example:**

```c++
class MPSigVectorAdaptor {
public:
    int __len__();
    MPSig __getitem__(int i);
};
```

- Class name ends with `VectorAdaptor`.
- Implements `__len__` and `__getitem__`.

**Map Iterator Example:**

```c++
class MPStringFeatureAttrMapAdaptor {
    std::map<std::string, FeatureAttr>* o;
public:
    int __len__();
    MPFeatureAttr __getitem__(std::string key);
    void __setitem__(std::string key, MPFeatureAttr& val);
    std::vector<std::string> keys();
};
```

- Class name ends with `MapAdaptor`.
- Implements `__len__`, `__getitem__`, and optionally `__setitem__`, etc.

### NumPy Arrays

**Input Arrays:**

```c++
class MPPidRepository {
    int read_all(string conf_fname, MEDPY_NP_INPUT(int* pids_to_take, int num_pids_to_take));
}
```

**In-place Arrays:**

```c++
void MedPyExportExample::numpy_vec_in_out(MEDPY_NP_INPLACE(double* vec, int m));
```

**Output Arrays:**

```c++
class MPFeatures {
    void MEDPY_GET_weights(MEDPY_NP_OUTPUT(float** float_out_buf, int* float_out_buf_len));
};
```

**Variant Output Example:**

```c++
void getitem(string key, MEDPY_NP_VARIANT_OUTPUT(void** var_arr, int* var_arr_sz, int* var_arr_type)) {
    // Implementation sets var_arr, var_arr_sz, var_arr_type based on key
    *var_arr_sz = 0;
    if (key == "i")
    {
        *var_arr = (void*)malloc(sizeof(int) * 10);
        *var_arr_sz = 10;
        *var_arr_type = (int)MED_NPY_TYPES::NPY_INT;
        for (int i = 0; i < 10; i++)
            ((*(int**)var_arr))[i] = i * 5;
    }
    else if (key == "d")
    {
        *var_arr = (void*)malloc(sizeof(double) * 20);
        *var_arr_sz = 20;
        *var_arr_type = (int)MED_NPY_TYPES::NPY_DOUBLE;
        for (int i = 0; i < 20; i++)
            ((*(double**)var_arr))[i] = i * 2.5;
    }
    else if (key == "f")
    {
        *var_arr = (void*)malloc(sizeof(float) * 15);
        *var_arr_sz = 15;
        *var_arr_type = (int)MED_NPY_TYPES::NPY_FLOAT;
        for (int i = 0; i < 15; i++)
            ((*(float**)var_arr))[i] = i * 0.33333f;
    }
    else if (key == "n")
    {
        *var_arr = nullptr;
    }
}
```

**Supported NumPy Types:**

```c++
NPY_BOOL, NPY_BYTE, NPY_UBYTE, NPY_SHORT, NPY_USHORT, NPY_INT, NPY_UINT,
NPY_LONG, NPY_ULONG, NPY_LONGLONG, NPY_ULONGLONG, NPY_FLOAT, NPY_DOUBLE,
NPY_LONGDOUBLE, NPY_CFLOAT, NPY_CDOUBLE, NPY_CLONGDOUBLE, NPY_OBJECT,
NPY_STRING, NPY_UNICODE, NPY_VOID, NPY_DATETIME, NPY_TIMEDELTA, NPY_HALF,
NPY_NTYPES, NPY_NOTYPE, NPY_CHAR, NPY_USERDEF, NPY_NTYPES_ABI_COMPATIBLE
```

## Helper Functions & Macros

- **Docstrings:**  
  `MEDPY_DOC(function_or_class_name, docstring)`
- **Ignore for SWIG:**  
  `MEDPY_IGNORE(...)` or `#ifdef SWIG ... #endif`
- **Buffer to Vector:**  
  `buf_to_vector(int_in_buf, int_in_buf_len, idx);`
- **Vector to Buffer:**  
  `vector_to_buf(o->weights, float_out_buf, float_out_buf_len);`

## Installation

Each user compiles their own version.  
[See Build the python extention](Build%20the%20python%20extention)


