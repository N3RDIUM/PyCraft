
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightGrayWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightGrayWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_gray_wool"],
            "front": self.parent.textures["light_gray_wool"],
            "back": self.parent.textures["light_gray_wool"],
            "left": self.parent.textures["light_gray_wool"],
            "right": self.parent.textures["light_gray_wool"],
            "bottom": self.parent.textures["light_gray_wool"]
        }
