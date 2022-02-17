
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Rainbow
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Rainbow", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["debug"],
            "front": self.parent.textures["debug"],
            "back": self.parent.textures["debug"],
            "left": self.parent.textures["debug"],
            "right": self.parent.textures["debug"],
            "bottom": self.parent.textures["debug"]
        }
