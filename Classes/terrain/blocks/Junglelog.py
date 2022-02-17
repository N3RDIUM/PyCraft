
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Junglelog
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Junglelog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["jungle_log_top"],
            "front": self.parent.textures["jungle_log"],
            "back": self.parent.textures["jungle_log"],
            "left": self.parent.textures["jungle_log"],
            "right": self.parent.textures["jungle_log"],
            "bottom": self.parent.textures["jungle_log_top"]
        }
