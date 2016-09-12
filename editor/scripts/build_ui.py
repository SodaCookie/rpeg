"""Script used to compile all UI files in the ui folder to design
folders in the design folder"""

import os.path
import glob
import subprocess
import platform

PYQT_AVAILABLE = False
PYSIDE_AVAILABLE = False

print("Checking for PyQt or PySide...")
try:
    import PyQt5
    PYQT_AVAILABLE = True
except ImportError:
    print("No PyQt5 installed.")

try:
    import PySide
    PYSIDE_AVAILABLE = True
except ImportError:
    print("No PySide installed.")

if not PYQT_AVAILABLE and not PYSIDE_AVAILABLE:
    print("No installation found. Quiting...")
    quit()

if PYQT_AVAILABLE:
    print("Using PyQt5...")
    command = "pyuic5"
elif PYSIDE_AVAILABLE:
    print("Using PySide...")
    command = "pyside-uic"

if platform.system() == 'Windows':
    design_files = glob.glob(os.path.dirname(__file__)+"ui/*.ui")
else:
    design_files = glob.glob(os.path.dirname(__file__)+"/../ui/*.ui")

for file in design_files:
    if platform.system == "Windows":
        output = os.path.join(os.path.dirname(__file__)+"design/", os.path.split(file)[1].split(".")[0]+"_design.py")
    else:
        output = os.path.join(os.path.dirname(__file__), "../design", os.path.split(file)[1].split(".")[0]+"_design.py")
    print("Building file %s to output %s" % (os.path.relpath(file), os.path.relpath(output)))
    if platform.system() == 'Windows':
        subprocess.call([command, file, "-o", output], shell=True)
    else:
        subprocess.call([command, file, "-o", output])
