# Installation

## Overview

There are four components that can be installed. You may install all of them or just the ones you need, depending on your requirements.

### Preliminary Steps to Build the Tools

These are the preliminary installation steps required:

#### 1. Install Compiler and Build Tools (Ubuntu)
To install the essential compiler and build tools, run:

```bash
sudo apt install binutils gcc g++ cmake make -y
```

#### 2. Install OpenMP Support (Ubuntu)
To enable OpenMP (used for parallel processing), install the following package:

```bash
sudo apt install libgomp1 -y
```

> **_NOTE:_** This is required step.

#### 3. Install Boost Libraries (Ubuntu)
To install the required Boost components, on Ubuntu 24.04, use:

```bash
sudo apt install libboost-system1.83-dev libboost-filesystem1.83-dev libboost-regex1.83-dev libboost-program-options1.83-dev -y
```

> **Note**: On Ubuntu 22.04, Boost version 1.74 is available and is also compatible.

If you want to compile the **AlgoMarker library** or compile it against a different Boost library, please [download and compile Boost manually](https://www.boost.org/users/download/) and follow the [Boost Compilation Steps](#boost-compilation-steps). This project has been tested with Boost versions 1.67 through 1.85 and should work with other versions as well.

#### Boost Compilation Steps

Example installation steps for version 1.85.0:

```bash title="Boost Compilation"
# Ensure you have wget to download the file and bzip2 to extract the "bz2" file. Setup in Ubuntu:
sudo apt install bzip2 wget -y

# Download the Boost Library
wget https://archives.boost.io/release/1.85.0/source/boost_1_85_0.tar.bz2

# Extract
tar -xjf boost_1_85_0.tar.bz2
rm -f boost_1_85_0.tar.bz2

# Setup Boost Install directory to current directory
WORK_BUILD_FOLDER=$(realpath .)
cd boost_1_85_0

# Configure to current system
./bootstrap.sh 
./b2 --clean

# Generate static libs
./b2 cxxflags="-march=x86-64" link=static variant=release linkflags=-static-libstdc++ -j8 cxxflags="-fPIC" --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options --with-system --with-regex --with-filesystem

mkdir -p ${WORK_BUILD_FOLDER}/Boost/include

# Generate symbolic link to headers inside Boost/include path
ln -sf ${WORK_BUILD_FOLDER}/boost_1_85_0/boost  ${WORK_BUILD_FOLDER}/Boost/include

# Generate shared/dynamic libs for tools, not needed for AlgoMarker
./b2 cxxflags="-march=x86-64" link=shared variant=release linkflags=-static-libstdc++ -j8 cxxflags="-fPIC" --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options --with-system --with-regex --with-filesystem
```

### 1. AlgoMarker Library

#### Description
The AlgoMarker shared library is used for deploying the AlgoMarker model. This library works with your final binary model output to access the model, apply it, and retrieve results. It provides a C-level API.

The Git repository is available at [MR_LIBS Git Repository](https://github.com/Medial-EarlySign/MR_LIBS).

#### Installation
1. Clone the Git repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_LIBS.git
   ```
2. Compile the Boost library. Refer to [Install Boost Libraries](#boost-compilation-steps). You must compile the Boost library since the `-fPIC` flag is needed, and it is not included in Ubuntu packages.
3. Edit `Internal/AlgoMarker/CMakeLists.txt` to include the following line:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   This should point to your Boost compiled home directory (`WORK_BUILD_FOLDER`) from the compilation step. Ensure the compiled libraries are in `/libs` and the headers are in `/include`.
4. Execute:
   ```bash
   Internal/AlgoMarker/full_build.sh
   ```

### 2. AlgoMarker Wrapper

#### Description
The AlgoMarker Wrapper provides a REST API for the AlgoMarker C++ Library. There are two wrappers available:

1. **C++ Native Wrapper**: Minimal dependencies, very fast, and efficient. Uses Boost Beast. Can be installed in a minimal Ubuntu Chiselled Docker image with just glibc.
2. **Python Wrapper**: Built with FastAPI, more flexible for changes, and supports the old AlgoMarker API. It is slower and has more dependencies but is friendlier for testing.

#### Installation

**C++ Native Wrapper**:

1. [Set up Boost Libraries](#3-install-boost-libraries-ubuntu). No need to compile.
2. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   ```
3. If you compiled the Boost library, edit `AlgoMarker_python_API/ServerHandler/CMakeLists.txt` to include the following line:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   This should point to your Boost compiled home directory (`WORK_BUILD_FOLDER`) from the compilation step. Ensure the compiled libraries are in `/libs` and the headers are in `/include`.
4. Compile the wrapper:
   ```bash
   AlgoMarker_python_API/ServerHandler/compile.sh
   ```
5. Execute the server:
   ```bash
   AlgoMarker_python_API/ServerHandler/Linux/Release/AlgoMarker_Server --algomarker_path $AM_CONFIG --library_path $AM_LIB --port 1234
   ```

	* `AM_CONFIG`: Path to the AlgoMarker configuration file.
   * `AM_LIB`: Path to the AlgoMarker shared library. 
      Refer to [AlgoMarker Library](#1-algomarker-library) for compilation steps.


**Python Wrapper**:

1. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   ```
2. Edit `AlgoMarker_python_API/run_server.sh` and update the following:

   - `AM_CONFIG`: Path to the AlgoMarker configuration file.
   - `AM_LIB`: Path to the AlgoMarker shared library. Refer to [AlgoMarker Library](#1-algomarker-library) for compilation steps.
   - If using the old ColonFlag, follow the steps in the ColonFlag setup page to compile the ICU library. Add the ICU library path to `LD_LIBRARY_PATH` in the script before calling `uvicorn`.
3. Run the Server `AlgoMarker_python_API/run_server.sh`

### 3. MES Tools to Train and Test Models

#### Description
Executables for training and testing models, along with other tools developed by MES for command-line use.

#### Installation
1. [Set up Boost Libraries](#3-install-boost-libraries-ubuntu). No need to compile.
2. Clone the repositories:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   git clone git@github.com:Medial-EarlySign/MR_LIBS.git
   ```
3. Navigate to the `MR_Tools` directory:
   ```bash
   cd MR_Tools
   ```
4. Edit `All_Tools/CMakeLists.txt` to set `LIBS_PATH` to the MR_LIBS cloned directory. The default structure is:
   ```
   Root Directory
   ├── MR_LIBS
   └── MR_Tools
   ```
   With this structure, no edits are needed.
5. Execute:
   ```bash
   AllTools/full_build.sh
   ```

### 4. Python Wrapper/Python API for MES Infrastructure

#### Description
A Python API Wrapper for the MES Infrastructure.

#### Installation
1. Install the required libraries:
   ```bash
   sudo apt install python3-dev swig -y
   ```
2. [Compile the Boost library](#boost-compilation-steps).
3. Edit `Internal/MedPyExport/generate_binding/CMakeLists.txt` to include the following line:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   This should point to your Boost compiled home directory (`WORK_BUILD_FOLDER`) from the compilation step. Ensure the compiled libraries are in `/libs` and the headers are in `/include`.
4. Execute:
   ```bash
   Internal/MedPyExport/generate_binding/make-simple.sh
   ```

## Code to Load All Tools into the Environment

```bash title="Start-Up Script"
#!/bin/bash

# Path to Boost library
LD_PATH=${HOME}/Documents/MES/Boost/lib
# Path to Git Repo clones
MR_LIBS=${HOME}/Documents/MES/MR_LIBS
MR_TOOLS=${HOME}/Documents/MES/MR_Tools
MR_SCRIPTS=${HOME}/Documents/MES/MR_Scripts

export PATH=$PATH:${MR_TOOLS}/AllTools/Linux/Release:${MR_SCRIPTS}/Python-scripts:${MR_SCRIPTS}/Bash-Scripts:${MR_SCRIPTS}/Perl-scripts
if [ ! -z "$LD_LIBRARY_PATH" ]; then
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${LD_PATH}
else
	export LD_LIBRARY_PATH=${LD_PATH}
fi
export PYTHONPATH=${MR_LIBS}/Internal/MedPyExport/generate_binding/Release/medial-python312:${MR_TOOLS}/RepoLoadUtils/common
```

Please edit `LD_PATH`, `MR_LIBS`, `MR_TOOLS`, and `MR_SCRIPTS` paths as needed.



