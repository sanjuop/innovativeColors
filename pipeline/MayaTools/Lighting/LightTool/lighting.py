import json
import os
import re
import shutil

import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya_wrapper as maya_wrapper;reload(maya_wrapper)
import lighting_wrapper as lighting_wrapper;reload(lighting_wrapper)
import config as config;reload(config)
import utility as utility;reload(utility)
import dialogue as dialogue;reload(dialogue)
import layer_setup as layer_setup;reload(layer_setup)
import objectProperties as objectProperties;reload(objectProperties)


class LightWidget(QtWidgets.QTabWidget):

    def __init__(self, parent = None):
        super(LightWidget, self).__init__(parent=parent)

        self.setObjectName("lightingtool")

        print "@28",pm.window("lightingtool",q=True, ex=True)

        self.setWindowTitle("Lighting Tool")
        self.setObjectName("lightingTool")
        self.setWindowFlags(QtCore.Qt.Window)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        self.tab1 = Analyse()
        self.tab2 = shotLighting()

        self.addTab(self.tab1, "Analyse")
        self.addTab(self.tab2, "shot Lighting")
        
        print "@44"
        
        self.all_references = maya_wrapper.list_references()
        
        self.tab1.pre_analyse.clicked.connect(self.pre_analyse_process)
        
        self.tab1.int_mesh.clicked.connect(lighting_wrapper.define_interaction_mesh)
        
        print '@51'
        
        self.tab1.master.clicked.connect(self.analyse_process)
        
        self.tab1.ch_list.itemClicked.connect(self.select_meshes_in_maya)
        
        self.tab2.bg_bty.clicked.connect(layer_setup.bg_bty)
        # self.tab2.bg_utility.clicked.connect(layer_setup.bg_utility)
        self.tab2.ch_bty.clicked.connect(layer_setup.ch_bty)
        self.tab2.ch_utility.clicked.connect(layer_setup.ch_utility)
        self.tab2.ch_Line.clicked.connect(layer_setup.ch_Line)
        print "@62"
        self.tab2.save_btn.clicked.connect(layer_setup.save_file_to_server)
        print "@65"
        maya_wrapper.load_render_globals()
        
        maya_wrapper.update_camera()
        
        maya_wrapper.update_frame_range()
        
        print "@66"
    def add_assets_ui(self):
        self.all_references = maya_wrapper.list_references()
        if self.tab1.bg_list.invisibleRootItem().childCount() == 0 and self.tab1.ch_list.invisibleRootItem().childCount() == 0:
            for each_ref in self.all_references.values():
                ref_path = each_ref.path
                if "cam" in ref_path:
                    continue
                asset_type = ref_path.split("/")[4]
                name_space = asset_type+":"+each_ref.namespace
                parent = QtWidgets.QTreeWidgetItem()
                parent.setText(0, name_space)
                if asset_type == "set":
                    self.tab1.bg_list.insertTopLevelItem(0,parent)
                else:
                    self.tab1.ch_list.insertTopLevelItem(0,parent)
                
    def select_meshes_in_maya(self):
        selected_item = self.tab1.ch_list.selectedItems()[0].text(0).split(":")[1]
        all_nodes = pm.ls(self.all_references[selected_item].nodes(), type="mesh")
        pm.select(all_nodes)
        
    def get_assets_hierarchy(self):
        assets_hierarchy = {"BG": {}, "CHAR":{}}
        root1 = self.tab1.bg_list
        root2 = self.tab1.ch_list
        for each_root in [root1,root2]:
            main_root = each_root.invisibleRootItem()
            for index in range(0, main_root.childCount()):
                parent = each_root.topLevelItem(index)
                if each_root == root1:
                    asset_type = "BG"
                elif each_root == root2:
                    asset_type = "CHAR"
                assets_hierarchy[asset_type][parent.text(0).split(":")[1]] = [parent.text(0).split(":")[1]]
                child_count = parent.childCount()
                if child_count > 0:
                    for each_child in xrange(child_count):
                        children = parent.child(each_child)
                        assets_hierarchy[asset_type][parent.text(0).split(":")[1]].append(children.text(0).split(":")[1])
        return assets_hierarchy
        
    def pre_analyse_process(self):
        self.all_references = self.all_references.values()
        for each_refs in self.all_references:
            old_path = each_refs.path
            pattern = re.search(config.replace_from,old_path)
            if pattern:
                old_path = re.sub(config.replace_from,config.replace_to,old_path)
                try:
                    each_refs.replaceWith(old_path)
                except Exception as error:
                    print str(error) + "__:__" + old_path
        
        self.add_assets_ui()
        self.add_light_rigs_to_ui()
        
    def add_light_rigs_to_ui(self):
        light_rig_path = [each_lg for each_lg in os.listdir(config.bg_preset_path)]
        self.tab1.light_rig.addItems(light_rig_path)
    
    def analyse_process(self):
        if not pm.objExists("interaction_mesh_set"):
            pm.confirmDialog(m="interaction_mesh not defined",b="Ok")
            return

        if self.tab1.light_rig.currentText() == "Select Light rig":
            pm.confirmDialog(m="Light rig not selected", b="Ok")
            return

        # Export interaction mesh
        # lighting_wrapper.export_interaction_meshes()

        # store asset hierarchy and light_rig name in json
        final_data = {}
        selected_light_rig = self.tab1.light_rig.currentText()
        assets_hierarchy = self.get_assets_hierarchy()
        final_data["light_rig_name"] = selected_light_rig
        final_data["assets_hierarchy"] = assets_hierarchy
        print "assets_hierarchy", assets_hierarchy
        # return
        # create sets and rs_op
        print "@148",self.all_references
        for each_asset_type in assets_hierarchy:
            for each_asset in assets_hierarchy[each_asset_type]:
                asset_obj = self.all_references[each_asset]
                meshes = maya_wrapper.get_meshes_from_top_group(asset_obj, fp=True)
                if each_asset_type == "BG":
                    meshes = meshes + [i.name() for i in pm.ls(type="instancer")]
                face_geos = [each_mesh for each_mesh in meshes if re.search(config.face_mesh_pattern, each_mesh)]
                if face_geos:
                    for each_face_mesh in face_geos:
                        if each_face_mesh in meshes:
                            meshes.remove(each_face_mesh)
                set_name = each_asset+"_"+each_asset_type
                pm.select(meshes)
                pm.sets(n=set_name)
                pm.select(cl=1)
                objectProperties.create_rs_obj_pro_node(0, set_name, meshes, enable=1)
                objectProperties.create_rs_obj_pro_node(1, set_name, meshes, enable=1)
                objectProperties.create_rs_obj_pro_node(3, set_name, meshes, enable=0)
                if each_asset_type == "CHAR":
                    smooth = objectProperties.create_rs_obj_pro_node(2, set_name, meshes, enable=1)
                    smooth.attr("maxTessellationSubdivs").set(2)

                if face_geos:
                    face_geo_set_name = each_asset + "_" + each_asset_type + "_face_geos"
                    pm.select(face_geos)
                    pm.sets(n=face_geo_set_name)
                    pm.select(cl=1)

        #publish IDs
        lighting_wrapper.publish_id(self.all_references, assets_hierarchy)

        #select default render layer
        maya_wrapper.set_default_render_layer()

        # save the file to local and paste a backUp of same file to server
        shot_details = maya_wrapper.get_scene_details_from_scene_name()
        ep = shot_details[0]
        seq = shot_details[1]
        shot = shot_details[2]
        shot_name = shot_details[3]
        local_path = os.path.join(config.maya_temp_path, shot_name)
        master_file_name = config.PRJCODE+"_"+shot_name
        maya_wrapper.save_scene_as(local_path, master_file_name)

        shot_lighting_path = os.path.join(config.get_shot_path(ep, seq, shot), "lighting")
        if not os.path.exists(shot_lighting_path):
            os.makedirs(shot_lighting_path)
        basename = maya_wrapper.get_scene_name(basename=True)
        shutil.copy2(os.path.join(local_path,basename),shot_lighting_path)

        # export json_file to shot directory
        json_file_name = ep+"_"+seq+"_"+shot+"_"+"shot_Data.json"
        json_path = os.path.join(shot_lighting_path, json_file_name)
        utility.write_json_file(json_path, final_data)



        dialogue.message("message", config.PRJCODE, "Masterfile successfully created")


