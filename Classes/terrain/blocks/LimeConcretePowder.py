
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LimeConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LimeConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["lime_concrete_powder"],
            "front": self.parent.textures["lime_concrete_powder"],
            "back": self.parent.textures["lime_concrete_powder"],
            "left": self.parent.textures["lime_concrete_powder"],
            "right": self.parent.textures["lime_concrete_powder"],
            "bottom": self.parent.textures["lime_concrete_powder"]
        }
