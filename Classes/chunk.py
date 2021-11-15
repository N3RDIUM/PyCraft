from pyglet import gl
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex
import threading
import time
from logging import *
from Classes.block_base import *
import math


seed = random.randint(0, 100000)
print(f"Seed: {seed}")
simplex_grass = OpenSimplex(seed)
simplex_dirt = OpenSimplex(seed)
simplex_stone = OpenSimplex(seed)

def distance_vector_2d(x1, y1, x2, y2):
    return math.dist([x1, y1], [x2, y2])

class Chunk:
    def __init__(self, X, Z, parent):
        self.parent = parent
        self.CHUNK_DIST = parent.CHUNK_DIST
        self.X = X
        self.Z = Z
        self.generated = False
        self.blocks = {}
        self._scheduled_frame_last = 0

    def generate(self):
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 8

        self.blocks = {}

        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST

        for x in range(int(self.X), int(self.X+self.CHUNK_DIST)):
            for y in range(int(self.Z), int(self.Z+self.CHUNK_DIST)):

                noiseval_grass = 10+int(simplex_grass.noise2d(x/50, y/50)*10+simplex_grass.noise2d(x/100, y/100)*20+simplex_grass.noise2d(x/1000, y/1000)*50)
                noiseval_dirt = 2+int(simplex_dirt.noise2d(x/100, y/100)*3+simplex_dirt.noise2d(x/1000, y/1000)*10)
                noiseval_stone = 20+int(simplex_stone.noise2d(x/150, y/150)*40+simplex_stone.noise2d(x/1000, y/1000)*100)

                self.blocks[(x, noiseval_grass, y)] = blocks_all["grass"](
                    block_data={"block_pos": {'x': x, 'y': noiseval_grass, 'z': y}}, parent=self)
                pyglet.clock.schedule_once(self.blocks[(x, noiseval_grass, y)].add_to_batch_and_save, 0)
                for i in range(noiseval_grass-noiseval_dirt-1, noiseval_grass):
                    self.blocks[(x, i, y)] = blocks_all["dirt"](
                        block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                for i in range(noiseval_grass-noiseval_dirt-noiseval_stone-1, noiseval_grass-noiseval_dirt):
                    if not i == noiseval_grass-noiseval_dirt-noiseval_stone-1:
                        self.blocks[(x, i, y)] = blocks_all["stone"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)
                    else:
                        self.blocks[(x, i, y)] = blocks_all["bedrock"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=self)

        for i in self.blocks:
            if not type(self.blocks[i]) == type(blocks_all["grass"]):
                self._scheduled_frame_last += 1
                pyglet.clock.schedule_once(self.blocks[i].add_to_batch_and_save,self._scheduled_frame_last)

        self.generated = True

    def add_block(self,type_,block_data,index):
        self.blocks[index] = blocks_all[type_](
                            block_data=block_data, parent=self)
        self.parent._scheduler_.add_task(self.blocks[index].add_to_batch_and_save)
                            
    def draw(self):
        if self.generated and not distance_vector_2d(self.parent.player.pos[0], self.parent.player.pos[2], self.X, self.Z) > self.parent.chunk_distance*1.5*self.CHUNK_DIST:
            self.batch.draw()
