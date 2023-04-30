from terrain.blocks.__base import Block

class _Export(Block):
    def __init__(self):
        self.details = {
            "model": "_internals/cube",
            "texture": {
                "top": "_internals/sand.png",
                "bottom": "_internals/sand.png",
                "left": "_internals/sand.png",
                "right": "_internals/sand.png",
                "front": "_internals/sand.png",
                "back": "_internals/sand.png"
            },
            "texture_type": "all-faces",
            "name": "sand",
            "id": "_internals/sand"
        }