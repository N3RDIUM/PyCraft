
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Clay
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Clay", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["clay"],
            "front": self.parent.textures["clay"],
            "back": self.parent.textures["clay"],
            "left": self.parent.textures["clay"],
            "right": self.parent.textures["clay"],
            "bottom": self.parent.textures["clay"]
        }
