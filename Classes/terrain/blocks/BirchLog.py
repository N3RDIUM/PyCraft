import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grass
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BirchLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["birch_log_top"],
            "front": self.parent.textures["birch_log"],
            "back": self.parent.textures["birch_log"],
            "left": self.parent.textures["birch_log"],
            "right": self.parent.textures["birch_log"],
            "bottom": self.parent.textures["birch_log_top"]
        }
