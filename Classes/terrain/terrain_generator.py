# imports
import pyglet
import random
import opensimplex

# inbuilt imports
import Classes as pycraft
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

                noiseval_grass = round(pycraft.lerp(self.noise.noise2d(x/10, z/10) * 2, self.noise.noise2d(x/100, z/100) * 10, self.noise.noise2d(x/500, z/500) * 50))
                noiseval_dirt = 1+abs(round(pycraft.lerp(self.noise.noise2d(x/10, z/10) * 2, self.noise.noise2d(x/100, z/100) * 7, self.noise.noise2d(x/500, z/500) * 5)))                
                noiseval_stone = 26+round(self.noise.noise2d(x/5000, z/5000) * 500)

                if not self.noise.noise3d(x/10, noiseval_grass/10, z/10) > 0.4:
                    self.parent.add_preloaded_block("Grass", (x, noiseval_grass, z))
                
                for y in range(noiseval_grass-noiseval_dirt, noiseval_grass):
                    if not self.noise.noise3d(x/10, y/10, z/10) > 0.3:
                        self.parent.add_preloaded_block("Dirt", (x, y, z))

                for y in range(noiseval_grass-noiseval_dirt-noiseval_stone, noiseval_grass-noiseval_dirt):
                    if not abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.2 and abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.1:
                        self.parent.add_preloaded_block("Stone", (x, y, z))
                    elif not abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.1 and abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.05:
                        self.parent.add_preloaded_block("CoalOre", (x, y, z))
                    elif not abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.05 and abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.01:
                        self.parent.add_preloaded_block("IronOre", (x, y, z))
                    elif not abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.01 and abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.005:
                        self.parent.add_preloaded_block("GoldOre", (x, y, z))
                    elif not abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.005 and abs(self.noise.noise3d(x/10, y/10, z/10)) > 0.001:
                        self.parent.add_preloaded_block("DiamondOre", (x, y, z))
                self.parent.add_preloaded_block("Bedrock", (x, noiseval_grass-noiseval_dirt-noiseval_stone-1, z))

                if abs(self.noise.noise2d(x, y)) * 10 < 0.4:
                    self.parent.parent.make_structure((x, noiseval_grass, z), "BirchTree", self.parent)

        pyglet.clock.schedule_once(self.parent._process_preloads, random.randint(1,3))
        exit()
