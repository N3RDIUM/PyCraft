from terrain.block import *

class _block(Block):
    def __init__(self, data):
        data["name"] = "grass"
        super().__init__(data)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("grass"),
            "bottom": self.texture_manager.get_texture("dirt"),
            "left": self.texture_manager.get_texture("grass_side"),
            "right": self.texture_manager.get_texture("grass_side"),
            "front": self.texture_manager.get_texture("grass_side"),
            "back": self.texture_manager.get_texture("grass_side"),
        }