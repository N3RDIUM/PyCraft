
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CutCopper
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CutCopper", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cut_copper"],
            "front": self.parent.textures["cut_copper"],
            "back": self.parent.textures["cut_copper"],
            "left": self.parent.textures["cut_copper"],
            "right": self.parent.textures["cut_copper"],
            "bottom": self.parent.textures["cut_copper"]
        }
