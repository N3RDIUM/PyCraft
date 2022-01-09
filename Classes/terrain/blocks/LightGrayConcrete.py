
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        LightGrayConcrete
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("LightGrayConcrete", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["light_gray_concrete"],
            "front": self.parent.textures["light_gray_concrete"],
            "back": self.parent.textures["light_gray_concrete"],
            "left": self.parent.textures["light_gray_concrete"],
            "right": self.parent.textures["light_gray_concrete"],
            "bottom": self.parent.textures["light_gray_concrete"]
        }
