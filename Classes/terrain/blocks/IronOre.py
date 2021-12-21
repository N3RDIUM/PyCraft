import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        IronOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Stone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["iron_ore"],
            "back": self.parent.textures["iron_ore"],
            "left": self.parent.textures["iron_ore"],
            "right": self.parent.textures["iron_ore"],
            "bottom": self.parent.textures["stone"]
        }
