
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PolishedBasalt
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PolishedBasalt", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["polished_basalt_top"],
            "front": self.parent.textures["polished_basalt_side"],
            "back": self.parent.textures["polished_basalt_side"],
            "left": self.parent.textures["polished_basalt_side"],
            "right": self.parent.textures["polished_basalt_side"],
            "bottom": self.parent.textures["polished_basalt_top"]
        }
