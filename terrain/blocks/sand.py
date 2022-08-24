from terrain.block import *

class _block(Block):
    def __init__(self, data, id):
        data["name"] = "sand"
        super().__init__(data, id)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("sand"),
            "bottom": self.texture_manager.get_texture("sand"),
            "left": self.texture_manager.get_texture("sand"),
            "right": self.texture_manager.get_texture("sand"),
            "front": self.texture_manager.get_texture("sand"),
            "back": self.texture_manager.get_texture("sand"),
        }