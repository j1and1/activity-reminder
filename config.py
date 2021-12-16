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

    def create_empty(self):
        self.cfg = {}
        self.cfg["port"] = "COM1"
        self.cfg["baud"] = 9600 
        self.cfg["time"] = 45 # default time in minutes
        self.cfg["allowed_skips"] = 3

    def write_config(self):
        with open(self.file_path, 'w') as config_file:
            json.dump(self.cfg, config_file, indent = 4, sort_keys = True)

    def read_config(self):
        with open(self.file_path) as config_file:
            self.cfg = json.load(config_file)
        
if __name__ == '__main__':
    config = Config()
    config.write_config()