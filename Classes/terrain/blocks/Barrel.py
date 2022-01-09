import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Barrel
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Barrel", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["barrel_top"],
            "front": self.parent.textures["barrel_side"],
            "back": self.parent.textures["barrel_side"],
            "left": self.parent.textures["barrel_side"],
            "right": self.parent.textures["barrel_side"],
            "bottom": self.parent.textures["barrel_bottom"]
        }
