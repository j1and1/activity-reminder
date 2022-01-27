import json
from os import name

class Config(object):

    def __init__(self, filePath = "config.json"):
        self.file_path = filePath
        self.cfg = {}
        if len(self.file_path) > 0:
            try:
                self.read_config()
            except:
                #aditionally load error
                self.create_empty()
        else:
            self.create_empty()

    @property
    def port(self):
        return self.cfg["port"]

    @property
    def baud(self):
        return self.cfg["baud"]
    
    @property
    def time(self):
        return self.cfg["time"] * 60

    @property
    def allowed_skips(self):
        return self.cfg["allowed_skips"]

    @property
    def camera(self):
        return self.cfg["camera"]

    @property
    def squat_count(self):
        return self.cfg["squats"]

    @property
    def precision(self):
        return self.cfg["precision"]

    def create_empty(self):
        self.cfg = {}
        self.cfg["port"] = "COM3"
        self.cfg["baud"] = 9600 
        self.cfg["time"] = 45 # default time in minutes
        self.cfg["camera"] = 0

        self.cfg["squats"] = 20
        self.cfg["allowed_skips"] = 2
        self.cfg["precision"] = 0.55

    def write_config(self):
        with open(self.file_path, 'w') as config_file:
            json.dump(self.cfg, config_file, indent = 4, sort_keys = True)

    def read_config(self):
        with open(self.file_path) as config_file:
            self.cfg = json.load(config_file)
        
if __name__ == '__main__':
    config = Config()
    config.write_config()