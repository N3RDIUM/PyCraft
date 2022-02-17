
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CrackedPolishedBlackstoneBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CrackedPolishedBlackstoneBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cracked_polished_blackstone_bricks"],
            "front": self.parent.textures["cracked_polished_blackstone_bricks"],
            "back": self.parent.textures["cracked_polished_blackstone_bricks"],
            "left": self.parent.textures["cracked_polished_blackstone_bricks"],
            "right": self.parent.textures["cracked_polished_blackstone_bricks"],
            "bottom": self.parent.textures["cracked_polished_blackstone_bricks"]
        }
