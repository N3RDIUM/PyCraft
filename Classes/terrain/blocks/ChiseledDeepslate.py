
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ChiseledDeepslate
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ChiseledDeepslate", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["chiseled_deepslate"],
            "front": self.parent.textures["chiseled_deepslate"],
            "back": self.parent.textures["chiseled_deepslate"],
            "left": self.parent.textures["chiseled_deepslate"],
            "right": self.parent.textures["chiseled_deepslate"],
            "bottom": self.parent.textures["chiseled_deepslate"]
        }
