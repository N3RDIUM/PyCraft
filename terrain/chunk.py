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

    def add_generated(self, position, type):
        self.block_types[type].preload(position, self)
        self.blocks[position] = type
        self.world.blocks[position] = type

    def block_exists(self, position):
        return position in self.blocks

    def generate(self):
        generator.generate(self, self.position)
