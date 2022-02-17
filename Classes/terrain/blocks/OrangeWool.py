
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OrangeWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OrangeWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["orange_wool"],
            "front": self.parent.textures["orange_wool"],
            "back": self.parent.textures["orange_wool"],
            "left": self.parent.textures["orange_wool"],
            "right": self.parent.textures["orange_wool"],
            "bottom": self.parent.textures["orange_wool"]
        }
