
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PurpleWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PurpleWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["purple_wool"],
            "front": self.parent.textures["purple_wool"],
            "back": self.parent.textures["purple_wool"],
            "left": self.parent.textures["purple_wool"],
            "right": self.parent.textures["purple_wool"],
            "bottom": self.parent.textures["purple_wool"]
        }
