
## AlgoMarker Library

### Overview

The AlgoMarker shared library enables deployment of the AlgoMarker model. It provides a C-level API to load, apply, and retrieve results from your binary model output.

You can download a prebuilt release from the [Release page](https://github.com/Medial-EarlySign/MR_LIBS/releases/tag/V1.0). The release is built with glibc 2.39 and will work out of the box on systems with **glibc ≥ 2.39** (e.g., **Ubuntu 24.04**). If you need to build from source, follow the instructions below.

### Installation Steps

1. Complete the [Preliminary Steps](index.md#prerequisites) to set up your build environment (install cmake, gcc, and libgomp1).
2. [Compile the Boost Libraries](index.md#compiling-boost-from-source). You must build Boost from source.
3. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_LIBS.git
   ```
4. Edit `Internal/AlgoMarker/CMakeLists.txt` and add:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   Set this path to your Boost build directory (`WORK_BUILD_FOLDER` from step 2). Ensure the compiled libraries are in `/libs` and headers in `/include`.
5. Build the library:
   ```bash
   Internal/AlgoMarker/full_build.sh
   ```

A full docker image for compilation can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [03.algomarker](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/03.algomarker) A build with algomarker library