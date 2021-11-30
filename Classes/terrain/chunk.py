# imports
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex
from logging import *
from Classes.terrain.block.blocks import *
from Classes.util.math_util import *
import math
from __main__ import test

# values and noise generators
seed = random.randint(0, 100000)
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
        self._scheduled_frame_last = 0

    def generate(self):
        """
        generate

        * Generates the chunk
        """
        # values and constants
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 8

        self.blocks = {}

        # get positions
        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST

        for x in range(int(self.X), int(self.X+self.CHUNK_DIST)):
            for y in range(int(self.Z), int(self.Z+self.CHUNK_DIST)):
                
                # get noise values
                noiseval_grass = 10+int(simplex_grass.noise2d(x/50, y/50)*10+simplex_grass.noise2d(
                    x/100, y/100)*20+simplex_grass.noise2d(x/1000, y/1000)*50)
                noiseval_dirt = 2 + \
                    int(simplex_dirt.noise2d(x/100, y/100)*3 +
                        simplex_dirt.noise2d(x/1000, y/1000)*10)
                noiseval_stone = 20 + \
                    int(simplex_stone.noise2d(x/150, y/150)*40 +
                        simplex_stone.noise2d(x/1000, y/1000)*100)
                
                # do the block generation
                self.blocks[(x, noiseval_grass, y)] = blocks_all["grass"](
                    block_data={"block_pos": {'x': x, 'y': noiseval_grass, 'z': y}}, parent=self)
                pyglet.clock.schedule_once(
                    self.blocks[(x, noiseval_grass, y)].add_to_batch_and_save, 0)
                for i in range(noiseval_grass-noiseval_dirt-1, noiseval_grass):
                    if not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        self.blocks[(x, i, y)] = blocks_all["dirt"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                for i in range(noiseval_grass-noiseval_dirt-noiseval_stone-1, noiseval_grass-noiseval_dirt):
                    if not i == noiseval_grass-noiseval_dirt-noiseval_stone-1 and not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.5 and not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.7:
                        self.blocks[(x, i, y)] = blocks_all["stone"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                    if simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.7 and not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        self.blocks[(x, i, y)] = blocks_all["iron_ore"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                    if simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.99 and not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        self.blocks[(x, i, y)] = blocks_all["gold_ore"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                    elif i == noiseval_grass-noiseval_dirt-noiseval_stone-1:
                        self.blocks[(x, i, y)] = blocks_all["bedrock"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                    elif simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.6 and not simplex_stone.noise3d(x/5, i/5, y/5)*2 > 0.7:
                        self.blocks[(x, i, y)] = None

        # schedule the chunk for rendering
        for i in self.blocks:
            self.parent._all_blocks[i] = self.blocks[i]
            if not type(self.blocks[i]) is type(blocks_all["grass"]) and not type(self.blocks[i]) is type(None):
                pyglet.clock.schedule_once(
                    self.blocks[i].add_to_batch_and_save, random.randint(0,1))

        self.generated = True

    def add_block(self, type_, block_data, index):
        """
        add_block

        * Adds a block to the chunk

        :type_: type of block
        :block_data: data for block
        :index: index of block
        """
        self.blocks[index] = blocks_all[type_](
            block_data=block_data, parent=self)
        self.parent._scheduler_.add_task(
            self.blocks[index].add_to_batch_and_save)

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
