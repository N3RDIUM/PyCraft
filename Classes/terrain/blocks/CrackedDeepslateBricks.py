
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CrackedDeepslateBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CrackedDeepslateBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cracked_deepslate_bricks"],
            "front": self.parent.textures["cracked_deepslate_bricks"],
            "back": self.parent.textures["cracked_deepslate_bricks"],
            "left": self.parent.textures["cracked_deepslate_bricks"],
            "right": self.parent.textures["cracked_deepslate_bricks"],
            "bottom": self.parent.textures["cracked_deepslate_bricks"]
        }
