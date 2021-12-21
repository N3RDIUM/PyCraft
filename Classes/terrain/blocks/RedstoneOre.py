import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        RedstoneOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("RedstoneOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["stone"],
            "front": self.parent.textures["redstone_ore"],
            "back": self.parent.textures["redstone_ore"],
            "left": self.parent.textures["redstone_ore"],
            "right": self.parent.textures["redstone_ore"],
            "bottom": self.parent.textures["stone"]
        }
