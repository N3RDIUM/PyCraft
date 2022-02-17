
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateCoalOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateCoalOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_coal_ore"],
            "back": self.parent.textures["deepslate_coal_ore"],
            "left": self.parent.textures["deepslate_coal_ore"],
            "right": self.parent.textures["deepslate_coal_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
