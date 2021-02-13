from PySide2 import QtWidgets, QtCore, QtGui

class CustomImageWidget(QtWidgets.QWidget):

    double_click = QtCore.Signal()

    def __init__(self, width, height, image_path, parent=None):
        super(CustomImageWidget, self).__init__(parent)

        self.set_size(width, height)
        self.set_image(image_path)
        self.set_background_color(QtCore.Qt.black)

    def mouseDoubleClickEvent(self, event):
        super(CustomImageWidget, self).mouseDoubleClickEvent(event)
        self.double_click.emit()

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    @property
    def get_image(self):
        return self.image_file_path

    def set_image(self, image_path):
        self.image_file_path = image_path
        image = QtGui.QImage(image_path)
        image = image.scaled(self.width(), self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(image)

        self.update()

    def set_background_color(self, color):
        self.background_color = color

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.fillRect(0, 0, self.width(), self.height(), self.background_color)
        painter.drawPixmap(self.rect(), self.pixmap)