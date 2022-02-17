import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlackGlazedTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlackGlazedTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["black_glazed_terracotta"],
            "front": self.parent.textures["black_glazed_terracotta"],
            "back": self.parent.textures["black_glazed_terracotta"],
            "left": self.parent.textures["black_glazed_terracotta"],
            "right": self.parent.textures["black_glazed_terracotta"],
            "bottom": self.parent.textures["black_glazed_terracotta"]
        }
