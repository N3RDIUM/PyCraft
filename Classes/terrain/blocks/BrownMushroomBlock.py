
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BrownMushroomBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BrownMushroomBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["brown_mushroom_block"],
            "front": self.parent.textures["brown_mushroom_block"],
            "back": self.parent.textures["brown_mushroom_block"],
            "left": self.parent.textures["brown_mushroom_block"],
            "right": self.parent.textures["brown_mushroom_block"],
            "bottom": self.parent.textures["brown_mushroom_block"]
        }
