import os
import inspect
import subprocess
import sys

import maya.utils as utils
import pymel.core as pm

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

PIPELINE_PATH = os.environ.get("PIPELINE_PATH").split("pipeline")[0]
if PIPELINE_PATH not in sys.path:
    sys.path.append(PIPELINE_PATH)

import pipeline.CoreModules.common_utils
import toolslist

parent_menu_name = 'Innovative-Colors'


def build_menu():
    menu_name = parent_menu_name+"_menu"
    if pm.menu(menu_name, exists=1):
        pm.delete(menu_name)
    
    # add to the main menu
    root_menu = pm.menu(menu_name, p='MayaWindow', to=1, aob=1, l=parent_menu_name)
    pm.menuItem(p=root_menu, d=1)
    
    assetManager = pm.menuItem('Asset Manager', p=root_menu, c=toolslist.asset_manager, l='Asset Manager')

    shader_library = pm.menuItem('Shader Library', p=root_menu, c=toolslist.shaderLibrary, l='Shader Library')

def _LOAD_TOOLS_():
    utils.executeDeferred('build_menu()')
    
    
_LOAD_TOOLS_()