import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Sponge
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Sponge", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["sponge"],
            "front": self.parent.textures["sponge"],
            "back": self.parent.textures["sponge"],
            "left": self.parent.textures["sponge"],
            "right": self.parent.textures["sponge"],
            "bottom": self.parent.textures["sponge"]
        }
