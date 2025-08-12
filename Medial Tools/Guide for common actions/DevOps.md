# DevOps
1. 
Compile all tools, from anywhere:
```bash
compile_all.sh
```
The executables can be found here: $MR_ROOT/Tools/AllTools/Linux/Release
2. 
Compile python:
```bash
build_py_wrapper.sh
```
If there are issues: [Build the python extention](/Python/Medial's%20C++%20API%20in%20Python/Build%20the%20python%20extention.html)
3. 
Pack all tools to external environment:
```bash
full_pack_all.sh
```
In the remote machine, unzip the mes_full.tar with "tar -xvf mes_full.tar" and run "medial_earlysign_setup.sh" to setup environment.
The environment is similar to what we have in the docker: Ubuntu docker (medial_dev). We can also install a docker if possible. In my opinion docker is 2nd priority.
This is based on those actions. If you don't want to to do all of them:
<table><tbody>
<tr>
<th>Command</th>
<th>Description</th>
<th>output path</th>
<th>Where to extract</th>
</tr>
<tr>
<td><pre>full_build.x86-64.sh</pre></td>
<td><pre>Builds all our tools for X86_64 computers: Flow, bootstrap_app, etc.</pre></td>
<td>/nas1/UsersData/git/MR/Tools/AllTools/Linux/Release/bin_apps.x86-64.tar.bz2</td>
<td><p>#copy to file to /earlysign/bins</p><p>cd /earlysign/bins</p><p>tar -xvf bin_apps.x86-64.tar.bz2</p></td>
</tr>
<tr>
<td><pre>pack_etl.sh</pre></td>
<td>Packs all ETL Infra code</td>
<td>/server/Linux/${USER%-*}/ETL.tar.bz2. USER might be: git if run from "<pre>full_pack_all.sh" or your username without "-internal"</pre></td>
<td>#copy to file to /earlysign/scripts<br/>cd /earlysign/scripts<br/>tar -xvf ETL.tar.bz2</td>
</tr>
<tr>
<td>pack_libs.sh</td>
<td>Packs all "External libs" needed for "full_build.x86-64.sh". For example, xgboost, lightGBM &amp; boost.<br/>There are not suppose to be "updates" in here.</td>
<td>/server/Linux/${USER%-*}/libs.tar.bz2. <span>USER might be: git if run from "</span><pre>full_pack_all.sh" or your username without "-internal"</pre></td>
<td><p>#copy to file to /earlysign/libs</p><p>cd /earlysign/libs</p><p>tar -xvf libs.tar.bz2</p></td>
</tr>
<tr>
<td>pack_scripts.sh</td>
<td>Packs all our helper scripts like: AutoValidation kits, bootstrap_format.py, plot.pt, paste.pl, etc.</td>
<td>/server/Linux/${USER%-*}/scripts.tar.bz2  <span>USER might be: git if run from "</span><pre>full_pack_all.sh" or your username without "-internal"</pre></td>
<td><p>#copy to file to /earlysign/scripts</p><p>cd /earlysign/scripts</p><p>tar -xvf scripts.tar.bz2</p></td>
</tr>
<tr>
<td>build_py_wrapper.sh</td>
<td>Builds the python wrapper for our infrastructure.</td>
<td>/server/Linux/${USER%-*}/PY.tar.bz2 <span>USER might be: git if run from "</span><pre>full_pack_all.sh" or your username without "-internal"</pre></td>
<td><p>#copy to file to /earlysign/libs</p><p>cd /earlysign/libs</p><p>tar -xvf PY.tar.bz2</p></td>
</tr>
<tr>
<td>Additional helper scripts:</td>
<td>A setup script that setup/update the environment: /nas1/UsersData/git/MR/Projects/Scripts/Bash-Scripts/usefull:<br/>medial_earlysign_setup.sh, <br/>medial_earlysign_resetup.sh</td>
<td><span><span>/nas1/UsersData/<span>${USER%-*}</span>/MR/Projects/Scripts/Bash-Scripts/usefull <br/><span>USER might be: git if run from "</span></span></span>full_pack_all.sh" or your username<br/> without "-internal"</td>
<td> </td>
</tr>
</tbody></table>
4. 
Jupyter is down in the internal? 
```bash
sudo systemctl restart jupyter
```
 
