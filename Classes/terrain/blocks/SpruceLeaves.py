
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        SpruceLeaves
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("SpruceLeaves", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["spruce_leaves"],
            "front": self.parent.textures["spruce_leaves"],
            "back": self.parent.textures["spruce_leaves"],
            "left": self.parent.textures["spruce_leaves"],
            "right": self.parent.textures["spruce_leaves"],
            "bottom": self.parent.textures["spruce_leaves"]
        }
