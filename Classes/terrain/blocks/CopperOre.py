
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CopperOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CopperOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["copper_ore"],
            "back": self.parent.textures["copper_ore"],
            "left": self.parent.textures["copper_ore"],
            "right": self.parent.textures["copper_ore"],
            "bottom": self.parent.textures["stone"]
        }
