from terrain.block import *

class _block(Block):
    def __init__(self, data, id):
        data["name"] = "water"
        super().__init__(data, id)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("water"),
            "bottom": self.texture_manager.get_texture("water"),
            "left": self.texture_manager.get_texture("water"),
            "right": self.texture_manager.get_texture("water"),
            "front": self.texture_manager.get_texture("water"),
            "back": self.texture_manager.get_texture("water"),
        }