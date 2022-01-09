
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        SlimeBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("SlimeBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["slime_block"],
            "front": self.parent.textures["slime_block"],
            "back": self.parent.textures["slime_block"],
            "left": self.parent.textures["slime_block"],
            "right": self.parent.textures["slime_block"],
            "bottom": self.parent.textures["slime_block"]
        }
