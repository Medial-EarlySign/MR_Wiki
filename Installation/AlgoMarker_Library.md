
## AlgoMarker Library

### Overview
The AlgoMarker shared library enables deployment of the AlgoMarker model. It provides a C-level API to load, apply, and retrieve results from your binary model output.

You can download a prebuilt release from the [Release page](https://github.com/Medial-EarlySign/medpython/releases/tag/V1.0.1). The release is built with glibc 2.17 and will work out of the box on systems with **glibc ≥ 2.17** (e.g., **Ubuntu >= 13.04**, **Centos>=7**, eg.). If you need to build from source, follow the instructions below.

For general instructions on how to use prebuilt binaries, refer to the Prebuilt Releases section in the main Installation Guide.

### Installation Steps

1.  Complete the Common [Prerequisites](index.md#prerequisites) and Compiler and Build Tools steps in the main Installation Guide to set up your build environment.
2. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/medpython.git MR_LIBS
   ```
3. Build the library:
   ```bash
   Internal/AlgoMarker/full_build.sh
   ```

A full docker image for compilation steps can be found under this link:
* [03.algomarker](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/03.algomarker) A build with algomarker library

### Verification

To verify that AlgoMarker Library has been successfully built and is accessible, you can try and use [AlgoMarker Wrapper](AlgoMarker%20Wrapper)