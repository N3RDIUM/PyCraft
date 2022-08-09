import threading
import opensimplex

from terrain.block import *
from core.renderer import *

CHUNK_SIZE = 8

NOISE = opensimplex.OpenSimplex(seed=69)

class Chunk:
    def __init__(self, position, parent):
        self.position = (position[0] * CHUNK_SIZE, position[1] * CHUNK_SIZE)
        self.parent = parent
        self.block_data = dict(self.parent.block_data)
        self.blocks = self.block_data["blocks"]
        self.storage = TerrainMeshStorage(self.parent.renderer)
        
        self._blocks = {}
        self._generated = False

    def block_exists(self, position):
        return position in self._blocks

    def generate(self):
        for i in range(0, CHUNK_SIZE):
            for j in range(0, CHUNK_SIZE):
                self.generate_filament(i + self.position[0], j + self.position[1])
        for index, block in self._blocks.items():
            _block = get_block_by_id(block)
            _block.add_instance(index, self.storage)
        self.parent.renderer.add_mesh(self.storage)
        self._generated = True

    def generate_filament(self, x, y):
        height_noise = abs(round(NOISE.noise2(x / 16, y / 16) * 10))
        height_noise_low = -(abs(64 + round(NOISE.noise2(x / 16, y / 16) * 10)))

        dirt_noise = abs(5 + round(NOISE.noise2(x / 16, y / 16) * 20))

        self._blocks[(x, height_noise, y)] = 1

        for i in range(height_noise_low, height_noise - 1):
            cave_noise = abs(round(NOISE.noise3(x / 16, i/16, y / 16) * 10))
            if i < height_noise and i > height_noise - dirt_noise:
                if cave_noise < 3:
                    self._blocks[(x, i, y)] = 0
            else:
                if cave_noise < 4:
                    self._blocks[(x, i, y)] = 2
