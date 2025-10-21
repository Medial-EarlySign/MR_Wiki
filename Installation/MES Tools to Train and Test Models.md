
## MES Tools to Train and Test Models

### Overview

These are command-line executables for training, testing, and manipulating models, as well as other utilities developed by MES.

You can download a prebuilt release from the [Release page](https://github.com/Medial-EarlySign/MR_Tools/releases/tag/V1.0). The release is built with glibc 2.35 and will work out of the box on systems with **glibc ≥ 2.35** (e.g., **Ubuntu 22.04**). If you need to build from source, follow the instructions below.

### Installation Steps

1. [Install Boost Libraries](index.md#3-install-boost-libraries-ubuntu). Compilation is not required, you might install from pacakge manager.
2. Clone the required repositories:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   git clone git@github.com:Medial-EarlySign/MR_LIBS.git
   ```
3. Change to the `MR_Tools` directory:
   ```bash
   cd MR_Tools
   ```
4. Edit `All_Tools/CMakeLists.txt` to set `LIBS_PATH` to the path of your MR_LIBS clone. If your directory structure is:
   ```
   Root Directory
   ├── MR_LIBS
   └── MR_Tools
   ```
   then no changes are needed. If you compiled Boost, also set `BOOST_ROOT` in the CMakeLists.txt file.
5. Build the tools:
   ```bash
   AllTools/full_build.sh
   ```

A full docker image for compilation can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [02.build_tools](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/02.build_tools) A build with tools prepared for usage