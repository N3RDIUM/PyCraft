import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GoldOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GoldOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["gold_ore"],
            "back": self.parent.textures["gold_ore"],
            "left": self.parent.textures["gold_ore"],
            "right": self.parent.textures["gold_ore"],
            "bottom": self.parent.textures["stone"]
        }
