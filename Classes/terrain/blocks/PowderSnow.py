
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PowderSnow
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PowderSnow", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["powder_snow"],
            "front": self.parent.textures["powder_snow"],
            "back": self.parent.textures["powder_snow"],
            "left": self.parent.textures["powder_snow"],
            "right": self.parent.textures["powder_snow"],
            "bottom": self.parent.textures["powder_snow"]
        }
