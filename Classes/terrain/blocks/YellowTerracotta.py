
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        YellowTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("YellowTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["yellow_terracotta"],
            "front": self.parent.textures["yellow_terracotta"],
            "back": self.parent.textures["yellow_terracotta"],
            "left": self.parent.textures["yellow_terracotta"],
            "right": self.parent.textures["yellow_terracotta"],
            "bottom": self.parent.textures["yellow_terracotta"]
        }
