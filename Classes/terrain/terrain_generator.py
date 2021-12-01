# imports
from opensimplex import *
from random import randint

from pyglet.window.key import F
from logger import *

# this file is currently not used

# values and noise generators
seed = randint(-999999, 999999)
noise = OpenSimplex(seed)
log("terrain_gen", f"Seed is {seed}")

# terrain generator class
class TerrainGenerator:
    def __init__(self):
        """
        TerrainGenerator

        * Generates terrain for a chunk.
        """
        self.simplex = noise

    def generate_for(self, chunk):
        """
        gen_for

        * Generates terrain for a chunk.

        :chunk: chunk to generate terrain for (Chunk)
        """
        for x in range(-round(chunk.CHUNK_DIST/2), round(chunk.CHUNK_DIST/2)):
            for y in range(-round(chunk.CHUNK_DIST/2), round(chunk.CHUNK_DIST/2)):
                noiseval_bedrock = 1 + int(abs(self.simplex.noise2d(x+chunk.X /
                        chunk.CHUNK_DIST, y+chunk.Z/chunk.CHUNK_DIST)*2))
                noiseval_stone = 10 + int(abs(self.simplex.noise2d(x+chunk.X/chunk.CHUNK_DIST, y +
                                        chunk.Z/chunk.CHUNK_DIST)*2+self.simplex.noise2d(x+chunk.X/100, y+chunk.Z/100)*10))
                noiseval_dirt = 30 + int(abs(self.simplex.noise2d(x+chunk.X/chunk.CHUNK_DIST, y + chunk.Z/chunk.CHUNK_DIST)*2))
                
                for i_ in range(0, noiseval_bedrock):
                    chunk.add_block(type_="bedrock", block_data={"block_pos": {
                        'x': chunk.X+x, 'y': i_, 'z': chunk.Z+y}}, index=(x, i_, y))
                
                for i_ in range(noiseval_bedrock, noiseval_bedrock+noiseval_stone):
                    chunk.add_block(type_="stone", block_data={"block_pos": {
                        'x': chunk.X+x, 'y': i_, 'z': chunk.Z+y}}, index=(x, i_, y))
                
                for i_ in range(noiseval_bedrock+noiseval_stone, noiseval_dirt):
                    chunk.add_block(type_="dirt", block_data={"block_pos": {
                        'x': chunk.X+x, 'y': i_, 'z': chunk.Z+y}}, index=(x, i_, y))
                
                chunk.add_block(type_="grass", block_data={"block_pos": {
                    'x': chunk.X+x, 'y': noiseval_dirt, 'z': chunk.Z+y}}, index=(x, noiseval_dirt, y))                
