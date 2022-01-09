
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BoneBlock
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BoneBlock", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["bone_block_top"],
            "front": self.parent.textures["bone_block_side"],
            "back": self.parent.textures["bone_block_side"],
            "left": self.parent.textures["bone_block_side"],
            "right": self.parent.textures["bone_block_side"],
            "bottom": self.parent.textures["bone_block_top"]
        }
