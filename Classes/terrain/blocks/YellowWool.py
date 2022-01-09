
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        YellowWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("YellowWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["yellow_wool"],
            "front": self.parent.textures["yellow_wool"],
            "back": self.parent.textures["yellow_wool"],
            "left": self.parent.textures["yellow_wool"],
            "right": self.parent.textures["yellow_wool"],
            "bottom": self.parent.textures["yellow_wool"]
        }
