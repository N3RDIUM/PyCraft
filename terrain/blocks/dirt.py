from terrain.blocks.__base import Block

class _Export(Block):
    def __init__(self):
        self.details = {
            "model": "_internals/cube",
            "texture": {
                "top": "_internals/dirt.png",
                "bottom": "_internals/dirt.png",
                "left": "_internals/dirt.png",
                "right": "_internals/dirt.png",
                "front": "_internals/dirt.png",
                "back": "_internals/dirt.png"
            },
            "texture_type": "all-faces",
            "name": "dirt",
            "id": "_internals/dirt"
        }