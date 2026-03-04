## C++ Native Wrapper

A prebuilt release is available on the [Release page](https://github.com/Medial-EarlySign/medpython/releases/tag/V1.0.1). The release is built with glibc 2.17 and will work out of the box on systems with **glibc ≥ 2.17** (e.g., **Ubuntu >= 13.04**, **Centos>=7**, eg.). If you need to build from source, follow the instructions below.

### Compilation Steps

1. Follow the [Preliminary Steps](../index.md#prerequisites) to setup build enviroment with cmake, cmake, gcc and libgopmp1
2. (**Optional Step**) [Compile the Boost Libraries](../index.md#compiling-boost-from-source). Don't forget to set environment variable `BOOST_ROOT` to reference the Boost build directory. Ensure the compiled libraries are in `/libs` and headers in `/include`.
3. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   ```
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
      Refer to [AlgoMarker Library](../AlgoMarker_Library.md)) for compilation steps.

A full docker image for compilation steps can be found under this link:

* [05.algomarker_wrapper](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/05.algomarker_wrapper) A build with algomarker wrapper