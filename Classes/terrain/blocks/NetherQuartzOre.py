
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        NetherQuartzOre
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("NetherQuartzOre", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["netherrack"],
            "front": self.parent.textures["nether_quartz_ore"],
            "back": self.parent.textures["nether_quartz_ore"],
            "left": self.parent.textures["nether_quartz_ore"],
            "right": self.parent.textures["nether_quartz_ore"],
            "bottom": self.parent.textures["netherrack"]
        }
