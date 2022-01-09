
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BubbleCoralBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BubbleCoralBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["bubble_coral_block"],
            "front": self.parent.textures["bubble_coral_block"],
            "back": self.parent.textures["bubble_coral_block"],
            "left": self.parent.textures["bubble_coral_block"],
            "right": self.parent.textures["bubble_coral_block"],
            "bottom": self.parent.textures["bubble_coral_block"]
        }
