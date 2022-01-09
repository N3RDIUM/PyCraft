
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CyanWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CyanWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cyan_wool"],
            "front": self.parent.textures["cyan_wool"],
            "back": self.parent.textures["cyan_wool"],
            "left": self.parent.textures["cyan_wool"],
            "right": self.parent.textures["cyan_wool"],
            "bottom": self.parent.textures["cyan_wool"]
        }
