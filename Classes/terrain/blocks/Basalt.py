import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Basalt
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Basalt", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["basalt_top"],
            "front": self.parent.textures["basalt_side"],
            "back": self.parent.textures["basalt_side"],
            "left": self.parent.textures["basalt_side"],
            "right": self.parent.textures["basalt_side"],
            "bottom": self.parent.textures["basalt_top"]
        }
