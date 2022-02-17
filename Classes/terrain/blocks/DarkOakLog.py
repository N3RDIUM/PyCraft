
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DarkOakLog
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DarkOakLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["dark_oak_log_top"],
            "front": self.parent.textures["dark_oak_log"],
            "back": self.parent.textures["dark_oak_log"],
            "left": self.parent.textures["dark_oak_log"],
            "right": self.parent.textures["dark_oak_log"],
            "bottom": self.parent.textures["dark_oak_log_top"]
        }
