
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        CrackedDeepslateTiles
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("CrackedDeepslateTiles", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["cracked_deepslate_tiles"],
            "front": self.parent.textures["cracked_deepslate_tiles"],
            "back": self.parent.textures["cracked_deepslate_tiles"],
            "left": self.parent.textures["cracked_deepslate_tiles"],
            "right": self.parent.textures["cracked_deepslate_tiles"],
            "bottom": self.parent.textures["cracked_deepslate_tiles"]
        }
