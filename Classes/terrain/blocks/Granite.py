
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Granite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Granite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["granite"],
            "front": self.parent.textures["granite"],
            "back": self.parent.textures["granite"],
            "left": self.parent.textures["granite"],
            "right": self.parent.textures["granite"],
            "bottom": self.parent.textures["granite"]
        }
