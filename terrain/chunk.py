import threading

from terrain.block import *
from core.renderer import *

CHUNK_SIZE = 16

class Chunk:
    def __init__(self, position, parent):
        self.position = (position[0] // CHUNK_SIZE, position[1] // CHUNK_SIZE)
        self.parent = parent
        self.block_data = get_blocks(parent, self)
        self.blocks = self.block_data["blocks"]
        self.storage = TerrainMeshStorage(self.parent)
        
        self._blocks = {}

    def block_exists(self, position):
        return position in self._blocks

    def load(self):
        self._thread = threading.Thread(target=self.generate, daemon=True)
        self._thread.start()

    def generate(self):
        for i in range(0, CHUNK_SIZE):
            for j in range(0, CHUNK_SIZE):
                self.generate_filament(i, j)
        for index, block in self._blocks.items():
            position = index
            _block = get_block_by_id(block)
            _block.add_instance(position, self.storage)
        self.parent.add_mesh(self.storage)
        self.storage.clear()

    def generate_filament(self, x, y):
        for i in range(-256, 0):
            self._blocks[(x, i, y)] = 0
