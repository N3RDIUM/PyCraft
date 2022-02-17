
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Gravel
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Gravel", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["gravel"],
            "front": self.parent.textures["gravel"],
            "back": self.parent.textures["gravel"],
            "left": self.parent.textures["gravel"],
            "right": self.parent.textures["gravel"],
            "bottom": self.parent.textures["gravel"]
        }
