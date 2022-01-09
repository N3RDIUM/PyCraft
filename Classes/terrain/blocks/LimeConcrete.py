
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LimeConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LimeConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["lime_concrete"],
            "front": self.parent.textures["lime_concrete"],
            "back": self.parent.textures["lime_concrete"],
            "left": self.parent.textures["lime_concrete"],
            "right": self.parent.textures["lime_concrete"],
            "bottom": self.parent.textures["lime_concrete"]
        }
