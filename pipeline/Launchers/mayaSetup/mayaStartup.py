import os
import inspect
import subprocess
import sys

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

setup_dir = os.path.join(current_directory, "userSetup")
os.environ["PYTHONPATH"] = setup_dir

subprocess.Popen([r"C:\Program Files\Autodesk\Maya2018\bin\maya.exe"])