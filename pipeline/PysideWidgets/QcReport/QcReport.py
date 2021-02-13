import sys

from PySide2 import QtWidgets, QtCore, QtGui

import FrameLayout

class QcReport(QtWidgets.QDialog):
    def __init__(self, errors_list, parent=None):
        super(QcReport, self).__init__(parent=None)
        self.errors_list = errors_list
        self.initUI()

    def initUI(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumWidth(450)
        self.setWindowTitle("Error Report")

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(5,5,5,5)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)

        self.interp_layout = QtWidgets.QVBoxLayout()
        self.interp_layout.setContentsMargins(0,0,0,0)
        self.interp_layout.setSpacing(0)
        self.interp_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addLayout(self.interp_layout)
        
        for each_error in self.errors_list:
            object = self.initTitle(each_error["error_title"], each_error["error_message"])
            self.interp_layout.addWidget(object)

    def initTitle(self, errot_title=None, error_content=None):
        t = FrameLayout.FrameLayout(title=errot_title)
        self._title = QtWidgets.QLabel(error_content)
        self._title.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        t.addWidget(self._title)
        return t

def main():
    error_list = [{"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"},
                        {"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"},
                        {"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"},
                        {"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"},
                        {"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"},
                        {"error_title":"Name is wrong", "error_message":"File naming is not proper"},
                        {"error_title":"you are wrong", "error_message":"you are not proper"} ]
    app = QtWidgets.QApplication(sys.argv)
    window = QcReport(error_list)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()