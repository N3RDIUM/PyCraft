
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Ice
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Ice", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["ice"],
            "front": self.parent.textures["ice"],
            "back": self.parent.textures["ice"],
            "left": self.parent.textures["ice"],
            "right": self.parent.textures["ice"],
            "bottom": self.parent.textures["ice"]
        }
