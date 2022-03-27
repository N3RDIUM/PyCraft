from email.generator import Generator
from terrain.block import *
from terrain.generator import *

generator = Generator()

class Chunk:
    def __init__(self, parent, position):
        self.parent = parent
        self.block_types = {"grass_block": GrassBlock(parent), "dirt": DirtBlock(parent)}
        self.blocks = {}
        self.position = (position[0] * 16, position[1] * 16)

    def add_generated(self, position, type):
        self.block_types[type].preload(position, self)
        self.blocks[position] = type

    def block_exists(self, position):
        return position in self.blocks

    def generate(self):
        generator.generate(self, self.position)
        for i in self.block_types:
            self.block_types[i].process_preloads()
        self.parent.update_vbo()
