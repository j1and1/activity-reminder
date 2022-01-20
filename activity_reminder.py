import sys
import threading
import time
import datetime

from PySide6 import QtWidgets

from config import Config
from computervision import SquatDetector
from main_window import MainWindow

class ActivityReminder:

    def __init__(self, cfg, window):
        self.cfg = cfg
        self.window = window
        self.enabled = True

        self.time = cfg.time

        #self.sd = SquatDetector(self.cfg, self.frame_ready, self.on_detected)
        #self.sd.start()

        self.timer = threading.Thread(target=self.timer_loop)
        self.timer.start()

    def stop(self):
        #self.sd.stop()
        self.enabled = False

    def frame_ready(self, image):
        self.window.update_image(image)

    def on_detected(self, is_squating):
        pass

    def timer_loop(self):
        while self.enabled:
            while self.time > 0 and self.enabled:
                text = f'Time left:{datetime.timedelta(seconds=self.time)}'
                self.window.update_lable(text)
                time.sleep(1)
                self.time = self.time - 1

            text = 'Please do 20 squats'
            self.window.update_lable(text)
            time.sleep(60)

            self.time = self.cfg.time


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(True)

    cfg = Config()
    widget = MainWindow()
    widget.resize(200, 150)
    widget.show()

    #start timer and comunication logic
    reminder = ActivityReminder(cfg, widget)

    exit_code = app.exec()
    #stop timer and comunication logic
    reminder.stop()
    sys.exit(exit_code)