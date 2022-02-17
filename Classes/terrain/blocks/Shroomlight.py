
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Shroomlight
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Shroomlight", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["shroomlight"],
            "front": self.parent.textures["shroomlight"],
            "back": self.parent.textures["shroomlight"],
            "left": self.parent.textures["shroomlight"],
            "right": self.parent.textures["shroomlight"],
            "bottom": self.parent.textures["shroomlight"]
        }
