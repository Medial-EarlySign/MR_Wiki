
## Python API for MES Infrastructure

### Overview
`MedPython` package provides a Python API for the MES Infrastructure, allowing you to train and manipulate MES models.

**Installation**

Requires Python 3.8+.

There are two primary ways to install `medpython`:

1.  **Using `pip` from PyPI (Recommended for most users):**
    This is the simplest method and provides prebuilt wheels for supported platforms.

```bash
pip install medpython
```

Alternatively anaconda can be used with `conda-forge` channel:

```bash
conda install medpython
```

Build from source:
```bash
python -m pip install -v "medpython @ git+https://github.com/Medial-EarlySign/medpython.git/#subdirectory=Internal/MedPyExport/generate_binding"
```

**Platform Support** 

| Platform | x86_64 (Intel/AMD) | aarch64 (ARM / Apple Silicon) |
| :--- | :--- | :--- |
| **Linux (glibc)** | ✅ Pre-built (Py 3.10-3.14) | ✅ Pre-built (Py 3.13) |
| **Linux (Alpine/musl)**| 🛠️ Compile Required | 🛠️ Compile Required |
| **Windows** | ✅ Pre-built (Py 3.10-3.14) | 🛠️ Compile Required |
| **macOS** | ✅ Pre-built (Py 3.10-3.14) | 🛠️ Compile Required |

Conda provide precompiled binaries for all python 3.10-3.14 within windows, macOS, linux_x86_64, linux_aarch64

> **Note:** For any Compile Required or either not listed as Pre-built. Compliation is required.
> See the "Build from Source" instructions below.

### Installation Steps

1. Install required system libraries:
   ```bash
   sudo apt install python3-dev swig -y
   ```
2. Ensure NumPy is installed:
   ```bash
   python -m pip install numpy
   ```
   > This API supports both NumPy 1.x and 2.x. For maximum compatibility, compile with NumPy 2.x (works for clients with either version). Compiling with NumPy 1.x will **not** work for clients using 2.x.
3. Build the Python API:
   ```bash
   cd Internal/MedPyExport/generate_binding
   pip install . -vv
   ```

A full docker image for compilation steps can be found under this link:

* [04.medpython](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/04.medpython) A build with the python. Please edit, install your python version in the build. This will use the python 3.10 on manylinux2014 (Centos 7) to support all linux distros with glibc >= 2.17. If you need a different version, please install it inside the docker before executing the setup script

#### Alpine

Install those Alpine packages
```bash
apk add py3-pip
apk add gcc g++ make python3-dev 

python -m pip install numpy "swig<4.3"
```
 
 Just run the install script `pip install . -vv`
