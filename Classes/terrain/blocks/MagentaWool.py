
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MagentaWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MagentaWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["magenta_wool"],
            "front": self.parent.textures["magenta_wool"],
            "back": self.parent.textures["magenta_wool"],
            "left": self.parent.textures["magenta_wool"],
            "right": self.parent.textures["magenta_wool"],
            "bottom": self.parent.textures["magenta_wool"]
        }
