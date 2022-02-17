
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        SpruceLog
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("SpruceLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["spruce_log_top"],
            "front": self.parent.textures["spruce_log"],
            "back": self.parent.textures["spruce_log"],
            "left": self.parent.textures["spruce_log"],
            "right": self.parent.textures["spruce_log"],
            "bottom": self.parent.textures["spruce_log_top"]
        }
