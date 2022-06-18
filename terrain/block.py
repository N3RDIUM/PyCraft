from OpenGL.GL import *
import threading
import random
import time

class Block:
    """
    Block
    * Base block class
    """
    def __init__(self, name, renderer):
        """
        Block.__init__
        :name: name of the block
        :texture: texture of the block
        :parent: the parent window
        """
        self.name = name
        self.renderer = renderer
        self.tex_coords = {}
        self.preloads = []
        self.preloads_per_frame = 1
        self.preloaded = 0
        
        self.added_data = []

    def preload(self, position, chunk, storage):
        """
        preload
        * Preloads the textures of the block
        """
        self.add(position, chunk, storage)

    def add(self, position, chunk, storage):
        """
        add
        * Adds a block to the world
        :position: the position of the block
        """

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)

        if not chunk.world.block_exists((x, Y, z)):
            storage.add((x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z), self.tex_coords["top"])
        if not chunk.world.block_exists((x, y - 1, z)):
            storage.add((x, y, z, X, y, z, X, y, Z, x, y, Z), self.tex_coords["bottom"])
        if not chunk.world.block_exists((x - 1, y, z)):
            storage.add((x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z), self.tex_coords["left"])
        if not chunk.world.block_exists((X, y, z)):
            storage.add((X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z), self.tex_coords["right"])
        if not chunk.world.block_exists((x, y, Z)):
            storage.add((x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z), self.tex_coords["front"])
        if not chunk.world.block_exists((x, y, z - 1)):
            storage.add((X, y, z,  x, y, z,  x, Y, z,  X, Y, z), self.tex_coords["back"])

def all_blocks(renderer):
    """
    all_blocks
    * Returns a list of all blocks
    """
    # List all files in the blocks folder
    # Then import each file as a module
    # Then get the block class from the module
    # Then add the block class to the dictionary
    import os
    import sys
    import importlib

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    blocks = {}
    for file in os.listdir("./terrain/blocks"):
        if file.endswith(".py") and file != "__init__.py":
            module = importlib.import_module("blocks." + file[:-3])
            _block = module.block(renderer)
            blocks[_block.name] = _block

    return blocks
