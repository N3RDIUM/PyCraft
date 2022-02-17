
import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Obsidian
        
        * Initializes the block
        
        :parent: the parent window
        """
        super().__init__("Obsidian", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["obsidian"],
            "front": self.parent.textures["obsidian"],
            "back": self.parent.textures["obsidian"],
            "left": self.parent.textures["obsidian"],
            "right": self.parent.textures["obsidian"],
            "bottom": self.parent.textures["obsidian"]
        }
