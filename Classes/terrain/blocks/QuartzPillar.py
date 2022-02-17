
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        QuartzPillar
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("QuartzPillar", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["quartz_pillar_top"],
            "front": self.parent.textures["quartz_pillar"],
            "back": self.parent.textures["quartz_pillar"],
            "left": self.parent.textures["quartz_pillar"],
            "right": self.parent.textures["quartz_pillar"],
            "bottom": self.parent.textures["quartz_pillar_top"]
        }
