
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MagentaGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MagentaGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["magenta_glazed_terracotta"],
            "front": self.parent.textures["magenta_glazed_terracotta"],
            "back": self.parent.textures["magenta_glazed_terracotta"],
            "left": self.parent.textures["magenta_glazed_terracotta"],
            "right": self.parent.textures["magenta_glazed_terracotta"],
            "bottom": self.parent.textures["magenta_glazed_terracotta"]
        }
