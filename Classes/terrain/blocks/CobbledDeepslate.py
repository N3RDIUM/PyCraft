
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CobbledDeepslate
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CobbledDeepslate", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cobbled_deepslate"],
            "front": self.parent.textures["cobbled_deepslate"],
            "back": self.parent.textures["cobbled_deepslate"],
            "left": self.parent.textures["cobbled_deepslate"],
            "right": self.parent.textures["cobbled_deepslate"],
            "bottom": self.parent.textures["cobbled_deepslate"]
        }
