from terrain import *

class block(Block):
    def __init__(self, renderer):
        super().__init__("grass", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["grass.png"],
            "bottom": self.renderer.texture_manager.texture_coords["dirt.png"],
            "left": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "right": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "front": self.renderer.texture_manager.texture_coords["grass_side.png"],
            "back": self.renderer.texture_manager.texture_coords["grass_side.png"]
        }