
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MagentaTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MagentaTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["magenta_terracotta"],
            "front": self.parent.textures["magenta_terracotta"],
            "back": self.parent.textures["magenta_terracotta"],
            "left": self.parent.textures["magenta_terracotta"],
            "right": self.parent.textures["magenta_terracotta"],
            "bottom": self.parent.textures["magenta_terracotta"]
        }
