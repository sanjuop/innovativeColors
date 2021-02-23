import os
import shutil

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import pymel.core as pm

import pipeline.CoreModules.common.common_utils as common_utils;reload(common_utils)
import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
import pipeline.PysideWidgets.dialogs as dialogs;reload(dialogs)

temp_dir = common_utils.temp_dir()

class FileExplorerDialog(QtWidgets.QDialog):

    def __init__(self):
        super(FileExplorerDialog, self).__init__()

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.tree_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_wdg.customContextMenuRequested.connect(self.show_context_menu)

    def create_actions(self):
        self.show_in_folder_action = QtWidgets.QAction("Show in Folder", self)
        self.open_in_local_action = QtWidgets.QAction("Open in Local", self)
        self.open_from_server_action = QtWidgets.QAction("Open from server", self)
        self.refer_asset_action = QtWidgets.QAction("Refer asset", self)

    def create_widgets(self):
        self.tree_wdg = QtWidgets.QTreeWidget()
        self.tree_wdg.setHeaderLabel("Published Files")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addWidget(self.tree_wdg)

    def create_connections(self):
        self.show_in_folder_action.triggered.connect(self.show_in_folder)
        self.open_in_local_action.triggered.connect(self.open_in_local)
        self.open_from_server_action.triggered.connect(self.open_from_server)
        self.refer_asset_action.triggered.connect(self.refer_asset)

    def refresh_list(self, DIRECTORY_PATH):
        self.tree_wdg.clear()
        self.add_children(None, DIRECTORY_PATH)

    def add_children(self, parent_item, dir_path):
        directory = QtCore.QDir(dir_path)
        files_in_directory = directory.entryList(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries, QtCore.QDir.DirsFirst | QtCore.QDir.IgnoreCase)

        for file_name in files_in_directory:
            self.add_child(parent_item, dir_path, file_name)


    def add_child(self, parent_item, dir_path, file_name):
        file_path = "{0}/{1}".format(dir_path, file_name)
        file_info = QtCore.QFileInfo(file_path)

        item = QtWidgets.QTreeWidgetItem(parent_item, [file_name])
        item.setIcon(0, QtGui.QIcon(':mayaIcon.png'))
        item.setData(0, QtCore.Qt.UserRole, file_path)

        if file_info.isDir():
            item.setIcon(0, QtGui.QIcon(':folder-open.png'))
            self.add_children(item, file_info.absoluteFilePath())

        if not parent_item:
            self.tree_wdg.addTopLevelItem(item)

    def show_context_menu(self, pos):
        item = self.tree_wdg.itemAt(pos)
        if not item:
            return
        
        file_path = item.data(0, QtCore.Qt.UserRole)
        file_info = QtCore.QFileInfo(file_path)
        self.show_in_folder_action.setData(file_path)

        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.show_in_folder_action)
        if not file_info.isDir():
            context_menu.addAction(self.open_in_local_action)
            context_menu.addAction(self.open_from_server_action)
            context_menu.addAction(self.refer_asset_action)
        context_menu.exec_(self.tree_wdg.mapToGlobal(pos))


    def show_in_folder(self):
        file_path = self.show_in_folder_action.data()
        
        if self.open_in_explorer(file_path):
            return

    def open_in_explorer(self, file_path):
        # Windows specific implementation
        file_info = QtCore.QFileInfo(file_path)
        args = []
        if not file_info.isDir():
            args.append("/select,")

        args.append(QtCore.QDir.toNativeSeparators(file_path))

        if QtCore.QProcess.startDetached("explorer", args):
            return True

        return False

    def open_in_local(self):
        file_path = self.show_in_folder_action.data()
        maya_file_path = file_path.replace(".fbx", ".ma")
        asset_name = os.path.splitext(os.path.basename(maya_file_path))[0]
        asset_path = os.path.join(temp_dir, asset_name, os.path.basename(maya_file_path))
        dir_name = os.path.dirname(asset_path)
        if os.path.exists(asset_path):
            message = "File already exists, Do you want to overwrite?"
            result = dialogs.warning("warning", "file exists", message)
            if result:
                shutil.rmtree(dir_name)
                os.makedirs(dir_name)
                # shutil.copy2(file_path, dir_name)
                pm.newFile(force=True)
                maya_wrappers.save_file_as(asset_path)
                maya_wrappers.import_file(file_path)
                maya_wrappers.save_file()
                
        else:
            try:
                os.makedirs(dir_name)
            except:
                pass
            # shutil.copy2(file_path, dir_name)
            maya_wrappers.saveFile(asset_path)
            maya_wrappers.import_file(file_path)
            maya_wrappers.save_file()
    
    def open_from_server(self):
        file_path = self.show_in_folder_action.data()
        maya_wrappers.open_file(file_path)

    def refer_asset(self):
        file_path = self.show_in_folder_action.data()
        maya_wrappers.refer_file(file_path)




if __name__ == "__main__":

    try:
        my_dialog.close() # pylint: disable=E0601
        my_dialog.deleteLater()
    except:
        pass

    my_dialog = FileExplorerDialog()
    my_dialog.show()