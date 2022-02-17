
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Brownterracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Brownterracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["brown_terracotta"],
            "front": self.parent.textures["brown_terracotta"],
            "back": self.parent.textures["brown_terracotta"],
            "left": self.parent.textures["brown_terracotta"],
            "right": self.parent.textures["brown_terracotta"],
            "bottom": self.parent.textures["brown_terracotta"]
        }
