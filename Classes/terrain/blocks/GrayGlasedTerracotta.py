
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GrayGlasedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GrayGlasedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["gray_glazed_terracotta"],
            "front": self.parent.textures["gray_glazed_terracotta"],
            "back": self.parent.textures["gray_glazed_terracotta"],
            "left": self.parent.textures["gray_glazed_terracotta"],
            "right": self.parent.textures["gray_glazed_terracotta"],
            "bottom": self.parent.textures["gray_glazed_terracotta"]
        }
