
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlueIce
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlueIce", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blue_ice"],
            "front": self.parent.textures["blue_ice"],
            "back": self.parent.textures["blue_ice"],
            "left": self.parent.textures["blue_ice"],
            "right": self.parent.textures["blue_ice"],
            "bottom": self.parent.textures["blue_ice"]
        }
