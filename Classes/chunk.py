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


simplex = OpenSimplex(seed=random.randint(0, 100000))


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
        self.X = X
        self.Z = Z
        self.generated = False
        self._scheduler = TaskScheduler()

    def generate(self):
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 16

        self.blocks = {}

        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST

        for x in range(int(self.X), int(self.X+self.CHUNK_DIST)):
            for y in range(int(self.Z), int(self.Z+self.CHUNK_DIST)):
                self.blocks[(x,y)] = blocks_all["grass"](block_data = {"block_pos":{'x': x, 'y': 0, 'z': y}},parent = self)
                self._scheduler.add_task([self.blocks[(x,y)].add_to_batch_and_save])
        self.generated = True

    def draw(self):
        if self.generated:
            glPushMatrix()
            glTranslatef(self.X, 0, self.Z)
            self.batch.draw()
            glPopMatrix()
        self._scheduler.run()

    def _dispose(self):
        for i in self.graphics:
            self.graphics[i].delete()
        self.graphics = {}
        self.generated = False
