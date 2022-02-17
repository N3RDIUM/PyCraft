
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        DeepslateIronOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("DeepslateIronOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["deepslate"],
            "front": self.parent.textures["deepslate_iron_ore"],
            "back": self.parent.textures["deepslate_iron_ore"],
            "left": self.parent.textures["deepslate_iron_ore"],
            "right": self.parent.textures["deepslate_iron_ore"],
            "bottom": self.parent.textures["deepslate"]
        }
