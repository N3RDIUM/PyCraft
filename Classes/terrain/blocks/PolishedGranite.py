
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PolishedGranite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PolishedGranite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["polished_granite"],
            "front": self.parent.textures["polished_granite"],
            "back": self.parent.textures["polished_granite"],
            "left": self.parent.textures["polished_granite"],
            "right": self.parent.textures["polished_granite"],
            "bottom": self.parent.textures["polished_granite"]
        }
