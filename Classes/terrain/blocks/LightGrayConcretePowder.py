
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightGrayConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightGrayConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_gray_concrete_powder"],
            "front": self.parent.textures["light_gray_concrete_powder"],
            "back": self.parent.textures["light_gray_concrete_powder"],
            "left": self.parent.textures["light_gray_concrete_powder"],
            "right": self.parent.textures["light_gray_concrete_powder"],
            "bottom": self.parent.textures["light_gray_concrete_powder"]
        }
