
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        IronBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("IronBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["iron_block"],
            "front": self.parent.textures["iron_block"],
            "back": self.parent.textures["iron_block"],
            "left": self.parent.textures["iron_block"],
            "right": self.parent.textures["iron_block"],
            "bottom": self.parent.textures["iron_block"]
        }
