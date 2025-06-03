# Medial's Python Environment Project
Documentation about the Python working environment in medial
## Quick start (Usage Level)
It was decided not to use Anaconda or Redhat's Python because : 
- we need to be able to compile Python on our own, sometimes for specific hardware with certain flags.
- Anaconda heavily relies on an internet connection.
- Redhat's software is outdated. The RPMs based distribution is missing some key features.
We compiled our own Python distribtion along with python2, R and nodejs.
The Medial Distribution tree resides at /opt/medial/dist.
Redhat/Centos system users should still be able to use the Python2 to run system scripts so the Medial distribution is not available globally.
To use the distribution you should execute the following command:
```bash
. /opt/medial/python36/enable
# for Python2 run:
. /opt/medial/python27/enable
# to use Medial's Python3 permanently for all future logins run:
echo "source /opt/medial/python36/enable" >> ~/.bashrc
echo "source /opt/medial/python36/enable" >> ~/.bash_profile
```
## Building The Python distribution
In case of need, we'd like to update our software, install new packages , add more programs. The environment building process takes a long while and requires interned connection. 
To rebuild the environment use this script:
```bash
cd $MR_ROOT/Projects/Scripts/Bash-Scripts/medial-dist-builder/
# first export the script to run on external linux computer with internet connection
./install -x -r /tmp/
# collect the tarball from /tmp/, untar it on external computer and execute
./install
# When finished you may generate a tarball containing the distribution:
./install -x -p /tmp/
# This file may take up to 10GB of disk space. 
# remove the old /opt/medial and untar the new distribution
```
You may add packages you need in  $MR_ROOT/Projects/Scripts/Bash-Scripts/medial-dist-builder/conf/pip_install_list.txt .
 
 
