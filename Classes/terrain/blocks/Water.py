import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Water
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Water", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["water_still"],
            "front": self.parent.textures["water_still"],
            "back": self.parent.textures["water_still"],
            "left": self.parent.textures["water_still"],
            "right": self.parent.textures["water_still"],
            "bottom": self.parent.textures["water_still"]
        }
