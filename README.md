

# About the repo
This repository contains the Python and Javascript files used in my thesis paper for computer science and engeneering.

# Pre-requisites
1) A rooted AVD with a Frida server running.
2) MobSF installed on a container.
3) A rooted AVD managed by MobSF scripts.
4) The ADB commandline shell.

The official documentation will probably do a better job to explain how to do these things that i could ever do, so i 'll leave the links with the official documentation.

Android Studio guide for making AVDs
https://developer.android.com/studio/run/managing-avds

MobSF repository:
https://github.com/MobSF/Mobile-Security-Framework-MobSF

Magisk repository:
https://github.com/topjohnwu/Magisk

Frida webiste:
https://frida.re/

# How to use
Install the requirments using **pip3 install -r requirements.txt**.
 The MobSF folder contains 2 scripts: 
 
1) To use them, you'll need to setup a target folder in the same folder with the scripts (You can see and change the name in the python file)
2) Inside target folder, for each application you analyze with MobSF, you're gonna need to create a subfolder, in which you put the .tar file containing the application files and the .txt file containing the HTTP traffic.

 The Frida folder contains various scripts: 
 1) If you want to run the js script you can use **Frida -U -f "application" -l class_method_signatures.js**
 2) You can run the frida trace script using **run-trace.py**, you can define inside the python file which syscalls to check. If you want to add your syscalls, call **Frida-trace -U -f "application" -i "syscall or function"**, then modify manually the generated hooks.
3) Once you have any data, you can run the other Python files.

# Acknowledgments
For the class_method_signatures.js functions:
https://github.com/0xdea/frida-scripts

Thesis related to the repo:
TODO


