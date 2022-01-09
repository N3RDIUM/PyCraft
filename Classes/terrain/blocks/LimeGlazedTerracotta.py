
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LimeGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LimeGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["lime_glazed_terracotta"],
            "front": self.parent.textures["lime_glazed_terracotta"],
            "back": self.parent.textures["lime_glazed_terracotta"],
            "left": self.parent.textures["lime_glazed_terracotta"],
            "right": self.parent.textures["lime_glazed_terracotta"],
            "bottom": self.parent.textures["lime_glazed_terracotta"]
        }
