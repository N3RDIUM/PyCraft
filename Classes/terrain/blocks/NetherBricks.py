
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        NetherBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("NetherBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["nether_bricks"],
            "front": self.parent.textures["nether_bricks"],
            "back": self.parent.textures["nether_bricks"],
            "left": self.parent.textures["nether_bricks"],
            "right": self.parent.textures["nether_bricks"],
            "bottom": self.parent.textures["nether_bricks"]
        }
