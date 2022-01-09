
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PurpleTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PurpleTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["purple_terracotta"],
            "front": self.parent.textures["purple_terracotta"],
            "back": self.parent.textures["purple_terracotta"],
            "left": self.parent.textures["purple_terracotta"],
            "right": self.parent.textures["purple_terracotta"],
            "bottom": self.parent.textures["purple_terracotta"]
        }
