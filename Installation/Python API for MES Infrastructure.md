
## Python API for MES Infrastructure

### Overview

This is a Python API wrapper for the MES Infrastructure, allowing you to interact with MES models from Python code.
Train and manipulate new models.

The simplest way to install our package is with this command (Requires Python >=3.10 and linux, there is source code package for windows and older python versinos):
```bash
pip install medpython
```

If you need to build from source, follow the instructions below.

### Installation Steps

1. Install required system libraries:
   ```bash
   sudo apt install python3-dev swig -y
   ```
2. [Compile the Boost library](index.md#compiling-boost-from-source) from source.
3. Edit `Internal/MedPyExport/generate_binding/CMakeLists.txt` and add/edit line:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   Set this path to your Boost build directory (`WORK_BUILD_FOLDER` from step 2). Make sure the compiled libraries are in `/libs` and headers in `/include`.
   Alternatively you can just set your environment variable `BOOST_ROOT` to reference the Boost build directory.
   To use the **system Boost libraries**, be aware that they were **not compiled** with the `-fPIC` flag. This will cause the build to fail when linking against static objects. **To compile against shared Boost libraries**: Set `export BOOST_DISABLE_STATIC=1` before running the build script. **A critical side effect**: The resulting library will only work on your local machine because it will expect the Boost shared libraries to be present at runtime. It **cannot be deployed** to other systems.
4. Ensure NumPy is installed:
   ```bash
   python -m pip install numpy
   ```
   > This API supports both NumPy 1.x and 2.x. For maximum compatibility, compile with NumPy 2.x (works for clients with either version). Compiling with NumPy 1.x will **not** work for clients using 2.x.
5. Build the Python API:
   ```bash
   Internal/MedPyExport/generate_binding/make-simple.sh
   ```
6. Make the library accessible to your python by adding it to `PYTHONPATH` variable: 
   ```bash
   export PYTHONPATH=${MR_LIBS}/Internal/MedPyExport/generate_binding/Release/medial-python${PY_VERSION}
   ```
   Change MR_LIBS to your cloned path of MR_LIBS and ${PY_VERSION} to your python version, eg. 312 for python 3.12.

A full docker image for compilation steps can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [04.medpython](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/04.medpython) A build with the python. Please edit, install your python version in the build. This will use the python 3.10 that was shipped with ubuntu 22.04. If you need a different version, please install it inside the docker before executing the setup script