import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grout
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Grout", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["grout"],
            "front": self.parent.textures["grout"],
            "back": self.parent.textures["grout"],
            "left": self.parent.textures["grout"],
            "right": self.parent.textures["grout"],
            "bottom": self.parent.textures["grout"]
        }
