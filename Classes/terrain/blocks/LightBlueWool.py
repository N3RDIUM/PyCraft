
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightBlueWool
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightBlueWool", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_blue_wool"],
            "front": self.parent.textures["light_blue_wool"],
            "back": self.parent.textures["light_blue_wool"],
            "left": self.parent.textures["light_blue_wool"],
            "right": self.parent.textures["light_blue_wool"],
            "bottom": self.parent.textures["light_blue_wool"]
        }
