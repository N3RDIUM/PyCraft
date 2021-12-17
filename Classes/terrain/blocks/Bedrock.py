import Classes as pycraft

class Block(pycraft.Block):
    def __init__(self, *args, **kwargs):
        """
        Grass
        
        * Initializes the grass block
        
        :parent: the parent window
        """
        super().__init__("Stone", *args, **kwargs)

        self.texture = {
            "top": self.parent.textures["bedrock"],
            "front": self.parent.textures["bedrock"],
            "back": self.parent.textures["bedrock"],
            "left": self.parent.textures["bedrock"],
            "right": self.parent.textures["bedrock"],
            "bottom": self.parent.textures["bedrock"]
        }
