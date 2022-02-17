import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        OakLog
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("OakLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["oak_log_top"],
            "front": self.parent.textures["oak_log"],
            "back": self.parent.textures["oak_log"],
            "left": self.parent.textures["oak_log"],
            "right": self.parent.textures["oak_log"],
            "bottom": self.parent.textures["oak_log_top"]
        }
