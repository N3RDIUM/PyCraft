import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Coal
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CoalBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["coal_block"],
            "front": self.parent.textures["coal_block"],
            "back": self.parent.textures["coal_block"],
            "left": self.parent.textures["coal_block"],
            "right": self.parent.textures["coal_block"],
            "bottom": self.parent.textures["coal_block"]
        }
