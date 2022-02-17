
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GrayWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GrayWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["gray_wool"],
            "front": self.parent.textures["gray_wool"],
            "back": self.parent.textures["gray_wool"],
            "left": self.parent.textures["gray_wool"],
            "right": self.parent.textures["gray_wool"],
            "bottom": self.parent.textures["gray_wool"]
        }
