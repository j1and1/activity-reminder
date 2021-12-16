import sys
import threading
import time
import datetime
from PySide6 import QtCore, QtWidgets, QtGui

from config import Config

class MainWindow(QtWidgets.QWidget):

    def __init__(self, cfg):
        super().__init__()

        self.time = cfg.time
        self.enabled = True

        self.button = QtWidgets.QPushButton("Stop")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.text.setFont(QtGui.QFont('Arial', 24))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.kill_timer)
        
        self.timer = threading.Thread(target=self.timer_loop)
        self.timer.start()

    @QtCore.Slot()
    def kill_timer(self):
        self.enabled = False

    def timer_loop(self):
        while self.enabled:
            while self.time > 0 and self.enabled:
                self.text.setText(f'Time left:{datetime.timedelta(seconds=self.time)}')
                time.sleep(1)
                self.time = self.time - 1

            self.text.setText('Please do 20 squats')
            time.sleep(60)

            self.time = cfg.time


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    cfg = Config()
    widget = MainWindow(cfg)

    widget.resize(200, 150)
    widget.show()

    sys.exit(app.exec())