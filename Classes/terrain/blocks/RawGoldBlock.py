
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        RawGoldBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("RawGoldBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["raw_gold_block"],
            "front": self.parent.textures["raw_gold_block"],
            "back": self.parent.textures["raw_gold_block"],
            "left": self.parent.textures["raw_gold_block"],
            "right": self.parent.textures["raw_gold_block"],
            "bottom": self.parent.textures["raw_gold_block"]
        }
