import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Glass
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Glass", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["glass"],
            "front": self.parent.textures["glass"],
            "back": self.parent.textures["glass"],
            "left": self.parent.textures["glass"],
            "right": self.parent.textures["glass"],
            "bottom": self.parent.textures["glass"]
        }
