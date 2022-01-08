import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OakLeaves
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OakLeaves", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["oak_leaves"],
            "front": self.parent.textures["oak_leaves"],
            "back": self.parent.textures["oak_leaves"],
            "left": self.parent.textures["oak_leaves"],
            "right": self.parent.textures["oak_leaves"],
            "bottom": self.parent.textures["oak_leaves"]
        }
