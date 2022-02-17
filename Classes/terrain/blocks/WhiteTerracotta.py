
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        WhiteTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("WhiteTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["white_terracotta"],
            "front": self.parent.textures["white_terracotta"],
            "back": self.parent.textures["white_terracotta"],
            "left": self.parent.textures["white_terracotta"],
            "right": self.parent.textures["white_terracotta"],
            "bottom": self.parent.textures["white_terracotta"]
        }
