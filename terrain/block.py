from models import cube, add_position

class Block:
    def __init__(self, data):
        self.data = data

        self.texture_manager = data["texture_manager"]
        self.name            = data["name"]

        self.instances = []

    def add_instance(self, position, storage):
        data = {
            "position": position,
            "vertices": (),
            "tex_coords": (),
            "index_range": (), # Not implemented yet (Index range from the renderer's VBO)
        }

        vertices = cube.vertices["top"]\
            + cube.vertices["bottom"]\
            + cube.vertices["left"]\
            + cube.vertices["right"]\
            + cube.vertices["front"]\
            + cube.vertices["back"]
        data["vertices"] = add_position(position, vertices)

        tex_coords = self.texture_coords["top"]\
            + self.texture_coords["bottom"]\
            + self.texture_coords["left"]\
            + self.texture_coords["right"]\
            + self.texture_coords["front"]\
            + self.texture_coords["back"]
        data["tex_coords"] = tex_coords

        storage.add(data["vertices"], data["tex_coords"])

        self.instances.append(data)

    def remove_instance(self, position, storage):
        raise NotImplementedError

# example block
class GrassBlock(Block):
    def __init__(self, data):
        data["name"] = "grass"
        super().__init__(data)

        self.texture_coords = {
            "top": self.texture_manager.get_texture("grass"),
            "bottom": self.texture_manager.get_texture("dirt"),
            "left": self.texture_manager.get_texture("grass_side"),
            "right": self.texture_manager.get_texture("grass_side"),
            "front": self.texture_manager.get_texture("grass_side"),
            "back": self.texture_manager.get_texture("grass_side"),
        }