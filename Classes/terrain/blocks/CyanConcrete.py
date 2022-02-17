
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CyanConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CyanConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cyan_concrete"],
            "front": self.parent.textures["cyan_concrete"],
            "back": self.parent.textures["cyan_concrete"],
            "left": self.parent.textures["cyan_concrete"],
            "right": self.parent.textures["cyan_concrete"],
            "bottom": self.parent.textures["cyan_concrete"]
        }
