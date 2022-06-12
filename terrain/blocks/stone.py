from terrain import *

class block(Block):
    def __init__(self, renderer):
        super().__init__("stone", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["stone.png"],
            "bottom": self.renderer.texture_manager.texture_coords["stone.png"],
            "left": self.renderer.texture_manager.texture_coords["stone.png"],
            "right": self.renderer.texture_manager.texture_coords["stone.png"],
            "front": self.renderer.texture_manager.texture_coords["stone.png"],
            "back": self.renderer.texture_manager.texture_coords["stone.png"]
        }