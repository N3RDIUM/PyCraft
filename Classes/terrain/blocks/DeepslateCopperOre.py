
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateCopperOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateCopperOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_copper_ore"],
            "back": self.parent.textures["deepslate_copper_ore"],
            "left": self.parent.textures["deepslate_copper_ore"],
            "right": self.parent.textures["deepslate_copper_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
