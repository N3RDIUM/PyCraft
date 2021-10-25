from pyglet import gl
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex
import threading
import time
import logging
from Classes.block_base import *

logging.basicConfig(level=logging.DEBUG)


def log(source, message):
    now = time.strftime("%H:%M:%S")
    logging.debug(f"({now}) [{source}]: {message}")

seed=random.randint(0, 100000)
simplex_grass = OpenSimplex(seed)
simplex_dirt = OpenSimplex(seed)
simplex_stone = OpenSimplex(seed)

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.task_lock = threading.Lock()
        self._frame = 0

    def add_task(self, tasklist):
        # Calculate the appropriate frame to run the task
        APPROPRIATE_FRAME = self._frame + 1
        for i in self.tasks:
            if i[1] == APPROPRIATE_FRAME:
                APPROPRIATE_FRAME += 1

        with self.task_lock:
            self.tasks.append([tasklist, APPROPRIATE_FRAME])

    def run(self):
        try:
            for task in self.tasks:
                if task[1] == self._frame:
                    for i in task[0]:
                        i()
                    del self.tasks[0]
        finally:
            self._frame += 1



class Chunk:
    def __init__(self, X, Z, parent):
        self.parent = parent
        self.CHUNK_DIST = 8
        self.X = X
        self.Z = Z
        self.generated = False
        self.blocks = {}
        self._scheduler = TaskScheduler()
        self._scheduler_less_priority = TaskScheduler()
        self._scheduler_lesser_priority = TaskScheduler()
        self._scheduler_least_priority = TaskScheduler()

    def generate(self):
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 8

        self.blocks = {}

        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST

        for x in range(int(self.X), int(self.X+self.CHUNK_DIST)):
            for y in range(int(self.Z), int(self.Z+self.CHUNK_DIST)):
                noiseval_grass = 10+int(simplex_grass.noise2d(x/50, y/50)*10)
                noiseval_dirt  = 10+int(simplex_dirt.noise2d(x/100, y/100)*3)
                noiseval_stone = 10+int(simplex_stone.noise2d(x/150, y/150)*40)
                self.blocks[(x,noiseval_grass,y)] = blocks_all["grass"](block_data = {"block_pos":{'x': x, 'y': noiseval_grass, 'z': y}},parent = self)
                self._scheduler.add_task([self.blocks[(x,noiseval_grass,y)].add_to_batch_and_save])
                for i in range(noiseval_grass-noiseval_dirt-1,noiseval_grass):
                    self.blocks[(x,i,y)] = blocks_all["dirt"](block_data = {"block_pos":{'x': x, 'y': i, 'z': y}},parent = self)
                    self._scheduler_less_priority.add_task([self.blocks[(x,i,y)].add_to_batch_and_save])
                for i in range(noiseval_grass-noiseval_dirt-noiseval_stone-1,noiseval_grass-noiseval_dirt):
                    self.blocks[(x,i,y)] = blocks_all["stone"](block_data = {"block_pos":{'x': x, 'y': i, 'z': y}},parent = self)
                    self._scheduler_less_priority.add_task([self.blocks[(x,i,y)].add_to_batch_and_save])
                self.blocks[(x,noiseval_grass-noiseval_dirt-noiseval_stone-noiseval_stone-1,y)] = blocks_all["bedrock"](block_data = {"block_pos":{'x': x, 'y': noiseval_grass-noiseval_dirt-noiseval_stone-noiseval_stone-1, 'z': y}},parent = self)
                self._scheduler_lesser_priority.add_task([self.blocks[(x,noiseval_grass-noiseval_dirt-noiseval_stone-noiseval_stone-1,y)].add_to_batch_and_save])
        self.generated = True

    def draw(self):
        if self.generated:
            self.batch.draw()
        self._scheduler.run()
        self._scheduler_less_priority.run()
        self._scheduler_lesser_priority.run()
