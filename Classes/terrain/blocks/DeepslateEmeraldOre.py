
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateEmeraldOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateEmeraldOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_emerald_ore"],
            "back": self.parent.textures["deepslate_emerald_ore"],
            "left": self.parent.textures["deepslate_emerald_ore"],
            "right": self.parent.textures["deepslate_emerald_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
