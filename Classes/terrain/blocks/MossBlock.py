
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MossBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MossBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["moss_block"],
            "front": self.parent.textures["moss_block"],
            "back": self.parent.textures["moss_block"],
            "left": self.parent.textures["moss_block"],
            "right": self.parent.textures["moss_block"],
            "bottom": self.parent.textures["moss_block"]
        }
