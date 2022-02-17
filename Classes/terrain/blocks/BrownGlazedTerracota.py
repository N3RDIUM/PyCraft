
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BrownGlazedterracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BrownGlazedterracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["brown_glazed_terracotta"],
            "front": self.parent.textures["brown_glazed_terracotta"],
            "back": self.parent.textures["brown_glazed_terracotta"],
            "left": self.parent.textures["brown_glazed_terracotta"],
            "right": self.parent.textures["brown_glazed_terracotta"],
            "bottom": self.parent.textures["brown_glazed_terracotta"]
        }
