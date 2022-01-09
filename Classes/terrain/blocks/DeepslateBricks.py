
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate_bricks"],
            "front": self.parent.textures["deepslate_bricks"],
            "back": self.parent.textures["deepslate_bricks"],
            "left": self.parent.textures["deepslate_bricks"],
            "right": self.parent.textures["deepslate_bricks"],
            "bottom": self.parent.textures["deepslate_bricks"]
        }
