
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CyanTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CyanTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cyan_terracotta"],
            "front": self.parent.textures["cyan_terracotta"],
            "back": self.parent.textures["cyan_terracotta"],
            "left": self.parent.textures["cyan_terracotta"],
            "right": self.parent.textures["cyan_terracotta"],
            "bottom": self.parent.textures["cyan_terracotta"]
        }
