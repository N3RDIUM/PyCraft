import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grout
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Grout", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["grout_sand"],
            "front": self.parent.textures["grout_sand"],
            "back": self.parent.textures["grout_sand"],
            "left": self.parent.textures["grout_sand"],
            "right": self.parent.textures["grout_sand"],
            "bottom": self.parent.textures["grout_sand"]
        }
