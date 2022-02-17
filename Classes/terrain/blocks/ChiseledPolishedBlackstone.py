
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ChiseledPolishedBlackstone
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ChiseledPolishedBlackstone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["chiseled_polished_blackstone"],
            "front": self.parent.textures["chiseled_polished_blackstone"],
            "back": self.parent.textures["chiseled_polished_blackstone"],
            "left": self.parent.textures["chiseled_polished_blackstone"],
            "right": self.parent.textures["chiseled_polished_blackstone"],
            "bottom": self.parent.textures["chiseled_polished_blackstone"]
        }
