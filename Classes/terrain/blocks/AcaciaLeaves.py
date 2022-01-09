import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        AcaciaLeaves
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("AcaciaLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["acacia_leaves"],
            "front": self.parent.textures["acacia_leaves"],
            "back": self.parent.textures["acacia_leaves"],
            "left": self.parent.textures["acacia_leaves"],
            "right": self.parent.textures["acacia_leaves"],
            "bottom": self.parent.textures["acacia_leaves"]
        }
