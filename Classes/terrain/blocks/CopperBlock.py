
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CopperBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CopperBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["copper_block"],
            "front": self.parent.textures["copper_block"],
            "back": self.parent.textures["copper_block"],
            "left": self.parent.textures["copper_block"],
            "right": self.parent.textures["copper_block"],
            "bottom": self.parent.textures["copper_block"]
        }
