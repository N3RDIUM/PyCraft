
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GreenTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GreenTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["green_terracotta"],
            "front": self.parent.textures["green_terracotta"],
            "back": self.parent.textures["green_terracotta"],
            "left": self.parent.textures["green_terracotta"],
            "right": self.parent.textures["green_terracotta"],
            "bottom": self.parent.textures["green_terracotta"]
        }
