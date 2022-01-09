import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Blackstone
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Blackstone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blackstone_top"],
            "front": self.parent.textures["blackstone"],
            "back": self.parent.textures["blackstone"],
            "left": self.parent.textures["blackstone"],
            "right": self.parent.textures["blackstone"],
            "bottom": self.parent.textures["blackstone_top"]
        }
