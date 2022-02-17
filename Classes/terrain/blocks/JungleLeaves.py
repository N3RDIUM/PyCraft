
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        JungleLeaves
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("JungleLeaves", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["jungle_leaves"],
            "front": self.parent.textures["jungle_leaves"],
            "back": self.parent.textures["jungle_leaves"],
            "left": self.parent.textures["jungle_leaves"],
            "right": self.parent.textures["jungle_leaves"],
            "bottom": self.parent.textures["jungle_leaves"]
        }
