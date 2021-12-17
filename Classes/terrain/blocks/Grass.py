import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grass
        
        * Initializes the grass block
        
        :parent: the parent window
        """
        super().__init__("Grass", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["grass_block_top"],
            "front": self.parent.textures["grass_block_side"],
            "back": self.parent.textures["grass_block_side"],
            "left": self.parent.textures["grass_block_side"],
            "right": self.parent.textures["grass_block_side"],
            "bottom": self.parent.textures["dirt"]
        }
