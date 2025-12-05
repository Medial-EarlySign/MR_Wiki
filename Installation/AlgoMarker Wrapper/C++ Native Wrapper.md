## C++ Native Wrapper

A prebuilt release is available on the [Release page](https://github.com/Medial-EarlySign/medpython/releases/tag/V1.0.1). The release is built with glibc 2.17 and will work out of the box on systems with **glibc ≥ 2.17** (e.g., **Ubuntu >= 13.04**, **Centos>=7**, eg.). If you need to build from source, follow the instructions below.

### Compilation Steps

1. Follow the [Preliminary Steps](../index.md#prerequisites) to setup build enviroment with cmake, cmake, gcc and libgopmp1
2. [Set up Boost Libraries](../index.md#3-install-boost-libraries-ubuntu). You can also install it from package manager and you are not forced to compile the Boost package.
3. Clone the repository:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   ```
4. If you compiled the Boost library, edit `AlgoMarker_python_API/ServerHandler/CMakeLists.txt` to include the following line:
   ```cmake
   set(BOOST_ROOT "$ENV{HOME}/boost-pic-install")
   ```
   This should point to your Boost compiled home directory (`WORK_BUILD_FOLDER` from step 2) from the compilation step. Ensure the compiled libraries are in `/libs` and the headers are in `/include`.
   Alternatively you can just set your environment variable `BOOST_ROOT` to reference the Boost build directory. 
5. Compile the wrapper:
   ```bash
   AlgoMarker_python_API/ServerHandler/compile.sh
   ```
6. Execute the server:
   ```bash
   AlgoMarker_python_API/ServerHandler/Linux/Release/AlgoMarker_Server --algomarker_path $AM_CONFIG --library_path $AM_LIB --port 1234
   ```

    * `AM_CONFIG`: Path to the AlgoMarker configuration file.
   * `AM_LIB`: Path to the AlgoMarker shared library. 
      Refer to [AlgoMarker Library](../AlgoMarker_Library.md)) for compilation steps.

A full docker image for compilation steps can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [05.algomarker_wrapper](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/05.algomarker_wrapper) A build with algomarker wrapper