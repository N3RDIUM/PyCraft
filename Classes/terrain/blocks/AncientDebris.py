import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        AncientDebris
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("AncientDebris", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["ancient_debris_top"],
            "front": self.parent.textures["ancient_debris_side"],
            "back": self.parent.textures["ancient_debris_side"],
            "left": self.parent.textures["ancient_debris_side"],
            "right": self.parent.textures["ancient_debris_side"],
            "bottom": self.parent.textures["ancient_debris_top"]
        }
