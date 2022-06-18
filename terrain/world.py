from terrain import *
from player import *
from core.renderer import *
import threading
import random

def execute_with_delay(func, delay):
    threading.Timer(delay, func).start()

class ThreadedChunkGenerator:
    def __init__(self, parent):
        self.parent = parent
        
        self.thread = threading.Thread(target=self.generate, daemon=True)
        self.thread.start()

    def generate(self):
        while True:
            if(len(self.parent.to_generate)-1) > 0:
                chunk = self.parent.to_generate.pop(0)
                storage = TerrainMeshStorage(self.parent.parent)
                chunk.generate(storage)
                chunk.process()
                
                self.parent.parent.add(storage.vertices, storage.texCoords)
                
                del storage

class World:
    def __init__(self, renderer, player):
        self.parent = renderer
        self.chunks = {}
        self.blocks = {}
        self.position = (0 * 16, 0 * 16)
        self.render_distance = 3
        self.infgen_threshold = 1
        self.block_types = all_blocks(renderer)
        self.to_generate = []
        self.player = player
        self.generator = ThreadedChunkGenerator(self)

    def block_exists(self, position):
        return position in self.blocks

    def _add_chunk(self, position):
        self.chunks[position] = Chunk(self.parent, self, position)
        self.to_generate.append(self.chunks[position])

    def add_chunk(self, position):
        execute_with_delay(lambda: self._add_chunk(position), random.randrange(1, 2))

    def generate(self):
        for i in range(self.position[0] - self.render_distance, self.position[0] + self.render_distance + 1):
            for j in range(self.position[1] - self.render_distance, self.position[1] + self.render_distance + 1):
                if (i, j) not in self.chunks:
                    self.add_chunk((i, j))

    def update_infgen(self, position):
        player_pos = (position[0] // 16, position[2] // 16)

        if player_pos[0] - self.position[0] > self.infgen_threshold:
            self.position = (self.position[0] + 1, self.position[1])
            self.generate()
        elif player_pos[0] - self.position[0] < -self.infgen_threshold:
            self.position = (self.position[0] - 1, self.position[1])
            self.generate()
        if player_pos[1] - self.position[1] > self.infgen_threshold:
            self.position = (self.position[0], self.position[1] + 1)
            self.generate()
        elif player_pos[1] - self.position[1] < -self.infgen_threshold:
            self.position = (self.position[0], self.position[1] - 1)
            self.generate()

    def render(self):
        self.parent.render()
        self.update_infgen(self.player.pos)
                    