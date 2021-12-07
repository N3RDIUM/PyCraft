# imports
from opensimplex import *
from random import randint
import pyglet
from pyglet.window.key import F
from logger import *
from Classes.terrain.block.blocks import *
from Classes.structures.structure_base import *
import pyximport
pyximport.install()

# Import the terrain generator helper
import Classes.terrain.terrain_generator_helper as helper

def add_to_batch(batch):
    helper.add_to_batch(batch)

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

    def add_block(self,batch, type_, block_data, index):
        """
        add_block

        * Adds a block to the chunk

        :type_: type of block
        :block_data: data for block
        :index: index of block
        """
        self.blocks[index] = blocks_all[type_](block_data=block_data, parent=self)
        self.blocks[index].add_to_batch_and_save(batch)

    def generate_for(self, chunk):
        """
        gen_for

        * Generates terrain for a chunk.

        :chunk: chunk to generate terrain for (Chunk)
        """
        for x in range(int(chunk.X), int(chunk.X+chunk.CHUNK_DIST)):
            for y in range(int(chunk.Z), int(chunk.Z+chunk.CHUNK_DIST)):

                # get noise values
                noiseval_grass = 10+abs(int(self.simplex.noise2d(x/50, y/50)*10+self.simplex.noise2d(
                    x/100, y/100)*20+self.simplex.noise2d(x/1000, y/1000)*50))
                noiseval_dirt = 2 + \
                    abs(int(self.simplex.noise2d(x/100, y/100)*3 +
                        self.simplex.noise2d(x/1000, y/1000)*10))
                noiseval_stone = 20 + \
                    abs(int(self.simplex.noise2d(x/150, y/150)*40 +
                        self.simplex.noise2d(x/1000, y/1000)*100))
                
                # get tree noise
                tree_noise = randint(0,100)
                if tree_noise < 2:
                    tree_pos_y = noiseval_grass
                    chunk.structures[(x,tree_pos_y,y)] = all_structures['birch_tree'](structure_data = {'structure_pos':{'x':x,'y':tree_pos_y,'z':y},'structure_type':'birch_tree'}, parent=chunk)
                
                # do the block generation
                chunk.blocks[(x, noiseval_grass, y)] = blocks_all["grass"](
                    block_data={"block_pos": {'x': x, 'y': noiseval_grass, 'z': y}}, parent=chunk)
                for i in range(noiseval_grass-noiseval_dirt-1, noiseval_grass):
                    if not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        chunk.blocks[(x, i, y)] = blocks_all["dirt"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=chunk)
                for i in range(noiseval_grass-noiseval_dirt-noiseval_stone-1, noiseval_grass-noiseval_dirt):
                    if not i == noiseval_grass-noiseval_dirt-noiseval_stone-1 and not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.5 and not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.7:
                        chunk.blocks[(x, i, y)] = blocks_all["stone"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=chunk)
                    if self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.7 and not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        chunk.blocks[(x, i, y)] = blocks_all["iron_ore"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=chunk)
                    if self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.99 and not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.5:
                        chunk.blocks[(x, i, y)] = blocks_all["gold_ore"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=chunk)
                    elif i == noiseval_grass-noiseval_dirt-noiseval_stone-1:
                        chunk.blocks[(x, i, y)] = blocks_all["bedrock"](
                            block_data={"block_pos": {'x': x, 'y': i, 'z': y}}, parent=chunk)
                    elif self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.6 and not self.simplex.noise3d(x/5, i/5, y/5)*2 > 0.7:
                        chunk.blocks[(x, i, y)] = None 
        for i in chunk.blocks:
            if chunk.blocks[i] is not None:
                chunk.parent._all_blocks[i] = chunk.blocks[i]  

        for i in chunk.structures:
            if chunk.structures[i] is not None:
                chunk.parent._all_structures[i] = chunk.structures[i]

        chunk.generated = True
        exit()

    def add_to_batch(self,chunk):
        for i in chunk.structures:
            if chunk.structures[i] is not None:
                chunk.structures[i].generate()

        add_to_batch(chunk)
