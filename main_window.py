import sys
from PySide6 import QtCore, QtWidgets, QtGui

from config import Config

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Activity reminder")

        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.text.setFont(QtGui.QFont('Arial', 24))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)

        self.image_frame = QtWidgets.QLabel()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    def update_image(self, image):
        self.image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def update_lable(self, text):
        self.text.setText(text)