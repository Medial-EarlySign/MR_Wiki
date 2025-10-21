
## Python API for MES Infrastructure

### Overview

This is a Python API wrapper for the MES Infrastructure, allowing you to interact with MES models from Python code.
Train and manipulate new models.

A prebuilt release is available on the [Release page](https://github.com/Medial-EarlySign/MR_LIBS/releases/tag/V1.0). The release is built with glibc 2.39 and works out of the box on systems with **glibc ≥ 2.39** (such as **Ubuntu 24.04**). If you need to build from source, follow the steps below.

### Installation Steps

1. Install required system libraries:
   ```bash
   sudo apt install python3-dev swig -y
   ```
2. [Compile the Boost library](index.md#compiling-boost-from-source) from source.
3. Edit `Internal/MedPyExport/generate_binding/CMakeLists.txt` and add:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   Set this path to your Boost build directory (`WORK_BUILD_FOLDER` from step 2). Make sure the compiled libraries are in `/libs` and headers in `/include`.
4. Ensure NumPy is installed:
   ```bash
   python -m pip install numpy
   ```
   > This API supports both NumPy 1.x and 2.x. For maximum compatibility, compile with NumPy 2.x (works for clients with either version). Compiling with NumPy 1.x will **not** work for clients using 2.x.
5. Build the Python API:
   ```bash
   Internal/MedPyExport/generate_binding/make-simple.sh
   ```

A full docker image for compilation can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [04.medpython](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/04.medpython) A build with the python. Please edit, install your python version in the build. This will use the python 3.10 that was shipped with ubuntu 22.04. If you need a different version, please install it inside the docker before executing the setup script