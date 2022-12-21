from terrain.block import Block
from models.cube import vertices

class Block(Block):
    def __init__(self, *args, **kwargs):
        self.texture = {
            "top": kwargs["texture_manager"].get_texture("dirt"),
            "bottom": kwargs["texture_manager"].get_texture("dirt"),
            "left": kwargs["texture_manager"].get_texture("dirt"),
            "right": kwargs["texture_manager"].get_texture("dirt"),
            "front": kwargs["texture_manager"].get_texture("dirt"),
            "back": kwargs["texture_manager"].get_texture("dirt"),
        }
        super().__init__(*args, **kwargs, name="dirt", id="PyCraft:Dirt", model=vertices, texture=self.texture)
