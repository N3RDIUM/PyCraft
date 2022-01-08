# imports
import pyglet
import random
import opensimplex
import pyximport
pyximport.install()

# inbuilt imports
from helpers.fast_func_executor import *
from logger import *

class TerrainGenerator:
    """
    TerrainGenerator

    * Initializes the terrain generator
    """
    def __init__(self, parent):
        """
        TerrainGenerator.__init__

        :parent: the parent window
        """
        self.parent = parent
        self.noise = opensimplex.OpenSimplex(seed=self.parent.parent.seed)
        self.queue = []
        self._size = 6

    def generate(self):
        """
        generate

        * Generates a chunk

        :position: the position of the chunk
        """
        for x in range(self.parent.position['x'] - self.parent.parent.chunk_size, self.parent.parent.chunk_size + self.parent.position['x']):
            for z in range(self.parent.position['z'] - self.parent.parent.chunk_size, self.parent.parent.chunk_size + self.parent.position['z']):
                if abs(self.noise.noise2(x / 100, z / 100)) > 0 and abs(self.noise.noise2(x / 100, z / 100)) < 0.6 and not abs(self.noise.noise2(x / 100, z / 100)) > 0.65:
                    fast_exec(lambda: self.parent.parent.biomes['Plains'].generate((x,z), self.parent))
                elif abs(self.noise.noise2(x / 100, z / 100)) > 0.6 and abs(self.noise.noise2(x / 100, z / 100)) < 0.65 and not abs(self.noise.noise2(x / 100, z / 100)) > 0.7:
                    fast_exec(lambda: self.parent.parent.biomes['Jungle'].generate((x,z), self.parent))
                elif abs(self.noise.noise2(x / 100, z / 100)) > 0.6 and abs(self.noise.noise2(x / 100, z / 100)) < 0.75 and not abs(self.noise.noise2(x / 100, z / 100)) > 8:
                    fast_exec(lambda: self.parent.parent.biomes['Desert'].generate((x,z), self.parent))

        pyglet.clock.schedule_once(self.parent._process_preloads, random.randint(1,3))
        pyglet.clock.schedule_once(lambda x: self.parent.parent._process_liquid_instances(), 0)
        exit()
