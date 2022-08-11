import os
import importlib
import threading

from models import cube, add_position

class Block:
    def __init__(self, data, id):
        self.data = data
        self.id   = id

        self.to_add_quantity = 16

        self.texture_manager = data["texture_manager"]
        self.name            = data["name"]
        self.add_handler     = data["add_handler"]
        self.parent          = data["parent"]
        self.add_handler.add(self)

        self.instances = []
        self.to_add    = []

    def add(self, position, storage):
        self.to_add.append((position, storage))

    def add_instance(self, position, storage):
        data = {
            "position": position,
            "vertices": (),
            "tex_coords": (),
            "index_range": (), # Not implemented yet (Index range from the renderer's VBO)
        }

        x, y, z = position

        vertices = []
        tex_coords = []

        chunk = self.parent

        if not chunk.block_exists((x, y + 1, z)):
            vertices.extend(cube.vertices["top"])
            tex_coords.extend(self.texture_coords["top"])

        if not chunk.block_exists((x, y - 1, z)):
            vertices.extend(cube.vertices["bottom"])
            tex_coords.extend(self.texture_coords["bottom"])

        if not chunk.block_exists((x - 1, y, z)):
            vertices.extend(cube.vertices["left"])
            tex_coords.extend(self.texture_coords["left"])

        if not chunk.block_exists((x + 1, y, z)):
            vertices.extend(cube.vertices["right"])
            tex_coords.extend(self.texture_coords["right"])

        if not chunk.block_exists((x, y, z - 1)):
            vertices.extend(cube.vertices["front"])
            tex_coords.extend(self.texture_coords["front"])

        if not chunk.block_exists((x, y, z + 1)):
            vertices.extend(cube.vertices["back"])
            tex_coords.extend(self.texture_coords["back"])
            
        data["vertices"] = add_position(position, vertices)
        data["tex_coords"] = tex_coords

        storage.add(data["vertices"], data["tex_coords"])
        self.instances.append(data)

    def remove_instance(self, position, storage):
        raise NotImplementedError

    def process_to_add(self):
        for i in range(self.to_add_quantity):
            if len(self.to_add) == 0:
                return
            position, storage = self.to_add.pop(0)
            self.add_instance(position, storage)

class BlockHandler:
    def __init__(self):
        self.blocks = {}
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def add(self, block):
        self.blocks[block.name] = block

    def remove(self, block):
        del self.blocks[block.name]

    def run(self):
        for i in self.blocks.values():
            i.process_to_add()

blocks = {}

def get_blocks(renderer, parent):
    ret = {
        "handler": BlockHandler(),
        "blocks":{}
    }

    data = {
        "texture_manager": renderer.texture_manager,
        "add_handler": ret["handler"],
        "parent": parent,
    }

    block_data = os.listdir("terrain/blocks/")
    for i in block_data:
        if i.endswith(".py") and i != "__init__.py":
            importlib.import_module("terrain.blocks." + i[:-3])
            id = len(ret["blocks"])
            block = importlib.import_module("terrain.blocks." + i[:-3])._block(data, id)
            ret["blocks"][block.name] = [block, id]
            ret["handler"].add(block)
            blocks[id] = block

    return ret

def get_block_types(block_data = blocks):
    # create a jsonifiable version of the blocks
    ret = {}
    for blocktype in block_data.values():
        ret[blocktype[0].name] = {
            "name": blocktype[0].name,
            "id": blocktype[1],
            "texture_coords": blocktype[0].texture_coords,
        }
    return ret

def get_block_by_id(id):
    return blocks[id]
