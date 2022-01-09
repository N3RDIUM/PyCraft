
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PrismarineBricks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PrismarineBricks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["prismarine_bricks"],
            "front": self.parent.textures["prismarine_bricks"],
            "back": self.parent.textures["prismarine_bricks"],
            "left": self.parent.textures["prismarine_bricks"],
            "right": self.parent.textures["prismarine_bricks"],
            "bottom": self.parent.textures["prismarine_bricks"]
        }
