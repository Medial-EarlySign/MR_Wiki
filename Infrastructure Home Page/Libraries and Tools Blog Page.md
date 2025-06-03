# Libraries and Tools Blog Page
A page to chronically announce information regarding the MR Libs and Tools code repositories. Please include name and date when you add a record and try to stick to the format.
 
###   - Alon - Build script to compile all our apps with documentition of git version
When including MedUtils we can use medial::get_git_version() which returns a string with git information about Libs and Tools Repositories used to complie the application.
Running our apps with --debug will print the app version and --version will just output the application version and exit.
- To compile all our tools with version info use build scripts in Scripts Repo: $MR_ROOT/Projects/Scripts/Bash-Scripts/full_build.sh
- example of version output running: bootstrap --version
*Version Info:*
*Build on 14-01-2019_17:42:20*
*=>Libs Git Head: 8fdbf55f32fc550420f300d391c88295bcb3a46a by avi at 2019-01-14*
*Last Commit Note: pushing the correct val in the diabetes registry*
*=>Tools Git Head: 97e7e06988a606781dda39625507d9702e146ac9 by avi at 2019-01-14*
*Last Commit Note: a diabetes read code list capabale of working with a registry rep processor*
### **06/01/2018 - Shlomi - Minor changes in our Python Environment and binding**
- The old Jupyter on node-02 (based on Anaconda2 ) was shut down. The old notebooks are available at: (node-02) /home/python/Now [http://node-02:8888](http://node-02:8888) will direct you to the New Py2/Py3/R enabled Jupyter installation. Keep in mind that it is preferable to use JupytherHub which is available at [http://node-0X:9000/](http://node-0X:9000/) since it is much more suitable for multiple users. The kernel you run is owned by your unix user and it directs you to your own directory at startup. Use port 8888 to share notebooks and present work.Use /server/Work/Shared/notebooks/ to copy and manipulate the actual files.
- The "Generic Python Binding" installation was deleted. From now on, if you want to use it, you will have to compile your own:cd $MR_ROOT/Libs/Internal/ ; git pullcd $MR_ROOT/Libs/Internal/MedPyExport/generate_binding ; ./make-all.shJupyterhub kernels (port 9000) will find your compiled Python Binding automatically, regular Jupyter kernels (port 8888) , OTOH, will require the usual sys.path.insert(…)
- The nltk sample data was eventually moved from /opt/medial/dist/usr/share/nltk_data on all nodes to /server/Work/Shared/nltk_data to free space on local nodes HDs.
- The latest commit to the Python Binding will provide a readable online help in the python console using 'help(med)'. Try it. Other documentation will be added to the Wiki.
- It is now possible to run 'import med' instead of the usual 'import medpython as …'It will provide a "cleaner" namespace.
 
### 16/12/2018 - Avi - MedIO and SerializableObject libraries
- MedIO was separated from MedUtils to be a standalone library
- SerializableObject was separated from MedProcessTools to be a standalone library
- Libraries compile, Flow compiles, you may need to do some changes to your projects for them to compile
- You need to update MR_LIBS_NAME (see the landing page - it was updated)
- You need to pull the resources scripts for the MR_LIBS_NAME in Linux
- From now on if you need any of the MedIO routines use:  #include <MedIO/MedIO/MedIO.h>
- From now on if you need the SerializableObject class use:  #include <SerializableObject/SerializableObject/SerializableObject.h>
 
### 18/12/2018 - Avi Clutter cleaning stage 1
Several changes in libraries, in order to get rid of old unused code, and break out messy libraries into meaningful libraries, to increase code quality and decrease dependencies.
- MedFeat is no more : you served us well, may you rest in peace. Contained mainly old unused code, needed remains were left in other places.
- MedSplit : a very small library, left over from MedFeat.
- Retired : a new library with old unused code (in case we will in some weird scenario need to compile some very old code)
- global time variables were moved to MedTime , their natural place.
- rand_1, rand_N were moved to MedGlobalRNG.h in MedUtils , since they are now implemented there, using them requires only the include of this h file and no need for the MedUtils library itself.
- MedMat : was split into a new library , if you need a MedMat make sure to : #include <MedMat/MedMat/MedMat.h>
- med_stoi, med_stof : created annying dependencies and were moved to SerializableObject : a more natural position.
- Again MR_LIBS_NAME was updated, see the landing page for windows, and pull the startup.sh script for linux (don't forget to close/open visual studio and linux terminals after the update)
