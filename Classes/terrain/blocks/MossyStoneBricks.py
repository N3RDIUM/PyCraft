
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        MossyStoneBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("MossyStoneBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["mossy_stone_bricks"],
            "front": self.parent.textures["mossy_stone_bricks"],
            "back": self.parent.textures["mossy_stone_bricks"],
            "left": self.parent.textures["mossy_stone_bricks"],
            "right": self.parent.textures["mossy_stone_bricks"],
            "bottom": self.parent.textures["mossy_stone_bricks"]
        }
