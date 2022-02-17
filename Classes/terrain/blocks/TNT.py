
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        TNT
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("TNT", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["tnt_top"],
            "front": self.parent.textures["tnt_side"],
            "back": self.parent.textures["tnt_side"],
            "left": self.parent.textures["tnt_side"],
            "right": self.parent.textures["tnt_side"],
            "bottom": self.parent.textures["tnt_bottom"]
        }
