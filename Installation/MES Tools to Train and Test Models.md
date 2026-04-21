
## MES Tools to Train and Test Models

### Overview
These are command-line executables for training, testing, and manipulating models, as well as other utilities developed by MES.

You can download a prebuilt release from the [Release page](https://github.com/Medial-EarlySign/medpython/releases/tag/V1.0.1). The release is built with glibc 2.17 and will work out of the box on systems with **glibc ≥ 2.17** (e.g., **Ubuntu >= 13.04**, **Centos>=7**, eg.). If you need to build from source, follow the instructions below.

For general instructions on how to use prebuilt binaries, refer to the Prebuilt Releases section in the main Installation Guide.

### Installation Steps

1.  **Install Boost Libraries:** Follow the instructions in the [Install Boost Libraries](index.md#3-install-boost-libraries-ubuntu) section of the main Installation Guide. Boost is a core dependency for MES Tools. If you compile Boost from source, ensure `BOOST_ROOT` is set correctly.
2. Clone the required repositories:
   ```bash
   git clone git@github.com:Medial-EarlySign/MR_Tools.git
   git clone git@github.com:Medial-EarlySign/medpython.git MR_LIBS
   ```
3. Change to the `MR_Tools` directory:
   ```bash
   cd MR_Tools
   ```
4.  **Configure Build Paths:** Instead of directly editing `CMakeLists.txt`, it's recommended to pass configuration variables via CMake arguments or environment variables.

    *   **`MR_LIBS` Path:** The build system needs to know the location of your `medpython` (MR_LIBS) clone.
        If your directory structure is:
        ```
        Root Directory
        ├── MR_LIBS
        └── MR_Tools
        ```
        then the build script should automatically detect `MR_LIBS`. Otherwise, you might need to set the `LIBS_PATH` environment variable before running the build script, or pass it as a CMake argument.

    *   **`BOOST_ROOT` Path (if compiled from source):** If you compiled Boost from source, ensure the `BOOST_ROOT` environment variable is set to your Boost installation directory (e.g., `/home/user/my_builds/Boost`). The build system will use this to find Boost.

    **Example of setting environment variables before building:**
   ```
   export LIBS_PATH="/path/to/your/medpython/clone" # e.g., /home/user/Documents/MES/MR_LIBS
   export BOOST_ROOT="/path/to/your/compiled/Boost" # Only if you compiled Boost from source
   ```
5. Build the tools:
   ```bash
   AllTools/full_build.sh
   ```

A full docker image for compilation steps can be found under this link:

* [01.basic_boost](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/01.basic_boost) A base docker image with Boost
* [02.build_tools](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/medbuild_tools.new/02.build_tools) A build with tools prepared for usage

### Verification

To verify that the MES Tools have been successfully built, you can try running one of the command-line executables.

```bash
# After sourcing your environment setup script (e.g., source ~/setup_mes_env.sh)
Flow --version
```

This command should output the version information for the `Flow` executable, indicating a successful build and correct environment setup.

## Common Issues

1. Can't find Boost libray errors in compilation - Please delete the "./build" folder to recreate all Makefiles again. It holds some bad settings of Boost in cache.

2.  **Can't find `boost_atomic.so` in runtime:** This usually indicates a linking issue. Ensure that your `BOOST_ROOT` (if compiled from source) is correctly set and that `LD_LIBRARY_PATH` includes the Boost library directory. The `full_build.sh` script and `CMakeLists.txt` should ideally handle linking `boost_atomic` automatically if it's a required component. If not, you might need to explicitly add it to the `BOOST_LIBS` in the `CMakeLists.txt`.

3. Running an executable may fail with:
```bash
$> Flow ...
Flow: error while loading shared libraries: libboost_regex.so.1.85.0: cannot open shared object file: No such file or directory
```
This indicates the Boost shared libraries are not found at runtime. Set `LD_LIBRARY_PATH` to point to your Boost lib directory. Add to your ~/.bashrc or run once per session:
```bash
export LD_LIBRARY_PATH=/path/to/BOOST_ROOT/lib
```
If Boost was installed via the system packages (Ubuntu 22.04 uses 1.74, 24.04 uses 1.83), install the appropriate dev packages instead of adjusting `LD_LIBRARY_PATH`:
```bash
sudo apt install libboost-program-options1.83-dev -y
```
Replace 1.83 with 1.74 on Ubuntu 22.04 when needed.
