#!/usr/bin/env python2.7

import sys 
import os
import subprocess

homeDir = os.environ['HOME']
currDir = os.getcwd()

subprocess.call(["mkdir", "-p", homeDir+"/.hhg"])
subprocess.call(["ln", "-s", "conf_HHG.py", "Conf.ui", "start_HHG.py", "Start.ui", "plot_HHG.py","dd_HHG.py", homeDir+"/.hhg"])
subprocess.call(["ln", "-s", "hhg_dialogs", "hhg_io", "hhg_features", "hhg_plot", "dd_img", homeDir+"/.hhg"])
