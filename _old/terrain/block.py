import os
from importlib import util as importutil
import sys

class Block:
    def __init__(self, texture_manager, *args, **kwargs):
        self.texture_manager = texture_manager
        self.name = kwargs["name"]
        self.id = kwargs["id"]
        self.texture = kwargs["texture"]
        self.model = kwargs["model"]

class BlockHandler:
    def __init__(self, parent):
        self.parent = parent
        self.blocks = {}

        self.load_blocks_from_dir("terrain/blocks", {
            "texture_manager": self.parent.texture_manager
        })

    def register_block(self, block):
        self.blocks[block.id] = block

    def get_block(self, id):
        return self.blocks[id]

    def get_block_by_name(self, name):
        for block in self.blocks.values():
            if block.name == name:
                return block

    def get_block_by_id(self, id):
        return self.blocks[id]

    def load_blocks_from_dir(self, path, args):
        blocks = os.listdir(path)

        for block in blocks:
            if block.endswith(".py") and not block.startswith("__"):
                block = block[:-3]
                spec = importutil.spec_from_file_location(block, f"{path}/{block}.py")
                object = importutil.module_from_spec(spec)
                sys.modules[spec.name] = object
                spec.loader.exec_module(object)

                block = object.Block(**args)
                self.register_block(block)

    def pack_blocks_to_json(self):
        blocks = {}
        for block in self.blocks.values():
            blocks[block.id] = {
                "name": block.name,
                "texture": block.texture,
                "model": block.model,
                "id": block.id
            }

        return blocks