class Analyse(QtWidgets.QWidget):
    def __init__(self):
        super(Analyse, self).__init__()

        analyse_lay = QtWidgets.QVBoxLayout()
        self.setLayout(analyse_lay)

        self.pre_analyse = QtWidgets.QPushButton("Pre-Analyse")
        self.int_mesh = QtWidgets.QPushButton("Define interaction Mesh")

        self.light_rig = QtWidgets.QComboBox()
        self.light_rig.addItem("Select Light rig")

        self.bg_list = QtWidgets.QTreeWidget()
        self.bg_list.setHeaderLabel("BG")
        self.bg_list.setDragEnabled(True)
        self.bg_list.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.bg_list.setAlternatingRowColors(True)
        self.bg_list.setObjectName("bg_list")

        self.ch_list = QtWidgets.QTreeWidget()
        self.ch_list.setHeaderLabel("CH")
        self.ch_list.setDragEnabled(True)
        self.ch_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.ch_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.ch_list.setAlternatingRowColors(True)
        self.ch_list.setObjectName("bg_list")

        self.master = QtWidgets.QPushButton("Create Master File")

        analyse_lay.addWidget(self.pre_analyse)
        analyse_lay.addWidget(self.int_mesh)
        analyse_lay.addWidget(self.light_rig)
        analyse_lay.addWidget(self.bg_list)
        analyse_lay.addWidget(self.ch_list)
        analyse_lay.addWidget(self.master)


class shotLighting(QtWidgets.QWidget):
    def __init__(self):
        super(shotLighting, self).__init__()

        shot_light_lay = QtWidgets.QVBoxLayout()
        self.setLayout(shot_light_lay)

        btn_lay = QtWidgets.QHBoxLayout()

        self.bg_bty = QtWidgets.QPushButton("BG_BTY")
        self.bg_fog = QtWidgets.QPushButton("BG_Fog")

        self.ch_bty = QtWidgets.QPushButton("CH_BTY")
        self.ch_utility = QtWidgets.QPushButton("CH_Utility")
        
        self.ch_Line = QtWidgets.QPushButton("CH_Line")


        bg_lay = QtWidgets.QVBoxLayout()
        bg_lay.addWidget(self.bg_bty)
        bg_lay.addWidget(self.bg_fog)

        ch_lay = QtWidgets.QVBoxLayout()
        ch_lay.addWidget(self.ch_bty)
        ch_lay.addWidget(self.ch_utility)
        ch_lay.addWidget(self.ch_Line)
        

        btn_lay.addLayout(bg_lay)
        btn_lay.addLayout(ch_lay)

        self.save_btn = QtWidgets.QPushButton("save to server")
        shot_light_lay.addLayout(btn_lay)
        shot_light_lay.addWidget(self.save_btn)



dlg = None


def main():
    global dlg
    if dlg is None:
        dlg = LightWidget(parent=maya_wrapper.maya_main_window())
    dlg.show()
    
    
    
"""
import sys
base_path = r"Q:\pipeline\pipeline_new"
if base_path not in sys.path:
    sys.path.append(base_path)
import lighting as lighting;reload(lighting)
lighting.main()
"""