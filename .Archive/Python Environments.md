# Python Environments
# Global paths
Python environments can be found in here: /nas1/Work/python-env
Python packages can be found in here: /nas1/Work/python-packages
 
current python environment is python36. in order to activate:
```bash
source  /nas1/Work/python-env/python36/bin/activate
#Or if your scripts git repository is updated:
python_env python36
```
# Create new python environment:
```bash
$MR_ROOT/Projects/Resources/python_env/create_py_env.sh 
#Can accept optional argument for location to setup the new environment (includes the name) - for example /nas1/Work/python-env/python36
#second argument is 0/1 flag to override existing if exists
```
The setup creates pip default config file in the environment to install new packages from /nas1/Work/python-packages. it can be found under /nas1/Work/python-env/$YOUR_ENV_NAME/pip.conf
Now you can just pip install when you want to install new package. The only thing you have to update is /nas1/Work/python-packages, using the next step.
## Medial library
Add code to activate script
 
```bash
PYTHONPATH=$MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/medial-python36
export PYTHONPATH
```
Add jupyter varaible:
```bash
export JUPYTER_RUNTIME_DIR=/var/opt/medial/dist/jupyter_kernels
```
 
## GPU support - update the activate script:
LD_LIBRARY_PATH="$[LD_LIBRARY_PATH:/usr/local/cuda-10.0/lib64](http://LD_LIBRARY_PATH/usr/local/cuda-10.0/lib64)"
# Download/Update packages to local repository of packages /nas1/Work/python-packages:
You need to update the folder /nas1/Work/python-packages.
There is script in the External Terminal 192.168.200.209 in 
```bat
P:\tools\python_env\get_packages.bat
###COMMENT### OR RUN THE PYTHON SCRIPT WITH ARGUMENTS FOR SPECIFIC PACKAGE - FOR EXAMPLE "pandas", CAN ALSO SPECIFY TEXT FILE WITH LINE FOR NEW PACKAGE WITH --package_list ARGUMENT:
C:\PYTHON37\python-3.7.2.amd64\python.exe --python_version "3.6"  --save_path "$PATH_TO_STORE_PACKAGES" --error_log "errors.log" --succ_log "succ.log" --log_level 2 --package_name "pandas"
```
The script downloads all packages from P:\tools\python_env\packages.list file and store them at P:\tools\python_env\packages. It creates error.list in the same folder with unfound packages.
<=Not anymore, it just adds new packages there (please use get_packages.bat and not update.OLD.bat)
After the process completes, copy P:\tools\python_env\packages into the Internal environment /nas1/Work/python-packages.
# Helpfull script to install multiple packages in the python environment from list:
Can be done with pip install -r $LIST_OF_PACKAGES after activating the correct python environment or by script:  $MR_ROOT/Projects/Resources/python_env/install_env.sh that installs the packges one by one from pacakges.list file and creates
log directory in the virtual environment of failed/success installations.
 
# Remarks
```python
>>> import tensorflow as tf
2020-10-29 13:34:21.939428: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudart.so.10.1
>>> tf.config.experimental.list_physical_devices('GPU')
020-10-29 13:54:01.090284: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcuda.so.1
2020-10-29 13:54:02.042019: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1716] Found device 0 with properties:
pciBusID: 0000:02:00.0 name: GeForce GTX 1080 Ti computeCapability: 6.1
coreClock: 1.582GHz coreCount: 28 deviceMemorySize: 10.92GiB deviceMemoryBandwidth: 451.17GiB/s
2020-10-29 13:54:02.042844: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1716] Found device 1 with properties:
pciBusID: 0000:81:00.0 name: GeForce GTX 1080 Ti computeCapability: 6.1
coreClock: 1.582GHz coreCount: 28 deviceMemorySize: 10.92GiB deviceMemoryBandwidth: 451.17GiB/s
2020-10-29 13:54:02.042894: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudart.so.10.1
2020-10-29 13:54:02.048298: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcublas.so.10
2020-10-29 13:54:02.052290: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcufft.so.10
2020-10-29 13:54:02.054009: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcurand.so.10
2020-10-29 13:54:02.058161: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcusolver.so.10
2020-10-29 13:54:02.060941: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcusparse.so.10
2020-10-29 13:54:02.068200: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudnn.so.7
2020-10-29 13:54:02.071301: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1858] Adding visible gpu devices: 0, 1
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:1', device_type='GPU')]
>>> tf.config.experimental.list_physical_devices('CPU')
[PhysicalDevice(name='/physical_device:CPU:0', device_type='CPU')]
```
 
In other nodes you will see:
```python
>>> import tensorflow as tf
2020-10-29 13:37:11.865139: W tensorflow/stream_executor/platform/default/dso_loader.cc:59] Could not load dynamic library 'libcudart.so.10.1'; dlerror: libcudart.so.10.1: cannot open shared object file: No such file or directory; LD_LIBRARY_PATH: /server/Work/Libs/Boost/latest/stage/lib:/usr/local/cuda-10.0/lib64
2020-10-29 13:37:11.865459: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
>>> tf.config.experimental.list_physical_devices('GPU')
[]
>>> tf.config.experimental.list_physical_devices('CPU')
[PhysicalDevice(name='/physical_device:CPU:0', device_type='CPU')]
```
 
  - med libary is added to the python path - the deafult search path is "$MR_ROOT/Libs/Internal/MedPyExport/generate_binding/Release/medial-python36". if not found, you will need to compile a sutiable version for this python. You can change library build to other path by controling this environment variable - PYTHONPATH - to point the new med library
## Jupyter Notebook
The jupyter is set as a service in each of the nodes 1-5. The scripts can be found in here: /etc/init.d/jupyter
To startthe service:
```bash
sudo service jupyter start
```
You can also stop it or check status by passing "stop" or "status".
logs can be found in here: /var/log/jupyter.log, /var/log/jupyter.err
You can open the notebook using the address - [http://node-01:9000/](http://node-01:9000/) - and change node number as needed. Make sure to enter personal workspace.
 
