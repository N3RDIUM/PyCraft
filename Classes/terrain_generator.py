from opensimplex import *
from random import randint
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def log(source, message):
    now = time.strftime("%H:%M:%S")
    logging.debug(f"({now}) [{source}]: {message}")

seed = randint(-999999,999999)
noise = OpenSimplex(seed)
log("terrain_gen",f"Seed is {seed}")

class terrain_gen:
    def __init__(self):
        self.simplex = noise

    def gen_for(self,chunk):
        for i in range(-chunk.CHUNK_DIST,chunk.CHUNK_DIST):
            for j in range(-chunk.CHUNK_DIST,chunk.CHUNK_DIST):
                noiseval_bedrock = 1+int(abs(self.simplex.noise2d(i+chunk.X/chunk.CHUNK_DIST,j+chunk.Z/chunk.CHUNK_DIST)*2))
                noiseval_stone = 10+int(abs(self.simplex.noise2d(i+chunk.X/chunk.CHUNK_DIST,j+chunk.Z/chunk.CHUNK_DIST)*2+self.simplex.noise2d(i+chunk.X/100,j+chunk.Z/100)*10))
                for i_ in range(0,noiseval_bedrock):
                    chunk.add_block(type_="bedrock",block_data={"block_pos": {'x': chunk.X+i, 'y': i_, 'z': chunk.Z+j}},index=(i,i_,j))
                for i_ in range(noiseval_bedrock,noiseval_bedrock+noiseval_stone):
                    if not abs(self.simplex.noise3d(i+chunk.X,i_,j+chunk.Z)*2) > 0.05:
                        chunk.add_block(type_="stone",block_data={"block_pos": {'x': chunk.X+i, 'y': i_, 'z': chunk.Z+j}},index=(i,i_,j))
