
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        NetherGoldOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("NetherGoldOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["netherrack"],
            "front": self.parent.textures["nether_gold_ore"],
            "back": self.parent.textures["nether_gold_ore"],
            "left": self.parent.textures["nether_gold_ore"],
            "right": self.parent.textures["nether_gold_ore"],
            "bottom": self.parent.textures["netherrack"]
        }
