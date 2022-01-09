
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OxidizedCutCopper
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OxidizedCutCopper", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["oxidized_cut_copper"],
            "front": self.parent.textures["oxidized_cut_copper"],
            "back": self.parent.textures["oxidized_cut_copper"],
            "left": self.parent.textures["oxidized_cut_copper"],
            "right": self.parent.textures["oxidized_cut_copper"],
            "bottom": self.parent.textures["oxidized_cut_copper"]
        }
