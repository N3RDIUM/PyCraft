
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightGrayGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightGrayGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_gray_glazed_terracotta"],
            "front": self.parent.textures["light_gray_glazed_terracotta"],
            "back": self.parent.textures["light_gray_glazed_terracotta"],
            "left": self.parent.textures["light_gray_glazed_terracotta"],
            "right": self.parent.textures["light_gray_glazed_terracotta"],
            "bottom": self.parent.textures["light_gray_glazed_terracotta"]
        }
