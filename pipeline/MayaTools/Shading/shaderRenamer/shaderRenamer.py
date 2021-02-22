import inspect
import os
import tempfile
import sys
import shutil
import subprocess
import json

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QFile, QObject
import pymel.core as pm

from shaderRenamerLogger import ShaderRenamerLogger
import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
import pipeline.CoreModules.common.common_utils as common_utils;reload(common_utils)

node_map_file = os.path.join(os.path.dirname(__file__), "nodeMapping.json")

node_map_data = common_utils.read_json_file(node_map_file)

class ShaderRenamer(QtWidgets.QWidget):
    IGNORE_NODES = ["colorManagementGlobals", "defaultShaderList", "materialInfo"]
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

        self.addShader_to_ui()

        self.shadersListView.itemSelectionChanged.connect(self.showDependencyNodes)
        self.renameBtn.clicked.connect(self.RenameShader)
    
    def RenameShader(self):
        if self.renameLineEdit.text() == "":
            pm.confirmDialog(b="Ok", m="Enter Shader name")
            return
        custom_shader_name = self.renameLineEdit.text()
        for each_node in self.all_conn_nodes:
            node_type = pm.nodeType(each_node)
            if node_type in self.IGNORE_NODES:
                continue
            if node_map_data.has_key(node_type):
                short_name = node_map_data[node_type]
            else:
                short_name = node_type
            new_node_name = custom_shader_name+"_"+short_name
            node = pm.PyNode(each_node)
            node.rename(new_node_name)
        
        self.addShader_to_ui()
        self.connectedListView.clear()

    def showDependencyNodes(self):
        self.connectedListView.clear()
        shader = self.shadersListView.currentItem().text()
        self.all_connected_nodes = pm.hyperShade(lun=shader)+pm.hyperShade(ldn=shader)+[shader]
        self.all_conn_nodes = [i for i in self.all_connected_nodes if pm.nodeType(i) not in self.IGNORE_NODES]
        self.connectedListView.addItems(self.all_conn_nodes)
        
    def addShader_to_ui(self):
        self.shadersListView.clear()
        all_shaders = self.getAllShaders()
        self.shadersListView.addItems(all_shaders)
        
    def getAllShaders(self):
		#returns all shaders in the scene. that's connected to a shading group.
        ignoreSg = ['initialParticleSE', 'initialShadingGroup']
        all_shaders = []
        shadingEngines = pm.ls(type="shadingEngine")
        for each_se in shadingEngines:
            if each_se.name() not in ignoreSg:
                shader = self.get_shader_from_engine(each_se)
                if shader:
                    all_shaders.append(shader.name())
        return all_shaders
		#stores all the child nodes for the shader
        

    def get_shader_from_engine(self, engine):
        surface_attr = engine.attr('surfaceShader')
        shaders = surface_attr.inputs()
        if shaders:
            return shaders[0]
        else:
            return None
        
        

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
