
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Bricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Bricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["bricks"],
            "front": self.parent.textures["bricks"],
            "back": self.parent.textures["bricks"],
            "left": self.parent.textures["bricks"],
            "right": self.parent.textures["bricks"],
            "bottom": self.parent.textures["bricks"]
        }
