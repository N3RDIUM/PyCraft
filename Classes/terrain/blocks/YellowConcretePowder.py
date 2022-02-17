
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        YellowConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("YellowConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["yellow_concrete_powder"],
            "front": self.parent.textures["yellow_concrete_powder"],
            "back": self.parent.textures["yellow_concrete_powder"],
            "left": self.parent.textures["yellow_concrete_powder"],
            "right": self.parent.textures["yellow_concrete_powder"],
            "bottom": self.parent.textures["yellow_concrete_powder"]
        }
