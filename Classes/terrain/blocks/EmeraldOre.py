
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        EmeraldOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("EmeraldOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["emerald_ore"],
            "back": self.parent.textures["emerald_ore"],
            "left": self.parent.textures["emerald_ore"],
            "right": self.parent.textures["emerald_ore"],
            "bottom": self.parent.textures["stone"]
        }
