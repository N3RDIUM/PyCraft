
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        PolishedAndesite
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("PolishedAndesite", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["polished_andesite"],
            "front": self.parent.textures["polished_andesite"],
            "back": self.parent.textures["polished_andesite"],
            "left": self.parent.textures["polished_andesite"],
            "right": self.parent.textures["polished_andesite"],
            "bottom": self.parent.textures["polished_andesite"]
        }
