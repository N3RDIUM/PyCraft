from terrain import *

class block(Block):
    def __init__(self, renderer):
        super().__init__("dirt", renderer)
        self.tex_coords = {
            "top": self.renderer.texture_manager.texture_coords["dirt.png"],
            "bottom": self.renderer.texture_manager.texture_coords["dirt.png"],
            "left": self.renderer.texture_manager.texture_coords["dirt.png"],
            "right": self.renderer.texture_manager.texture_coords["dirt.png"],
            "front": self.renderer.texture_manager.texture_coords["dirt.png"],
            "back": self.renderer.texture_manager.texture_coords["dirt.png"]
        }

        self.preloads_per_frame = 100