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
        self.preloads_per_frame = 64
        self.preloaded = 0
        
        self.added_data = []
        self.process_preloads_thread = threading.Thread(target=self.process_preloads, daemon=True)
        self.process_preloads_thread.start()

    def preload(self, position, chunk):
        """
        preload
        * Preloads the textures of the block
        """
        self.preloads.append((position, chunk))

    def add(self, position, chunk):
        """
        add
        * Adds a block to the world
        :position: the position of the block
        """

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)

        if not chunk.block_exists((x, Y, z)):
            self.renderer.add((x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z), self.tex_coords["top"])
        if not chunk.block_exists((x, y - 1, z)):
            self.renderer.add((x, y, z, X, y, z, X, y, Z, x, y, Z), self.tex_coords["bottom"])
        if not chunk.block_exists((x - 1, y, z)):
            self.renderer.add((x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z), self.tex_coords["left"])
        if not chunk.block_exists((X, y, z)):
            self.renderer.add((X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z), self.tex_coords["right"])
        if not chunk.block_exists((x, y, Z)):
            self.renderer.add((x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z), self.tex_coords["front"])
        if not chunk.block_exists((x, y, z - 1)):
            self.renderer.add((X, y, z,  x, y, z,  x, Y, z,  X, Y, z), self.tex_coords["back"])

    def process_preloads(self):
        """
        process_preloads
        * Processes the preloads
        """
        while True:
            try:
                for i in range(self.preloads_per_frame):
                    if len(self.preloads) > 0:
                        random_index = random.randrange(0, len(self.preloads))
                        position, chunk = self.preloads.pop(random_index)
                        self.add(position, chunk)
            except Exception as e:
                pass
            time.sleep(1/60000)

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
