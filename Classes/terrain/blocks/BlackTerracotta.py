import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlackTerracotta
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlackTerracotta", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["black_terracotta"],
            "front": self.parent.textures["black_terracotta"],
            "back": self.parent.textures["black_terracotta"],
            "left": self.parent.textures["black_terracotta"],
            "right": self.parent.textures["black_terracotta"],
            "bottom": self.parent.textures["black_terracotta"]
        }
