
# Installation Guide

## Introduction
The MES Infrastructure is a suite of tools and libraries designed for building, training, and deploying machine learning models, particularly in medical contexts.

This guide describes how to install and set up the MES Infrastructure and its various components. You can choose to install all or only the specific components you need, depending on your use case. These tools allow you to use [published models](../Models). For guidance on how to use our tools, please refer to the Tutorials section.

## Prebuilt Releases

For convenience, prebuilt packages of executables and Python wheels are available. Using these eliminates the need for manual compilation.

### How to Use Prebuilt Binaries

1.  **Download:** Obtain the appropriate prebuilt release package from the Release page.
2.  **Extract:** Unzip or untar the downloaded archive to a location on your system (e.g., `~/mes_binaries`).
3.  **Add to PATH (Optional but Recommended):** To easily run the executables from any directory, add the directory containing the binaries to your system's `PATH` environment variable.
    ```bash
    export PATH="/path/to/your/extracted/binaries:$PATH"
    ```
4.  **Set `LD_LIBRARY_PATH`:** The C++ executables, are dependent in Boost library. Set `LD_LIBRARY_PATH` to include the directory containing shared libraries (e.g., Boost). Refer to the Environment Setup Script for guidance.

A prebuilt package of executables is available for [direct download](https://github.com/Medial-EarlySign/medpython/releases/tag/V1.0.1). This eliminates the need for manual compilation. The binaries are built on **manylinux2014** and are compatible with any Linux distribution using **glibc ≥ 2.17** (Ubuntu >= 13.04, Centos>=7 or any other linux distro that has glibc>=2.17). You must also install [OpenMP support](#2-install-openmp-support-ubuntu). In Mac the prebuild is for macOS >= 14

You might also want to install our [PyPi python package](https://pypi.org/project/medpython/) for working with python.
```bash
pip install medpython
```
**Platform Support for MedPython** 

| Platform | x86_64 (Intel/AMD) | aarch64 (ARM / Apple Silicon) |
| :--- | :--- | :--- |
| **Linux (glibc)** | ✅ Pre-built (Py 3.10-3.14) | ✅ Pre-built (Py 3.12) |
| **Linux (Alpine/musl)**| 🛠️ Compile Required | 🛠️ Compile Required |
| **Windows** | ✅ Pre-built (Py 3.10-3.13) | 🛠️ Compile Required |
| **macOS** | 🛠️ Compile Required | ✅ Pre-built (Py 3.10-3.13) |

> **Note:** For any Compile Required or either not listed as Pre-built. Compliation is required.
> See the "Building the tools yourself" instructions below.

## Common Prerequisites

These prerequisites are generally required for both running prebuilt binaries and building from source.

### 1. General System Requirements

*   **Operating System:** Linux (Ubuntu 13.04+, CentOS 7+ recommended), macOS (14+ for prebuilt Python wheels).
*   **Memory:** 4GB RAM minimum, 16GB+ recommended for model training.
*   **Disk Space:** 10GB+ free space for source code, dependencies, and build artifacts.

### 2. Install OpenMP Support (Ubuntu)

OpenMP is required for parallel processing in many of the C++ components.

```bash
sudo apt install libgomp1 -y
```

> **Note:** This step is required even if you don't plan to compile the tools. It is required for runtime.
> Equivalent package exists in other linux distros, but here we will cover Ubuntu.

## Building the tools yourself

Before building the tools, complete the following steps:

### 1. Install Compiler and Build Tools (Ubuntu)

Install the required compiler and build tools if you want to build the software yourself:

```bash
sudo apt install binutils gcc g++ cmake make -y
```

### 2. Install Boost Libraries
Boost is a collection of C++ libraries. It is needed for the C++-based MES Tools.

> **Important Note:**
> *   For the Python API (`medpython`), Boost is handled automatically by the build process and does not require manual installation.
> *   For AlgoMarker Library, Boost is handled automatically by the build process and does not require manual installation.
> *   For AlgoMarker Wrapper, Boost is unneeded.
> *   For MES Tools, Boost is a core dependency.

#### When is Boost needed?

*   **MES Tools:** Required.
*   **AlgoMarker Library:** Handled automatically, manual installation not needed.
*   **Python API:** Handled automatically, manual installation not needed.

#### Which Boost version?

The MES Infrastructure is generally compatible with Boost versions 1.67 and newer.

#### How to install Boost:

**Option A: Install via Package Manager (Recommended for most users)**

This is the simplest method and often sufficient.

```bash
# For Ubuntu 22.04 (Boost 1.74)
# sudo apt install libboost-program-options1.74-dev  -y

# For Ubuntu 24.04 (Boost 1.83)
sudo apt install libboost-program-options1.83-dev -y
```

> **Note:** The exact package names might vary slightly depending on your Ubuntu version. Install the `dev` packages to get both libraries and headers.

**Option B: Compile Boost from Source (Advanced / Specific Requirements)**

This method is only necessary if:

*   Your system's package manager does not provide a compatible Boost version.
*   You need a specific, custom-built version of Boost.

For detailed instructions on compiling Boost from source, refer to the Advanced: Installation Script below.

If you compile Boost from source, remember to set the `BOOST_ROOT` environment variable to point to your compiled Boost installation directory (e.g., `/path/to/your/compiled/Boost`). This is crucial for the build system to find the correct Boost libraries and headers.

```bash
# Example if you compiled Boost to /home/user/my_builds/Boost
export BOOST_ROOT="/home/user/my_builds/Boost"
```

> **Important:** If you install Boost via a package manager, `BOOST_ROOT` is typically not needed as the system's CMake/pkg-config will find it automatically. Only set `BOOST_ROOT` if you compiled Boost manually.


**Installation Script**
You can [download Boost](https://www.boost.org/users/download/) and compile it manually. 
Example steps for version 1.90.0:

```bash title="Boost Compilation"
# Install tools for download and extraction
# sudo apt install bzip2 wget -y

# Download Boost
VERSION=1.90.0
VERSION_2=$(echo ${VERSION} | awk -F. '{print $1 "_" $2 "_" $3}')
wget https://archives.boost.io/release/${VERSION}/source/boost_${VERSION_2}.tar.bz2

# Extract files
tar -xjf boost_${VERSION_2}.tar.bz2
rm -f boost_${VERSION_2}.tar.bz2

# Set up Boost install directory
WORK_BUILD_FOLDER=$(realpath .)
cd boost_${VERSION_2}

# Configure and clean
./bootstrap.sh
./b2 --clean

# Build static libraries
./b2 cxxflags=-march=x86-64 cxxflags=-fPIC pch=off link=static variant=release -j8 --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options

mkdir -p ${WORK_BUILD_FOLDER}/Boost/include

# Link headers to Boost/include
ln -sf ${WORK_BUILD_FOLDER}/boost_${VERSION_2}/boost  ${WORK_BUILD_FOLDER}/Boost/include

# Build shared libraries (not needed for AlgoMarker, but needed for MES tools if you choose to compile)
./b2 cxxflags=-march=x86-64 cxxflags=-fPIC pch=off link=shared variant=release -j8 --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options
```

## Available Components

You can install any of the following four components:

1. [AlgoMarker Shared Library](AlgoMarker_Library.md): A shared Linux C library for accessing the AlgoMarker API and generating predictions/outputs from a model. Designed for **production use**, it supports only the essential "predict" and related APIs. Follow those steps only if you want to **productize** your model.
2. [AlgoMarker Wrapper](AlgoMarker%20Wrapper): A REST API wrapper for the AlgoMarker Shared Library. Follow those steps only if you want to **productize** your model.
3. [MES Tools to Train and Test Models](MES%20Tools%20to%20Train%20and%20Test%20Models.md): Command-line executables for training, testing, and manipulating models using the MR_LIBS infrastructure. Required for training new models. Alternatively, you can use the Python API.
4. [Python API for MES Infrastructure](Python%20API%20for%20MES%20Infrastructure.md): Python API, enabling model training, testing, and manipulation from Python. Some features may only be available via MES Tools or by [extending the Python API](../Infrastructure%20Library/Medial%20Tools/Python/Extend%20and%20Develop.md). Can be install via `pip install medpython`

## Environment Setup Script

After installing the required components, it is recommended to use the following script to configure your shell environment for all tools and scripts (This is only needed, if you are not using the python pypi package or if you want to use the executables):

```bash title="Start-Up Script"
#!/bin/bash
# Path to Boost Library (If you compiled the boost library)
BOOST_ROOT=${HOME}/Documents/MES/Boost
# Path to Git repository clones - here in the example, we clones all repositories under ${HOME}/Documents/MES
MR_LIBS=${HOME}/Documents/MES/MR_LIBS
MR_TOOLS=${HOME}/Documents/MES/MR_Tools

LD_PATH=${BOOST_ROOT}/lib
if [ ! -z "$LD_LIBRARY_PATH" ]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${LD_PATH}
else
    export LD_LIBRARY_PATH=${LD_PATH}
fi

export PATH=$PATH:${MR_TOOLS}/AllTools/Linux/Release:${MR_TOOLS}/Scripts/Python-scripts:${MR_TOOLS}/Scripts/Bash-Scripts:${MR_TOOLS}/Scripts/Perl-scripts
export AUTOTEST_LIB="${MR_TOOLS}/AutoValidation/kits"
# --- Python API Setup (if built from source) ---
PY_VERSION=$(python -c "import platform; print(''.join(platform.python_version().split('.')[:2]))")

export PYTHONPATH=${MR_LIBS}/Internal/MedPyExport/generate_binding/Release/medial-python${PY_VERSION}:${MR_TOOLS}/RepoLoadUtils/common
export BOOST_ROOT
```

> **Tip:** Adjust the `BOOST_ROOT`, `MR_LIBS`, and `MR_TOOLS` variables as needed for your system.
