
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DarkOakLeaves
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DarkOakLeaves", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["dark_oak_leaves"],
            "front": self.parent.textures["dark_oak_leaves"],
            "back": self.parent.textures["dark_oak_leaves"],
            "left": self.parent.textures["dark_oak_leaves"],
            "right": self.parent.textures["dark_oak_leaves"],
            "bottom": self.parent.textures["dark_oak_leaves"]
        }
