
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        EmeraldBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("EmeraldBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["emerald_block"],
            "front": self.parent.textures["emerald_block"],
            "back": self.parent.textures["emerald_block"],
            "left": self.parent.textures["emerald_block"],
            "right": self.parent.textures["emerald_block"],
            "bottom": self.parent.textures["emerald_block"]
        }
