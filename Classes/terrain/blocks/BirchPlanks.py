import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        BirchPlanks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("BirchPlanks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["birch_planks"],
            "front": self.parent.textures["birch_planks"],
            "back": self.parent.textures["birch_planks"],
            "left": self.parent.textures["birch_planks"],
            "right": self.parent.textures["birch_planks"],
            "bottom": self.parent.textures["birch_planks"]
        }
