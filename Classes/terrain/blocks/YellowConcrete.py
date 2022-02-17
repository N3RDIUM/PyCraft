
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        YellowConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("YellowConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["yellow_concrete"],
            "front": self.parent.textures["yellow_concrete"],
            "back": self.parent.textures["yellow_concrete"],
            "left": self.parent.textures["yellow_concrete"],
            "right": self.parent.textures["yellow_concrete"],
            "bottom": self.parent.textures["yellow_concrete"]
        }
