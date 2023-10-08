import subprocess
import os
import inspect

nuke_version = os.getenv("nuke_version")
nuke_dir_path = os.getenv("nuke_dir_path")
current_directory = os.path.dirname(inspect.getfile(inspect.currentframe()))
os.environ["NUKE_PATH"] = '{}/setup'.format(current_directory)
nuke_exe=os.path.join(nuke_dir_path, "Nuke"+nuke_version + ".exe")
print("nuke_exe", nuke_exe)
subprocess.call([nuke_exe, '--disable-nuke-frameserver'])
