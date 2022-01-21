import threading
import json
from serial import Serial

class Communication(object):

    def __init__(self, cfg, callback):
        self._callbacks = []
        self._callbacks.append(callback)
        self._running = True
        self._cv = threading.Condition()
        self._thread = threading.Thread(target = self.main_loop)
        self._serial = Serial(cfg.port, cfg.baud, timeout = 20)
        self._thread.start()

    def add_calback(self, callback):
        self._callbacks.append(callback)

    def stop(self):
        self._running = False
        with self._cv:
            self._cv.notifyAll()

    def main_loop(self):
        while self._running:
            if not self._running:
                return

            try:
                data = self._serial.readline()
                data = json.loads(data)
                for fn in self._callbacks:
                    fn(data)
            except Exception as e:
                #print (str(e))
                pass

    def send_data(self, data):
        # append newline and send data
        data = json.dumps(data)
        self._serial.write(f"{data}\n".encode())
        self._serial.flush()