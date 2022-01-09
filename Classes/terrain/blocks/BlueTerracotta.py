
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlueTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlueTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blue_terracotta"],
            "front": self.parent.textures["blue_terracotta"],
            "back": self.parent.textures["blue_terracotta"],
            "left": self.parent.textures["blue_terracotta"],
            "right": self.parent.textures["blue_terracotta"],
            "bottom": self.parent.textures["blue_terracotta"]
        }
