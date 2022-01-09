
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OxidizedCopper
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OxidizedCopper", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["oxidized_copper"],
            "front": self.parent.textures["oxidized_copper"],
            "back": self.parent.textures["oxidized_copper"],
            "left": self.parent.textures["oxidized_copper"],
            "right": self.parent.textures["oxidized_copper"],
            "bottom": self.parent.textures["oxidized_copper"]
        }
