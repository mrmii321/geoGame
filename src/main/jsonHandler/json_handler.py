import json


class JsonHandler:

    def __init__(self):
        self.file_path = r"C:\Users\noahf\Desktop\Development\Python\geoGame\src\main\objects.json"
        self.data = None
        self.load_json()
    

    def load_json(self):
        with open(self.file_path) as f:
            self.data = json.load(f)
        

    def get_data(self):
        return self.data


    def get_json(self, platform, surface, level):
        with open(self.file_path) as f:
            data = json.load(f)
            for plat in data[level]:  # the level is based on what nested list in the json file is used
                platforms.append(
                    Platform(plat["x"], plat["y"], plat["width"], plat["height"])
                )
        for plat in self.platforms:
            plat.draw(surface, self.camera_x)
