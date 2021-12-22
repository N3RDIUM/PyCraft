# imports
import pyglet
from pyglet.gl import *
import threading

# Inbuilt imports
import Classes as pycraft
from logger import *

class Chunk:
    """
    Chunk

    * Initializes a chunk
    """
    def __init__(self, parent, position):
        """
        Chunk.__init__

        :parent: the parent world
        :position: the position of the chunk (x, z)
        """
        self.parent = parent
        self.position = {'x': position['x'] * self.parent.chunk_size, 'z': position['z'] * self.parent.chunk_size}

        self.structures = {}

        self.generator = pycraft.TerrainGenerator(self)

        self.batch = pyglet.graphics.Batch()
        
    def add_block(self, type, position):
        """
        add

        * Adds a block to the world

        :position: the position of the block
        """
        self.parent.block_types[type].add(position=position, parent=self)

    def add_preloaded_block(self, type, position):
        """
        add_preloaded

        * Adds a block to the chunk

        :position: the position of the block
        """
        self.parent.block_types[type]._preload_block(position=position, parent=self)
        self.parent.all_blocks[tuple(position)] = self.parent.block_types[type]

    def _process_preloads(self, *args, **kwargs):
        """
        _process_preloads

        * Processes the preloaded blocks
        """
        for block in self.parent.block_types:
            if self.parent.block_types[block]._preload_queue:
                self.parent.block_types[block]._process_preloads(self)

    def generate(self):
        """
        generate

        * Generates a chunk
        """
        threading.Thread(target = self.generator.generate, daemon = True).start()

    def update(self):
        """
        update

        * Updates the chunk
        """
        pass

    def draw(self):
        """
        draw

        * Draws the chunk
        """
        self.batch.draw()

    def remove_block(self, position):
        """
        remove

        * Removes a block from the chunk

        :position: the position of the block
        """
        _type = self.parent.all_blocks[tuple(position)][0]

        self.parent.block_types[_type].remove(tuple(position))
