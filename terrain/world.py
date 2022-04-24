from terrain import *
from player import *
import threading

class World:
    def __init__(self, renderer, player):
        self.parent = renderer
        self.chunks = {}
        self.position = (0 * 16, 0 * 16)
        self.render_distance = 1
        self.block_types = {"grass_block": GrassBlock(renderer), "dirt": DirtBlock(renderer)}
        self.to_generate = []
        self.player = player

    def block_exists(self, position):
        return position in self.blocks

    def add_chunk(self, position):
        self.chunks[position] = Chunk(self.parent, self, position)
        target=self.chunks[position].generate()

    def generate(self):
        for i in range(self.position[0] - self.render_distance, self.position[0] + self.render_distance):
            for j in range(self.position[1] - self.render_distance, self.position[1] + self.render_distance):
                if (i, j) not in self.chunks:
                    threading.Thread(target=self.add_chunk((i, j))).start()

    def render(self):
        self.parent.render()
        for i in self.chunks:
            self.chunks[i].update()
                    