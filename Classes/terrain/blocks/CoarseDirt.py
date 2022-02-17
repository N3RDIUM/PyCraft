
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CoarseDirt
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CoarseDirt", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["coarse_dirt"],
            "front": self.parent.textures["coarse_dirt"],
            "back": self.parent.textures["coarse_dirt"],
            "left": self.parent.textures["coarse_dirt"],
            "right": self.parent.textures["coarse_dirt"],
            "bottom": self.parent.textures["coarse_dirt"]
        }
