
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Cobblestone
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Cobblestone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cobblestone"],
            "front": self.parent.textures["cobblestone"],
            "back": self.parent.textures["cobblestone"],
            "left": self.parent.textures["cobblestone"],
            "right": self.parent.textures["cobblestone"],
            "bottom": self.parent.textures["cobblestone"]
        }
