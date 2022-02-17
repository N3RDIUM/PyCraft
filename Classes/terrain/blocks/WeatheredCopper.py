
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        WeatheredCopper
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("WeatheredCopper", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["weathered_copper"],
            "front": self.parent.textures["weathered_copper"],
            "back": self.parent.textures["weathered_copper"],
            "left": self.parent.textures["weathered_copper"],
            "right": self.parent.textures["weathered_copper"],
            "bottom": self.parent.textures["weathered_copper"]
        }
