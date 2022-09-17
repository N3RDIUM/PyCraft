from terrain.block import Block
from models.cube import vertices

class Block(Block):
    def __init__(self, *args, **kwargs):
        self.texture = {
            "top": kwargs["texture_manager"].get_texture("grass_top"),
            "bottom": kwargs["texture_manager"].get_texture("dirt"),
            "left": kwargs["texture_manager"].get_texture("grass_side"),
            "right": kwargs["texture_manager"].get_texture("grass_side"),
            "front": kwargs["texture_manager"].get_texture("grass_side"),
            "back": kwargs["texture_manager"].get_texture("grass_side"),
        }
        super().__init__(*args, **kwargs, name="grass", id="PyCraft:Grass", model=vertices, texture=self.texture)
