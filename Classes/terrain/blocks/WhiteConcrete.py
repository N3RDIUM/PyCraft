
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        WhiteConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("WhiteConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["white_concrete"],
            "front": self.parent.textures["white_concrete"],
            "back": self.parent.textures["white_concrete"],
            "left": self.parent.textures["white_concrete"],
            "right": self.parent.textures["white_concrete"],
            "bottom": self.parent.textures["white_concrete"]
        }
