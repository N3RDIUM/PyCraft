
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MossyCobblestone
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MossyCobblestone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["mossy_cobblestone"],
            "front": self.parent.textures["mossy_cobblestone"],
            "back": self.parent.textures["mossy_cobblestone"],
            "left": self.parent.textures["mossy_cobblestone"],
            "right": self.parent.textures["mossy_cobblestone"],
            "bottom": self.parent.textures["mossy_cobblestone"]
        }
