import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Sand
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Sand", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["sand"],
            "front": self.parent.textures["sand"],
            "back": self.parent.textures["sand"],
            "left": self.parent.textures["sand"],
            "right": self.parent.textures["sand"],
            "bottom": self.parent.textures["sand"]
        }
