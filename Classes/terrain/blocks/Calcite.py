
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Calcite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Calcite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["calcite"],
            "front": self.parent.textures["calcite"],
            "back": self.parent.textures["calcite"],
            "left": self.parent.textures["calcite"],
            "right": self.parent.textures["calcite"],
            "bottom": self.parent.textures["calcite"]
        }
