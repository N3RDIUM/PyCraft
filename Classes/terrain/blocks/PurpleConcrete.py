
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PurpleConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PurpleConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["purple_concrete"],
            "front": self.parent.textures["purple_concrete"],
            "back": self.parent.textures["purple_concrete"],
            "left": self.parent.textures["purple_concrete"],
            "right": self.parent.textures["purple_concrete"],
            "bottom": self.parent.textures["purple_concrete"]
        }
