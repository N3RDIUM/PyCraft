import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DiamondOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DiamondOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["diamond_ore"],
            "back": self.parent.textures["diamond_ore"],
            "left": self.parent.textures["diamond_ore"],
            "right": self.parent.textures["diamond_ore"],
            "bottom": self.parent.textures["stone"]
        }
