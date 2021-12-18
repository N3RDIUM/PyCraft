# imports
import pyglet
from pyglet.gl import *

# Inbuilt imports
import Classes as pycraft
from logger import *

class Chunk:
    def __init__(self, parent, position):
        """
        Chunk
        
        * Initializes a chunk
        
        :parent: the parent world
        :position: the position of the chunk (x, z)
        """
        self.parent = parent
        self.position = position

        self.generator = pycraft.TerrainGenerator(self)

        self.batch = pyglet.graphics.Batch()
        
    def add_block(self, type, position):
        """
        add
        
        * Adds a block to the world
        
        :position: the position of the block
        """
        self.parent.block_types[type].add(position=position, parent=self)

    def generate(self):
        """
        generate
        
        * Generates a chunk
        """
        self.generator.generate()

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
        self.all_blocks[tuple(position)].remove()
        del self.all_blocks[tuple(position)]
        del self.parent.all_blocks[tuple(position)]

    def block_exists(self, position):
        """
        block_exists
        
        * Checks if a block exists
        
        :position: the position of the block
        """
        return self.parent.block_exists(position)
