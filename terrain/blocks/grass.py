from terrain.blocks.__base import Block

class _Export(Block):
    def __init__(self):
        self.details = {
            "model": "_internals/cube",
            "texture": {
                "top": "_internals/grass_top.png",
                "bottom": "_internals/dirt.png",
                "left": "_internals/grass_side.png",
                "right": "_internals/grass_side.png",
                "front": "_internals/grass_side.png",
                "back": "_internals/grass_side.png"
            },
            "texture_type": "single-face",
            "name": "grass",
            "id": "_internals/grass"
        }