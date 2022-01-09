
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PurpurBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PurpurBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["purpur_block"],
            "front": self.parent.textures["purpur_block"],
            "back": self.parent.textures["purpur_block"],
            "left": self.parent.textures["purpur_block"],
            "right": self.parent.textures["purpur_block"],
            "bottom": self.parent.textures["purpur_block"]
        }
