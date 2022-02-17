
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LimeWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LimeWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["lime_wool"],
            "front": self.parent.textures["lime_wool"],
            "back": self.parent.textures["lime_wool"],
            "left": self.parent.textures["lime_wool"],
            "right": self.parent.textures["lime_wool"],
            "bottom": self.parent.textures["lime_wool"]
        }
