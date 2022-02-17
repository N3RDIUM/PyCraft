
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateRedstoneOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateRedstoneOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_redstone_ore"],
            "back": self.parent.textures["deepslate_redstone_ore"],
            "left": self.parent.textures["deepslate_redstone_ore"],
            "right": self.parent.textures["deepslate_redstone_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
