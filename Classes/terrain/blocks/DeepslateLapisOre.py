
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateLapisOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateLapisOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_lapis_ore"],
            "back": self.parent.textures["deepslate_lapis_ore"],
            "left": self.parent.textures["deepslate_lapis_ore"],
            "right": self.parent.textures["deepslate_lapis_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
