
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MagentaConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MagentaConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["magenta_concrete"],
            "front": self.parent.textures["magenta_concrete"],
            "back": self.parent.textures["magenta_concrete"],
            "left": self.parent.textures["magenta_concrete"],
            "right": self.parent.textures["magenta_concrete"],
            "bottom": self.parent.textures["magenta_concrete"]
        }
