
## MES Tools to Train and Test Models

### Overview

These are command-line executables for training, testing, and manipulating models, as well as other utilities developed by MES.

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
