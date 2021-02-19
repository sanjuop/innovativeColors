import inspect
import os
import tempfile
import sys
import shutil
import subprocess

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QFile, QObject
import pymel.core as pm

import pipeline.CoreModules.common_utils as common_utils;reload(common_utils)
import QcConfig as QcConfig;reload(QcConfig)
import pipeline.PysideWidgets.dialogs as dialogs;reload(dialogs)
import pipeline.PysideWidgets.QcReport.QcReport as QcReport;reload(QcReport)
import pipeline.PysideWidgets.image_widget as image_widget;reload(image_widget)
import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
from pipeline.MayaTools.workspace_control import DockableUI
import file_explorer as file_explorer;reload(file_explorer)
import pipeline.Icons as icon

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
icon_dir = os.path.dirname(icon.__file__)


assets_path = r"T:\Batch01"

temp_dir = common_utils.temp_dir()

department_shot_name = {"Modeling":"Mo", "Texturing":"Tx"}

class AssetPublishTool(DockableUI):
    
    WINDOW_TITLE = "Asset Manager"

    ui_instance = None
    def __init__(self):
        super(AssetPublishTool, self).__init__()

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(300)

        # self.setWindowFlags(QtCore.Qt.Window)
        main_layout = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QHBoxLayout()
        
        toggle_lay = QtWidgets.QHBoxLayout()
        self.model_btn = QtWidgets.QRadioButton("Modeling")
        self.model_btn.setChecked(True)
        self.texture_btn = QtWidgets.QRadioButton("Texturing")
        toggle_lay.addWidget(self.model_btn)
        toggle_lay.addWidget(self.texture_btn)

        asset_lay = QtWidgets.QVBoxLayout()
        self.assets_label = QtWidgets.QLabel("Assets List")
        self.assets_list = QtWidgets.QListWidget()
        self.assets_list.setSortingEnabled(True)
        self.assets_list.setFixedWidth(80)
        self.thumbnail = self.image_thumbnail()
        
        self.assets_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.assets_list.customContextMenuRequested.connect(self.show_right_click)

        asset_lay.addWidget(self.thumbnail)
        asset_lay.addWidget(self.assets_label)
        asset_lay.addWidget(self.assets_list)

        self.tab1 = QtWidgets.QWidget()

        # Create first tab
        self.tab1.layout = QtWidgets.QHBoxLayout(self)
        self.qc_lay = QtWidgets.QVBoxLayout()
        self.qc_list = QtWidgets.QListWidget()
        self.qc_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.all_qc_btn = QtWidgets.QPushButton("Run all QC's")
        
        self.qc_lay.addLayout(toggle_lay)
        self.qc_lay.addWidget(self.qc_list)
        self.qc_lay.addWidget(self.all_qc_btn)
        self.tab1.layout.addLayout(self.qc_lay)
        self.tab1.setLayout(self.tab1.layout)

        # self.layout.addLayout(toggle_lay)
        self.layout.addLayout(asset_lay)
        self.layout.addWidget(self.tab1)

        self.file_explorer = file_explorer.FileExplorerDialog()
        main_layout.addLayout(self.layout)
        main_layout.addWidget(self.file_explorer)
        
        self.setLayout(main_layout)

        self.apply_darkOrange_style()

        self.model_btn.clicked.connect(lambda: self.populate_qc_list("modeling", False))
        self.texture_btn.clicked.connect(lambda: self.populate_qc_list("texturing", False))
        
        self.populate_assets_list()
        self.populate_qc_list("modeling", True)

        self.qc_list.itemDoubleClicked.connect(self.execute_selced_qc)
        self.all_qc_btn.clicked.connect(self.run_all_Qc)
        self.assets_list.itemSelectionChanged.connect(self.toggle_thumbnail)
        self.assets_list.itemSelectionChanged.connect(self.toggle_folder_structure)
        self.label.double_click.connect(self.open_image)

    def toggle_folder_structure(self):
        selected_item = self.assets_list.currentItem().text()
        asset_path = os.path.join(assets_path, selected_item, "_Maya")
        self.file_explorer.refresh_list(asset_path)

    def open_image(self):
        image_path = self.label.get_image
        xn_view = common_utils.xn_view_path
        if os.path.exists(xn_view):
            command = '"{}" "{}"'.format(common_utils.xn_view_path , image_path)
            subprocess.call(command)

    def toggle_thumbnail(self):
        selected_item = self.assets_list.currentItem().text()
        asset_path = os.path.join(assets_path, selected_item)
        ref_images = [os.path.join(root, each_file) for root, dir, file1 in os.walk(asset_path) for each_file in file1 if 'REF' in each_file]
        if ref_images:
            ref_images = ref_images[0]
        else:
            ref_images = '{}/Default.jpg'.format(current_directory)
        
        self.label.set_image(ref_images)

    def image_thumbnail(self):
        self.label = image_widget.CustomImageWidget(80, 80,'{}/Default.jpg'.format(current_directory))
        return self.label

    def populate_assets_list(self):
        all_assets_list = os.listdir(assets_path)
        self.assets_list.addItems(all_assets_list)

    def get_asset_publish_path(self, asset_name, department):
        dept_shot_name = department_shot_name[department]
        asset_name = maya_wrappers.getBaseName()
        asset_path = os.path.join(assets_path, asset_name, "_Maya", dept_shot_name, asset_name+".fbx")
        return asset_path


    def file_publised(self):
        asset_name = maya_wrappers.getBaseName()
        asset_path = self.get_asset_publish_path(asset_name, "Modeling")
        if os.path.exists(asset_path):
            return True
        return False

    def populate_qc_list(self, department, default=True):
        if not default:
            if not self.file_publised():
                self.model_btn.setChecked(True)
                dialogs.message("massage", "Modeling not published", "Modeling not published, You cannont do texturing Qc")
                return
        self.qc_list.clear()
        qc_list = eval('QcConfig.{}_qc_list'.format(department))
        self.qc_list.addItems(qc_list)

    def apply_darkOrange_style(self):
        style = open('{}/darkorange.css'.format(current_directory) , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def show_right_click(self, pos):
        item = self.assets_list.itemAt(pos)
        if not item:
            return
        
        context_menu = QtWidgets.QMenu()
        font = QtGui.QFont()
        font.setBold(True)
        context_menu.setFont(font)

        template_creation = QtWidgets.QAction("Create Template", self)
        template_creation.triggered.connect(self.create_template)
        context_menu.addAction(template_creation)

        context_menu.addSeparator()

        open_folder = QtWidgets.QAction("Open Folder", self)
        open_folder.triggered.connect(self.show_in_folder)
        context_menu.addAction(open_folder)

        context_menu.exec_(QtGui.QCursor.pos())

    def get_selected_asset(self):
        selected_asset = self.assets_list.currentItem().text()
        return selected_asset

    def create_template(self):
        selected_asset = self.get_selected_asset()
        asset_path = os.path.join(temp_dir, selected_asset)
        asset_full_path = "{}/{}".format(asset_path, selected_asset)
        if os.path.exists(asset_path):
            message = "This Template already exists, Do you want to create new?"
            result = dialogs.warning("warning", "Template exists", message)
            if result:
                shutil.rmtree(asset_path)
                os.makedirs(asset_path)
                maya_wrappers.save_file_as(asset_full_path)
        else:
            os.makedirs(asset_path)
            maya_wrappers.save_file_as(asset_full_path)
        
    def show_in_folder(self):
        selected_asset = self.get_selected_asset()
        asset_path = os.path.join(assets_path, selected_asset)
        os.startfile(asset_path)

    def execute_selced_qc(self):
        execute_selced_qc = [each_qc.text() for each_qc in self.qc_list.selectedItems()]
        error_list = self.run_qc_func(execute_selced_qc) 
        
        if error_list:
            qc_report = QcReport.QcReport(error_list)
            qc_report.exec_()
            return

    def run_qc_func(self, qc_list):
        error_list = []
        for each_qc in qc_list:
            result = eval("QcConfig.{}()".format(each_qc))
            print "each_qc", each_qc
            if not result is True:
                result["error_title"] = each_qc
                error_list.append(result)
        return error_list
    
    def run_all_Qc(self):
        itemsTextList =  [str(self.qc_list.item(i).text()) for i in range(self.qc_list.count())]
        error_list = self.run_qc_func(itemsTextList)
        
        if error_list:
            qc_report = QcReport.QcReport(error_list, parent=None)
            qc_report.exec_()
            return

        self.publish_btn = QtWidgets.QPushButton("Publish")
        self.publish_btn.clicked.connect(self.publishData)
        self.qc_lay.addWidget(self.publish_btn)
        

    
    def publishData(self):
        itemsTextList =  [str(self.qc_list.item(i).text()) for i in range(self.qc_list.count())]
        error_list = self.run_qc_func(itemsTextList)
        
        if error_list:
            publish_btn_index = self.qc_lay.indexOf(self.publish_btn)
            item = self.qc_lay.takeAt(publish_btn_index)
            w = item.widget()
            w.deleteLater()
            qc_report = QcReport.QcReport(error_list, parent=None)
            qc_report.exec_()
            return

        asset_name = maya_wrappers.getBaseName()
        if self.model_btn.isChecked():
            dept = self.model_btn.text()
        elif self.texture_btn.isChecked():
            dept = self.texture_btn.text()

        publish_path = self.get_asset_publish_path(asset_name, dept)

        main_node = maya_wrappers.get_assembly_nodes()[0]
        pm.select(main_node)
        local_File_path = os.path.join(common_utils.temp_dir(), asset_name+".fbx")
        if os.path.exists(local_File_path):
            os.remove(local_File_path)
        pm.mel.FBXExport(f=local_File_path, s=True)
        common_utils.copy_to_server(local_File_path, publish_path)
        os.remove(local_File_path)
        dialogs.message("massage", "file published", "File published, {}".format(dept))

        
def main():

    workspace_control_name = AssetPublishTool.get_workspace_control_name()
    if pm.window(workspace_control_name, exists=True):
        pm.deleteUI(workspace_control_name)

    AssetPublishTool.module_name_override = "dockable_assetmanager"
    AssetPublishTool()

# import sys
# ___path = r"E:\InnovativeColors\MayaToMax"
# if ___path not in sys.path:
#     sys.path.append(___path)
# import AssetPublishTool as AssetPublishTool;reload(AssetPublishTool)
# ui=AssetPublishTool.AssetPublishTool()
# ui.show()
