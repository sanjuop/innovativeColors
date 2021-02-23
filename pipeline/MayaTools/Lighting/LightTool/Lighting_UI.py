# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Q:\pipeline\scripts\Lighting_UI.ui',
# licensing of 'Q:\pipeline\scripts\Lighting_UI.ui' applies.
#
# Created: Wed Aug  7 08:11:46 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(278, 561)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Pre_analyse = QtWidgets.QPushButton(self.tab)
        self.Pre_analyse.setObjectName("Pre_analyse")
        self.verticalLayout.addWidget(self.Pre_analyse)
        self.int_mesh = QtWidgets.QPushButton(self.tab)
        self.int_mesh.setObjectName("int_mesh")
        self.verticalLayout.addWidget(self.int_mesh)
        self.light_rig = QtWidgets.QComboBox(self.tab)
        self.light_rig.setObjectName("light_rig")
        self.light_rig.addItem("")
        self.verticalLayout.addWidget(self.light_rig)
        self.bg_list = QtWidgets.QListWidget(self.tab)
        self.bg_list.setObjectName("bg_list")
        QtWidgets.QListWidgetItem(self.bg_list)
        self.verticalLayout.addWidget(self.bg_list)
        self.CH_list = QtWidgets.QListWidget(self.tab)
        self.CH_list.setObjectName("CH_list")
        QtWidgets.QListWidgetItem(self.CH_list)
        self.verticalLayout.addWidget(self.CH_list)
        self.create_master = QtWidgets.QPushButton(self.tab)
        self.create_master.setObjectName("create_master")
        self.verticalLayout.addWidget(self.create_master)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.BG_BTY = QtWidgets.QPushButton(self.tab_2)
        self.BG_BTY.setObjectName("BG_BTY")
        self.verticalLayout_2.addWidget(self.BG_BTY)
        self.BG_UTILITY = QtWidgets.QPushButton(self.tab_2)
        self.BG_UTILITY.setObjectName("BG_UTILITY")
        self.verticalLayout_2.addWidget(self.BG_UTILITY)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.CH_BTY = QtWidgets.QPushButton(self.tab_2)
        self.CH_BTY.setObjectName("CH_BTY")
        self.verticalLayout_5.addWidget(self.CH_BTY)
        self.CH_UTILITY = QtWidgets.QPushButton(self.tab_2)
        self.CH_UTILITY.setObjectName("CH_UTILITY")
        self.verticalLayout_5.addWidget(self.CH_UTILITY)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Lightig Tool", None, -1))
        self.Pre_analyse.setText(QtWidgets.QApplication.translate("Dialog", "Pre-analyse", None, -1))
        self.int_mesh.setText(QtWidgets.QApplication.translate("Dialog", "Interaction mesh", None, -1))
        self.light_rig.setItemText(0, QtWidgets.QApplication.translate("Dialog", "SelectLightRig", None, -1))
        self.bg_list.item(1).setText(QtWidgets.QApplication.translate("Dialog", "BG", None, -1))
        self.CH_list.item(2).setText(QtWidgets.QApplication.translate("Dialog", "CH", None, -1))
        self.create_master.setText(QtWidgets.QApplication.translate("Dialog", "Create Maseter File", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("Dialog", "Analyse", None, -1))
        self.BG_BTY.setText(QtWidgets.QApplication.translate("Dialog", "BG_BTY", None, -1))
        self.BG_UTILITY.setText(QtWidgets.QApplication.translate("Dialog", "BG_UTILITY", None, -1))
        self.CH_BTY.setText(QtWidgets.QApplication.translate("Dialog", "CH_BTY", None, -1))
        self.CH_UTILITY.setText(QtWidgets.QApplication.translate("Dialog", "CH_UTILITY", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("Dialog", "shot lighting", None, -1))

