
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ChiseledQuartzBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ChiseledQuartzBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["chiseled_quartz_block_top"],
            "front": self.parent.textures["chiseled_quartz_block"],
            "back": self.parent.textures["chiseled_quartz_block"],
            "left": self.parent.textures["chiseled_quartz_block"],
            "right": self.parent.textures["chiseled_quartz_block"],
            "bottom": self.parent.textures["chiseled_quartz_block_top"]
        }
