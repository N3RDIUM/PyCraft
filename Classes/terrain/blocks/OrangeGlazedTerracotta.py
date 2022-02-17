
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OrangeGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OrangeGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["orange_glazed_terracotta"],
            "front": self.parent.textures["orange_glazed_terracotta"],
            "back": self.parent.textures["orange_glazed_terracotta"],
            "left": self.parent.textures["orange_glazed_terracotta"],
            "right": self.parent.textures["orange_glazed_terracotta"],
            "bottom": self.parent.textures["orange_glazed_terracotta"]
        }
