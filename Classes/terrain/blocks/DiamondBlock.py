
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DiamondBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DiamondBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["diamond_block"],
            "front": self.parent.textures["diamond_block"],
            "back": self.parent.textures["diamond_block"],
            "left": self.parent.textures["diamond_block"],
            "right": self.parent.textures["diamond_block"],
            "bottom": self.parent.textures["diamond_block"]
        }
