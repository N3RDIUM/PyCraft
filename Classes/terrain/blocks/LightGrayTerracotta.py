
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightGrayTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightGrayTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_gray_terracotta"],
            "front": self.parent.textures["light_gray_terracotta"],
            "back": self.parent.textures["light_gray_terracotta"],
            "left": self.parent.textures["light_gray_terracotta"],
            "right": self.parent.textures["light_gray_terracotta"],
            "bottom": self.parent.textures["light_gray_terracotta"]
        }
