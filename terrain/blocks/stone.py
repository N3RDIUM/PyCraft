from terrain.block import *

class _block(Block):
    def __init__(self, data, id):
        data["name"] = "stone"
        super().__init__(data, id)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("stone"),
            "bottom": self.texture_manager.get_texture("stone"),
            "left": self.texture_manager.get_texture("stone"),
            "right": self.texture_manager.get_texture("stone"),
            "front": self.texture_manager.get_texture("stone"),
            "back": self.texture_manager.get_texture("stone"),
        }