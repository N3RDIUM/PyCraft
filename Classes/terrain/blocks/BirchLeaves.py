import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grass
        
        * Initializes the grass block
        
        :parent: the parent window
        """
        super().__init__("Dirt", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["birch_leaves"],
            "front": self.parent.textures["birch_leaves"],
            "back": self.parent.textures["birch_leaves"],
            "left": self.parent.textures["birch_leaves"],
            "right": self.parent.textures["birch_leaves"],
            "bottom": self.parent.textures["birch_leaves"]
        }
