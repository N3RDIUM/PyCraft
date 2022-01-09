import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BlueConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BlueConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["blue_concrete"],
            "front": self.parent.textures["blue_concrete"],
            "back": self.parent.textures["blue_concrete"],
            "left": self.parent.textures["blue_concrete"],
            "right": self.parent.textures["blue_concrete"],
            "bottom": self.parent.textures["blue_concrete"]
        }
