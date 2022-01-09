import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Andesite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Andesite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["andesite"],
            "front": self.parent.textures["andesite"],
            "back": self.parent.textures["andesite"],
            "left": self.parent.textures["andesite"],
            "right": self.parent.textures["andesite"],
            "bottom": self.parent.textures["andesite"]
        }
