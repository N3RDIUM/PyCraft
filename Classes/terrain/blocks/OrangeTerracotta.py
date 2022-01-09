
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OrangeTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OrangeTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["orange_terracotta"],
            "front": self.parent.textures["orange_terracotta"],
            "back": self.parent.textures["orange_terracotta"],
            "left": self.parent.textures["orange_terracotta"],
            "right": self.parent.textures["orange_terracotta"],
            "bottom": self.parent.textures["orange_terracotta"]
        }
