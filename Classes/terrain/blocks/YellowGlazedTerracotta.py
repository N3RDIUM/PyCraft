
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        YellowGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("YellowGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["yellow_glazed_terracotta"],
            "front": self.parent.textures["yellow_glazed_terracotta"],
            "back": self.parent.textures["yellow_glazed_terracotta"],
            "left": self.parent.textures["yellow_glazed_terracotta"],
            "right": self.parent.textures["yellow_glazed_terracotta"],
            "bottom": self.parent.textures["yellow_glazed_terracotta"]
        }
