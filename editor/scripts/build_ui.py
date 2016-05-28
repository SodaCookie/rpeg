"""Script used to compile all UI files in the ui folder to design
folders in the design folder"""

import os.path
import glob
import subprocess

design_files = glob.glob(os.path.dirname(__file__)+"/../ui/*.ui")
for file in design_files:
    output = os.path.dirname(__file__)+"/../"+"design/"+os.path.split(file)[1].split(".")[0]+"_design.py"
    print("Building file %s to output %s" % (os.path.relpath(file), os.path.relpath(output)))
    subprocess.call(["pyuic5", file, "-o", output], shell=True)