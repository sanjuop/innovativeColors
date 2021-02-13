import os
import inspect
import subprocess
import sys

import maya.utils as utils

import menu

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

PIPELINE_PATH = os.environ.get("PIPELINE_PATH").split("pipeline")[0]
if PIPELINE_PATH not in sys.path:
    sys.path.append(PIPELINE_PATH)

import pipeline.CoreModules.common_utils

def _LOAD_TOOLS_():
    tools='menu.build_menu()'
    utils.executeDeferred(tools)
    
    
_LOAD_TOOLS_()