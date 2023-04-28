from terrain.blocks.__base import Block
from models.cube import vertices

class Block(Block):
    def __init__(self, *args, **kwargs):
        self.texture = {
            "top": kwargs["texture_manager"].get_texture("stone"),
            "bottom": kwargs["texture_manager"].get_texture("stone"),
            "left": kwargs["texture_manager"].get_texture("stone"),
            "right": kwargs["texture_manager"].get_texture("stone"),
            "front": kwargs["texture_manager"].get_texture("stone"),
            "back": kwargs["texture_manager"].get_texture("stone"),
        }
        super().__init__(*args, **kwargs, name="stone", id="PyCraft:Stone", model=vertices, texture=self.texture)
