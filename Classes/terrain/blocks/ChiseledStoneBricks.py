
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        ChiseledStoneBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("ChiseledStoneBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["chiseled_stone_bricks"],
            "front": self.parent.textures["chiseled_stone_bricks"],
            "back": self.parent.textures["chiseled_stone_bricks"],
            "left": self.parent.textures["chiseled_stone_bricks"],
            "right": self.parent.textures["chiseled_stone_bricks"],
            "bottom": self.parent.textures["chiseled_stone_bricks"]
        }
