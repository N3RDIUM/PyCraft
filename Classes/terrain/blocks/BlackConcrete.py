import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlackConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlackConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["black_concrete"],
            "front": self.parent.textures["black_concrete"],
            "back": self.parent.textures["black_concrete"],
            "left": self.parent.textures["black_concrete"],
            "right": self.parent.textures["black_concrete"],
            "bottom": self.parent.textures["black_concrete"]
        }
