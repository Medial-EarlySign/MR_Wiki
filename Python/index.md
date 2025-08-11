# Python
In the following sub-pages you will find information about Python utilization in Medial.
 
- [Medial's C++ API in Python](Medial's%20C++%20API%20in%20Python)
  - [Build the python extention](/Python/Build%20the%20python%20extention)
  - [Examples](/Python/Examples)
  - [Extend and Develop](/Python/Extend%20and%20Develop)
  - [Python AlgoMarker API Wrapper](/Python/Python%20AlgoMarker%20API%20Wrapper)
  - [Usage](/Python/Usage)
- [Python binding Troubleshooting](Python%20binding%20Troubleshooting)

## Quick start (Usage Level)

We compiled our own Python distribtion - 3.12 and also have 3.10
The Medial Distribution tree resides at nas storage (That we will have the same copy/environment for all nodes) /nas1/Work/python-env/python312.
System users should still be able to use the local python shiped with the OS, just run deactivate in terminal (The default is to use the shared python environment).

To use the distribution you should execute the following command:
```bash
. /nas1/Work/python-env/python312/bin/activate
# to return to systems python
deactivate
# Already set in system level for all users to use this python
```

You may want to put this line in your ~/.bashrc and ~/.bash_profile , to load that python envirnment every time you log on:
```bash
echo "source /nas1/Work/python-env/python312/bin/activate" >> ~/.bashrc
echo "source /nas1/Work/python-env/python312/bin/activate" >> ~/.bash_profile
```