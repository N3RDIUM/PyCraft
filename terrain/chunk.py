import time
from terrain.block import *
from terrain.generator import *

generator = Generator()

class Chunk:
    def __init__(self, parent, world, position):
        self.parent = parent
        self.world = world
        self.block_types = world.block_types
        self.blocks = {}
        self.position = (position[0] * 16, position[1] * 16)

        self._scheduled = []

    def add_generated(self, position, type, storage):
        self._scheduled.append(lambda: self.block_types[type].preload(position, self, storage))
        self.blocks[position] = type
        self.world.blocks[position] = type

    def block_exists(self, position):
        return position in self.blocks

    def process(self,):
        for i in range(len(self._scheduled)):
            self._scheduled[i]()
        self._scheduled = []

    def generate(self, storage):
        generator.generate(self, self.position, storage)
