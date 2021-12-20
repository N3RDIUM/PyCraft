import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grass
        
        * Initializes the grass block
        
        :parent: the parent window
        """
        super().__init__("Dirt", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["dirt"],
            "front": self.parent.textures["dirt"],
            "back": self.parent.textures["dirt"],
            "left": self.parent.textures["dirt"],
            "right": self.parent.textures["dirt"],
            "bottom": self.parent.textures["dirt"]
        }
