
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PurpurPillar
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PurpurPillar", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["purpur_pillar_top"],
            "front": self.parent.textures["purpur_pillar"],
            "back": self.parent.textures["purpur_pillar"],
            "left": self.parent.textures["purpur_pillar"],
            "right": self.parent.textures["purpur_pillar"],
            "bottom": self.parent.textures["purpur_pillar_top"]
        }
