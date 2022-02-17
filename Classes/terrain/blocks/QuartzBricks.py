
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        QuartzBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("QuartzBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["quartz_bricks"],
            "front": self.parent.textures["quartz_bricks"],
            "back": self.parent.textures["quartz_bricks"],
            "left": self.parent.textures["quartz_bricks"],
            "right": self.parent.textures["quartz_bricks"],
            "bottom": self.parent.textures["quartz_bricks"]
        }
