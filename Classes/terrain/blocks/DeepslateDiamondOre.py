
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateDiamondOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateDiamondOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_diamond_ore"],
            "back": self.parent.textures["deepslate_diamond_ore"],
            "left": self.parent.textures["deepslate_diamond_ore"],
            "right": self.parent.textures["deepslate_diamond_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
