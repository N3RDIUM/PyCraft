from terrain.block import *

class _block(Block):
    def __init__(self, data, id):
        data["name"] = "dirt"
        super().__init__(data, id)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("dirt"),
            "bottom": self.texture_manager.get_texture("dirt"),
            "left": self.texture_manager.get_texture("dirt"),
            "right": self.texture_manager.get_texture("dirt"),
            "front": self.texture_manager.get_texture("dirt"),
            "back": self.texture_manager.get_texture("dirt"),
        }