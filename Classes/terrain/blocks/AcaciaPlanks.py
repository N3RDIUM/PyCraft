import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        AcaciaPlanks
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("AcaciaPlanks", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["acacia_planks"],
            "front": self.parent.textures["acacia_planks"],
            "back": self.parent.textures["acacia_planks"],
            "left": self.parent.textures["acacia_planks"],
            "right": self.parent.textures["acacia_planks"],
            "bottom": self.parent.textures["acacia_planks"]
        }
