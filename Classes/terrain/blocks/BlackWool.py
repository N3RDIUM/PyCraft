import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlackWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlackWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["black_wool"],
            "front": self.parent.textures["black_wool"],
            "back": self.parent.textures["black_wool"],
            "left": self.parent.textures["black_wool"],
            "right": self.parent.textures["black_wool"],
            "bottom": self.parent.textures["black_wool"]
        }
