
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Tuff
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Tuff", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["tuff"],
            "front": self.parent.textures["tuff"],
            "back": self.parent.textures["tuff"],
            "left": self.parent.textures["tuff"],
            "right": self.parent.textures["tuff"],
            "bottom": self.parent.textures["tuff"]
        }
