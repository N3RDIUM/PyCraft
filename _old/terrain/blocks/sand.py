from terrain.blocks.__base import Block
from models.cube import vertices

class Block(Block):
    def __init__(self, *args, **kwargs):
        self.texture = {
            "top": kwargs["texture_manager"].get_texture("sand"),
            "bottom": kwargs["texture_manager"].get_texture("sand"),
            "left": kwargs["texture_manager"].get_texture("sand"),
            "right": kwargs["texture_manager"].get_texture("sand"),
            "front": kwargs["texture_manager"].get_texture("sand"),
            "back": kwargs["texture_manager"].get_texture("sand"),
        }
        super().__init__(*args, **kwargs, name="sand", id="PyCraft:Sand", model=vertices, texture=self.texture)
