import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlackConcretePowder
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlackConcretePowder", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["black_concrete_powder"],
            "front": self.parent.textures["black_concrete_powder"],
            "back": self.parent.textures["black_concrete_powder"],
            "left": self.parent.textures["black_concrete_powder"],
            "right": self.parent.textures["black_concrete_powder"],
            "bottom": self.parent.textures["black_concrete_powder"]
        }
