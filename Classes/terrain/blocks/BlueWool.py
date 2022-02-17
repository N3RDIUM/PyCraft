
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlueWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlueWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blue_wool"],
            "front": self.parent.textures["blue_wool"],
            "back": self.parent.textures["blue_wool"],
            "left": self.parent.textures["blue_wool"],
            "right": self.parent.textures["blue_wool"],
            "bottom": self.parent.textures["blue_wool"]
        }
