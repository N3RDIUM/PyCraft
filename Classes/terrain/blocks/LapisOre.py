
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LapisOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LapisOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["lapis_ore"],
            "back": self.parent.textures["lapis_ore"],
            "left": self.parent.textures["lapis_ore"],
            "right": self.parent.textures["lapis_ore"],
            "bottom": self.parent.textures["stone"]
        }
