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

        self.thread = threading.Thread(target=self._constantly_preload, daemon=True)
        self.thread.start()

    def add_generated(self, position, type):
        self.block_types[type].preload(position, self)
        self.blocks[position] = type

    def block_exists(self, position):
        return position in self.blocks

    def generate(self):
        generator.generate(self, self.position)
    
    def _constantly_preload(self):
        while True:
            time.sleep(1)
            for i in self.block_types:
                self.block_types[i].process_preloads()
