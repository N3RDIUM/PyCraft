
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ExposedCopper
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ExposedCopper", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["exposed_copper"],
            "front": self.parent.textures["exposed_copper"],
            "back": self.parent.textures["exposed_copper"],
            "left": self.parent.textures["exposed_copper"],
            "right": self.parent.textures["exposed_copper"],
            "bottom": self.parent.textures["exposed_copper"]
        }
