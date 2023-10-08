import os
import sys
import nuke
import inspect

all_dirs = os.listdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
for folder in all_dirs:
    nuke.pluginAddPath("./{FL}".format(FL=folder))

PipelineBasePath = os.getenv("_PYTHON_PATH_")
if PipelineBasePath not in sys.path:
    sys.path.append(PipelineBasePath)
