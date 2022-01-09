
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GreenConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GreenConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["green_concrete"],
            "front": self.parent.textures["green_concrete"],
            "back": self.parent.textures["green_concrete"],
            "left": self.parent.textures["green_concrete"],
            "right": self.parent.textures["green_concrete"],
            "bottom": self.parent.textures["green_concrete"]
        }
