# imports
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex
from logging import *
from Classes.terrain.block.blocks import *
from Classes.terrain.terrain_generator import *
from Classes.util.math_util import *
import threading
from __main__ import test

# values and noise generators
seed = random.randint(-99999999, 99999999)
log("Seed" ,str(seed))
simplex_grass = OpenSimplex(seed)
simplex_dirt = OpenSimplex(seed)
simplex_stone = OpenSimplex(seed)

# Chunk Class
class Chunk:
    def __init__(self, X, Z, parent):
        """
        Chunk

        * Class for a chunk of blocks

        :X: X position of chunk
        :Z: Z position of chunk
        :parent: parent world object
        """
        self.parent = parent
        self.CHUNK_DIST = parent.CHUNK_DIST
        self.X = X
        self.Z = Z
        self.generated = False
        self.blocks = {}
        self.structures = {}
        self._scheduled_frame_last = 0
        self.added_to_batch = False

    def generate(self):
        """
        generate

        * Generates the chunk
        """
        # values and constants
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 8
        self.generator = TerrainGenerator()

        self.blocks = {}

        # get positions
        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST
        threading.Thread(target = lambda: self.generator.generate_for(self), daemon = True).start()
        self.generated = True

    def add_block(self, type_, block_data, index):
        """
        add_block

        * Adds a block to the chunk

        :type_: type of block
        :block_data: data for block
        :index: index of block
        """
        self.blocks[index] = blocks_all[type_](block_data=block_data, parent=self)
        self.parent._all_blocks[index] = self.blocks[index]
        pyglet.clock.schedule_once(self.blocks[index].add_to_batch_and_save, randint(0, 1))

    def remove_block(self, index):
        """
        remove_block

        * Removes a block from the chunk

        :index: index of block
        """
        self.blocks[index] = None

    def block_exists(self, index):
        """
        block_exists

        * Checks if a block exists in the chunk

        :index: index of block
        """
        try:
            return self.blocks[index].block_data
        except:
            return False

    def draw(self):
        """
        draw

        * Draws the chunk
        """
        if not test and self.generated and not distance_vector_2d(self.parent.player.pos[0], self.parent.player.pos[2], self.X, self.Z) > self.parent.chunk_distance*1.5*self.CHUNK_DIST:
            self.batch.draw()
        elif test:
            self.batch.draw()

        if self.generated:
            self.add_to_batch()

    def add_to_batch(self):
        """
        add_to_batch

        * Adds the chunk to the batch
        """
        if not self.added_to_batch:
            self.generator.add_to_batch(chunk=self)
            self.added_to_batch = True
