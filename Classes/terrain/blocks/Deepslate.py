
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Deepslate
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Deepslate", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate"],
            "back": self.parent.textures["deepslate"],
            "left": self.parent.textures["deepslate"],
            "right": self.parent.textures["deepslate"],
            "bottom": self.parent.textures["deepslate"]
        }
