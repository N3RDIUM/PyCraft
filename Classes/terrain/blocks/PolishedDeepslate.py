
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PolishedDeepslate
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PolishedDeepslate", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["polished_deepslate"],
            "front": self.parent.textures["polished_deepslate"],
            "back": self.parent.textures["polished_deepslate"],
            "left": self.parent.textures["polished_deepslate"],
            "right": self.parent.textures["polished_deepslate"],
            "bottom": self.parent.textures["polished_deepslate"]
        }
