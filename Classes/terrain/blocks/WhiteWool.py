
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        WhiteWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("WhiteWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["white_wool"],
            "front": self.parent.textures["white_wool"],
            "back": self.parent.textures["white_wool"],
            "left": self.parent.textures["white_wool"],
            "right": self.parent.textures["white_wool"],
            "bottom": self.parent.textures["white_wool"]
        }
