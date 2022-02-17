
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        WhiteConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("WhiteConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["white_concrete_powder"],
            "front": self.parent.textures["white_concrete_powder"],
            "back": self.parent.textures["white_concrete_powder"],
            "left": self.parent.textures["white_concrete_powder"],
            "right": self.parent.textures["white_concrete_powder"],
            "bottom": self.parent.textures["white_concrete_powder"]
        }
