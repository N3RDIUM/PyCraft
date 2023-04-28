from terrain.blocks.__base import Block

class _Export(Block):
    def __init__(self):
        self.details = {
            "model": "cube",
            "textures": ["_internals/dirt.png"]*6,
            "name": "dirt",
            "id": "_internals/dirt"
        }