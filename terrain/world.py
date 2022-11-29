import random
import math
from terrain.chunk import *
from terrain.block import *
from player.player import *
from constants import *
from core.util import *

class World:
    def __init__(self, renderer):
        self.renderer = renderer
        self.player = Player(renderer)
        self.texture_manager = renderer.texture_manager
        self.block_handler = BlockHandler(self)

        self.chunks = {}
        self.render_distance = 4
        self.seed = random.randint(0, 1000000)

        self.player = Player(renderer)
        self.generate()

    def generate_chunk(self, position):
        self.chunks[position] = Chunk(self.renderer, position, self)

    def generate(self):
        for i in range(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                self.generate_chunk((i, j))

    def block_exists(self, position):
        return NotImplementedError

    def drawcall(self):
        self.player.update()

        # INFGEN
        position = (round(self.player.pos[0] // CHUNK_SIZE), round(self.player.pos[2] // CHUNK_SIZE))
        positions = []
        for i in range(-self.render_distance + position[0], self.render_distance + position[0]):
            for j in range(-self.render_distance + position[1], self.render_distance + position[1]):
                if (i, j) not in self.chunks:
                    self.generate_chunk((i, j))
                    positions.append((i, j))

        for chunk in self.chunks.values():
            chunk._drawcall()
