import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        AcaciaLog
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("AcaciaLog", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["acacia_log_top"],
            "front": self.parent.textures["acacia_log"],
            "back": self.parent.textures["acacia_log"],
            "left": self.parent.textures["acacia_log"],
            "right": self.parent.textures["acacia_log"],
            "bottom": self.parent.textures["acacia_log_top"]
        }
