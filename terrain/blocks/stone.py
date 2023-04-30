from terrain.blocks.__base import Block

class _Export(Block):
    def __init__(self):
        self.details = {
            "model": "_internals/cube",
            "texture": {
                "top": "_internals/stone.png",
                "bottom": "_internals/stone.png",
                "left": "_internals/stone.png",
                "right": "_internals/stone.png",
                "front": "_internals/stone.png",
                "back": "_internals/stone.png"
            },
            "texture_type": "all-faces",
            "name": "stone",
            "id": "_internals/stone"
        }