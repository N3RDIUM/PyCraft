
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlueConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlueConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blue_concrete_powder"],
            "front": self.parent.textures["blue_concrete_powder"],
            "back": self.parent.textures["blue_concrete_powder"],
            "left": self.parent.textures["blue_concrete_powder"],
            "right": self.parent.textures["blue_concrete_powder"],
            "bottom": self.parent.textures["blue_concrete_powder"]
        }
