
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BrownWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BrownWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["brown_wool"],
            "front": self.parent.textures["brown_wool"],
            "back": self.parent.textures["brown_wool"],
            "left": self.parent.textures["brown_wool"],
            "right": self.parent.textures["brown_wool"],
            "bottom": self.parent.textures["brown_wool"]
        }
