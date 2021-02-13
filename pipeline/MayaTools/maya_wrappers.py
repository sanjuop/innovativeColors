import os

import maya.OpenMayaUI as omui
from PySide2 import QtGui, QtCore, QtWidgets
from shiboken2 import wrapInstance

import pymel.core as pm

def saveFile(path):
    path = path+".ma"
    pm.saveAs(path)

def getFilePath():
    return pm.sceneName()

def getBaseName(ext=False):
    file_path = getFilePath()
    base_name = str(file_path.basename().splitext()[0])
    if not ext:
        return base_name
    return base_name


def get_assembly_nodes():
    exclude = ["persp", "top", "front", "side"]
    all_assemblies = [i for i in pm.ls(assemblies=True) if i.name() not in exclude]
    return all_assemblies

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)