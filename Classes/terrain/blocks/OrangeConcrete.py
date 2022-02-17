
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OrangeConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OrangeConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["orange_concrete"],
            "front": self.parent.textures["orange_concrete"],
            "back": self.parent.textures["orange_concrete"],
            "left": self.parent.textures["orange_concrete"],
            "right": self.parent.textures["orange_concrete"],
            "bottom": self.parent.textures["orange_concrete"]
        }
