
# Installation Guide

## Introduction

This guide describes how to install and set up the MES Infrastructure and its components. You can choose to install all or only the components you need, depending on your use case. These tools allow you to use [published models](../Models), train new models with [MES Tools](MES%20Tools%20to%20Train%20and%20Test%20Models.md), or work with the [Python API](Python%20API%20for%20MES%20Infrastructure.md).

## Prebuilt Releases

A prebuilt package (excluding [MES Tools](MES%20Tools%20to%20Train%20and%20Test%20Models.md)) is available for [direct download](https://github.com/Medial-EarlySign/MR_LIBS/releases/tag/V1.0). This eliminates the need for manual compilation. The binaries are built on **Ubuntu 24.04** and are compatible with any Linux distribution using **glibc ≥ 2.39**. You must also install [OpenMP support](#2-install-openmp-support-ubuntu).

## Prerequisites

Before building the tools, complete the following steps:

### 1. Install Compiler and Build Tools (Ubuntu)

Install the required compiler and build tools:

```bash
sudo apt install binutils gcc g++ cmake make -y
```

### 2. Install OpenMP Support (Ubuntu)

Install OpenMP for parallel processing:

```bash
sudo apt install libgomp1 -y
```

> **Note:** This step is required even if you don't plan to compile the tools. It is required for runtime.

### 3. Install Boost Libraries (Ubuntu)

#### Compiling Boost from Source

You can [download Boost](https://www.boost.org/users/download/) and compile it manually. Example steps for version 1.85.0:

```bash title="Boost Compilation"
# Install tools for download and extraction
sudo apt install bzip2 wget -y

# Download Boost
wget https://archives.boost.io/release/1.85.0/source/boost_1_85_0.tar.bz2

# Extract files
tar -xjf boost_1_85_0.tar.bz2
rm -f boost_1_85_0.tar.bz2

# Set up Boost install directory
WORK_BUILD_FOLDER=$(realpath .)
cd boost_1_85_0

# Configure and clean
./bootstrap.sh
./b2 --clean

# Build static libraries
./b2 cxxflags="-march=x86-64" link=static variant=release linkflags=-static-libstdc++ -j8 cxxflags="-fPIC" --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options --with-system --with-regex --with-filesystem

mkdir -p ${WORK_BUILD_FOLDER}/Boost/include

# Link headers to Boost/include
ln -sf ${WORK_BUILD_FOLDER}/boost_1_85_0/boost  ${WORK_BUILD_FOLDER}/Boost/include

# Build shared libraries (not needed for AlgoMarker, but needed for MES tools if you choose to compile)
./b2 cxxflags="-march=x86-64" link=shared variant=release linkflags=-static-libstdc++ -j8 cxxflags="-fPIC" --stagedir="${WORK_BUILD_FOLDER}/Boost" --with-program_options --with-system --with-regex --with-filesystem
```

#### Installing Boost via Package Manager

```bash
sudo apt install libboost-system1.83-dev libboost-filesystem1.83-dev libboost-regex1.83-dev libboost-program-options1.83-dev -y
```

> **Note:** On Ubuntu 22.04, Boost version 1.74 is available and compatible.
> 
> **Important:** This method does **not** work for the AlgoMarker library or the Python API. For those, you must compile Boost from source.

## Available Components

You can install any of the following five components:

1. [AlgoMarker Shared Library](AlgoMarker_Library.md): A shared Linux C library for accessing the AlgoMarker API and generating predictions/outputs from a model. Designed for production use, it supports only the essential "predict" and related APIs.
2. [AlgoMarker Wrapper](AlgoMarker%20Wrapper): A REST API wrapper for the AlgoMarker Shared Library.
3. [MES Tools to Train and Test Models](MES%20Tools%20to%20Train%20and%20Test%20Models.md): Command-line executables for training, testing, and manipulating models using the MR_LIBS infrastructure. Required for training new models. Alternatively, you can use the Python API.
4. [Python API for MES Infrastructure](Python%20API%20for%20MES%20Infrastructure.md): Python API for MR_LIBS, enabling model training, testing, and manipulation from Python. Some features may only be available via MES Tools or by [extending the Python API](../Python/Extend%20and%20Develop.md).
5. [MR_Scripts]: Useful Python and Bash scripts. Clone the repository with `git clone git@github.com:Medial-EarlySign/MR_Scripts.git`.

## Environment Setup Script

After installing the required components, use the following script to configure your shell environment for all tools and scripts:

```bash title="Start-Up Script"
#!/bin/bash

# Path to Boost Library (If you compiled the boost library)
LD_PATH=${HOME}/Documents/MES/Boost/lib
# Path to Git repository clones - here in the example, we clones all repositories under ${HOME}/Documents/MES
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

> **Tip:** Adjust the `LD_PATH`, `MR_LIBS`, `MR_TOOLS`, and `MR_SCRIPTS` variables as needed for your system.



