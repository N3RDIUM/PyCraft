
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Terracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Terracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["terracotta"],
            "front": self.parent.textures["terracotta"],
            "back": self.parent.textures["terracotta"],
            "left": self.parent.textures["terracotta"],
            "right": self.parent.textures["terracotta"],
            "bottom": self.parent.textures["terracotta"]
        }
