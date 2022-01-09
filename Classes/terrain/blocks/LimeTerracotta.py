
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LimeTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LimeTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["lime_terracotta"],
            "front": self.parent.textures["lime_terracotta"],
            "back": self.parent.textures["lime_terracotta"],
            "left": self.parent.textures["lime_terracotta"],
            "right": self.parent.textures["lime_terracotta"],
            "bottom": self.parent.textures["lime_terracotta"]
        }
