
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        GrayConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("GrayConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["gray_concrete"],
            "front": self.parent.textures["gray_concrete"],
            "back": self.parent.textures["gray_concrete"],
            "left": self.parent.textures["gray_concrete"],
            "right": self.parent.textures["gray_concrete"],
            "bottom": self.parent.textures["gray_concrete"]
        }
