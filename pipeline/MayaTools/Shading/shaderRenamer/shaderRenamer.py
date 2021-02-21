import inspect
import os
import tempfile
import sys
import shutil
import subprocess

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QFile, QObject
import pymel.core as pm

from shaderRenamerLogger import ShaderRenamerLogger
import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
from pipeline.MayaTools.workspace_control import DockableUI
import utils as utils;reload(utils)

class ShaderRenamer(QtWidgets.QWidget):
    def __init__(self):
        super(ShaderRenamer, self).__init__()

        self.setWindowTitle("Shader Renamer")

        ShaderRenamerLogger.info("setting up ui...")

        self.setFixedWidth(300)
        
        self.shadersLable = QtWidgets.QLabel("shaders")
        self.connected_nodes = QtWidgets.QLabel("connected nodes")

        self.shadersListView = QtWidgets.QListWidget()
        self.connectedListView = QtWidgets.QListWidget()

        self.renameLineEdit = QtWidgets.QLineEdit()
        self.renameBtn = QtWidgets.QPushButton("Rename Shader")

        main_layout = QtWidgets.QHBoxLayout(self)
        
        shader_layout = QtWidgets.QVBoxLayout()
        shader_layout.addWidget(self.shadersLable)
        shader_layout.addWidget(self.shadersListView)
        shader_layout.addWidget(self.renameLineEdit)
        shader_layout.addWidget(self.renameBtn)

        connection_layout = QtWidgets.QVBoxLayout()
        connection_layout.addWidget(self.connected_nodes)
        connection_layout.addWidget(self.connectedListView)


        main_layout.addLayout(shader_layout)
        main_layout.addLayout(connection_layout)
       
        
        self.setLayout(main_layout)

        ShaderRenamerLogger.info("ui display")
        self.all_shders = self.getAllShaders()

    def getAllShaders(self):
		#returns all shaders in the scene. that's connected to a shading group.
        ignoreSg = ['initialParticleSE', 'initialShadingGroup']
    
        shadingGroups = pm.ls(type="shadingEngine")
		#stores all the child nodes for the shader
        allDependencies = dict()
        
        ShaderRenamerLogger.info("getting all shaders in the scene.")
        for sg in shadingGroups:
            if sg.name() not in ignoreSg:
                ShaderRenamerLogger.info(""+str(sg))
                connectedShader = pm.connectionInfo(sg+".surfaceShader", sfd=True)
                connectedShader = connectedShader.split(".")[0]
                if connectedShader == "":
                    continue
                allDependencies[connectedShader] = utils.getUpstreamNodes(connectedShader)
		return allDependencies

win=None
def main(debug=False):
	#launch shader renamer
    global win
    try:
        win.close()
    except:
        pass
    win = ShaderRenamer()
    win.show()
    return
