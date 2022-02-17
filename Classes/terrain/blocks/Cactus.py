
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Cactus
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Cactus", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cactus_top"],
            "front": self.parent.textures["cactus_side"],
            "back": self.parent.textures["cactus_side"],
            "left": self.parent.textures["cactus_side"],
            "right": self.parent.textures["cactus_side"],
            "bottom": self.parent.textures["cactus_bottom"]
        }
