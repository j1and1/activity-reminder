from operator import contains
import sys
import threading
import time
import datetime

from PySide6 import QtWidgets

from config import Config
from communication import Communication
from computervision import SquatDetector
from main_window import MainWindow

class ActivityReminder:

    def __init__(self, cfg, window):
        self.cfg = cfg
        self.window = window
        self.enabled = True
        self.times_paused = 0
        self.time = cfg.time

        # initialise computervision and serial port
        self.sd = SquatDetector(self.cfg, self.frame_ready, self.on_detected)
        self.communication = Communication(cfg, self.on_serial_data)
        
        self.timer = threading.Thread(target=self.timer_loop)
        self.timer.start()

    def on_serial_data(self, data):
        print(str(data))
        if "msg" in data and data["msg"] == "button" and self.squats_needed > 0:
            if self.cfg.allowed_skips > self.times_paused:
                self.times_paused = self.times_paused + 1
                self.squats_needed = 0
                self.sd.stop()
                self.update_device_state(False)
                self.frame_ready(None)
            else:
                print("Can't pause anymore... do squats pls")

    def stop(self):
        self.sd.stop()
        self.enabled = False

    def frame_ready(self, image):
        self.window.update_image(image)

    def on_detected(self, is_squating, angle):
        if is_squating and not self.is_squatting:
            self.is_squatting = is_squating
            self.squats_needed = self.squats_needed - 1
            self.update_lable()
        elif not is_squating and self.is_squatting:
            self.is_squatting = is_squating

        if self.squats_needed == 0:
            self.sd.stop()
            self.update_device_state(False)
            self.frame_ready(None)

    def update_lable(self):
        text = f"Please do {self.squats_needed} squats"
        self.window.update_lable(text)

    def update_device_state(self, state):
        data = {}
        data["msg"] = state
        self.communication.send_data(data)

    def timer_loop(self):
        while self.enabled:
            while self.time > 0 and self.enabled:
                text = f'Time left:{datetime.timedelta(seconds=self.time)}'
                self.window.update_lable(text)
                time.sleep(1)
                self.time = self.time - 1

            if not self.enabled:
                return

            self.squats_needed = cfg.squat_count + self.times_paused * cfg.squat_count / 2
            self.is_squatting = False
            self.update_lable()
            self.update_device_state(True)
            # start computervision
            self.sd.start()
            # wait till computervision is stopped
            self.sd.wait()

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