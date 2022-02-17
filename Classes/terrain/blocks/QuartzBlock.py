
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        QuartzBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("QuartzBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["quartz_block_top"],
            "front": self.parent.textures["quartz_block_side"],
            "back": self.parent.textures["quartz_block_side"],
            "left": self.parent.textures["quartz_block_side"],
            "right": self.parent.textures["quartz_block_side"],
            "bottom": self.parent.textures["quartz_block_bottom"]
        }
