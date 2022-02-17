import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Beacon
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Beacon", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["beacon"],
            "front": self.parent.textures["beacon"],
            "back": self.parent.textures["beacon"],
            "left": self.parent.textures["beacon"],
            "right": self.parent.textures["beacon"],
            "bottom": self.parent.textures["beacon"]
        }
