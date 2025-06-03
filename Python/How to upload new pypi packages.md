# How to upload new pypi packages
1. On the external computer, go to: P:\tools\python_env (P: being the "Public" drive)
2. For convenience, delete files in "packages_extra" (the packages from previous runs)
3. Run "get_package_by_name.sh" and input names of all packages you wish to download. It will automatically download dependencies.
4. Copy contents of "packages_extra" to:internal at /nas1/Work/python-packages/3.10.
5. Run pip install normally.
 
 
 
