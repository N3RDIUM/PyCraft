
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PolishedDiorite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PolishedDiorite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["polished_diorite"],
            "front": self.parent.textures["polished_diorite"],
            "back": self.parent.textures["polished_diorite"],
            "left": self.parent.textures["polished_diorite"],
            "right": self.parent.textures["polished_diorite"],
            "bottom": self.parent.textures["polished_diorite"]
        }
