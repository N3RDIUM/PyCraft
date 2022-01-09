
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ChiseledNetherBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ChiseledNetherBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["chiseled_nether_bricks"],
            "front": self.parent.textures["chiseled_nether_bricks"],
            "back": self.parent.textures["chiseled_nether_bricks"],
            "left": self.parent.textures["chiseled_nether_bricks"],
            "right": self.parent.textures["chiseled_nether_bricks"],
            "bottom": self.parent.textures["chiseled_nether_bricks"]
        }
