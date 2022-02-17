
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateGoldOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateGoldOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_gold_ore"],
            "back": self.parent.textures["deepslate_gold_ore"],
            "left": self.parent.textures["deepslate_gold_ore"],
            "right": self.parent.textures["deepslate_gold_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
