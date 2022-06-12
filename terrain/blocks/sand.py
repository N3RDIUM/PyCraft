from terrain import *

class block(Block):
    def __init__(self, renderer):
        super().__init__("sand", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["sand.png"],
            "bottom": self.renderer.texture_manager.texture_coords["sand.png"],
            "left": self.renderer.texture_manager.texture_coords["sand.png"],
            "right": self.renderer.texture_manager.texture_coords["sand.png"],
            "front": self.renderer.texture_manager.texture_coords["sand.png"],
            "back": self.renderer.texture_manager.texture_coords["sand.png"]
        }