
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        RawIronBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("RawIronBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["raw_iron_block"],
            "front": self.parent.textures["raw_iron_block"],
            "back": self.parent.textures["raw_iron_block"],
            "left": self.parent.textures["raw_iron_block"],
            "right": self.parent.textures["raw_iron_block"],
            "bottom": self.parent.textures["raw_iron_block"]
        }
