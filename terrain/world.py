import random
from core.logger import *
from terrain.chunk import *
from terrain.block import *
from player.player import *
from settings import *
from core.util import *
import requests

class World:
    def __init__(self, renderer):
        self.renderer = renderer
        self.player = Player(renderer, self)
        self.texture_manager = renderer.texture_manager
        self.block_handler = BlockHandler(self)

        self.chunks = {}
        self.render_distance = 2
        self.seed = random.randint(0, 1000000)

        self.generate()

    def generate_chunk(self, position):
        self.chunks[position] = Chunk(self.renderer, position, self)

    def generate(self):
        for i in range(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                self.generate_chunk((i, j))

    def block_exists(self, position):
        position = encode_vector(position)
        try:
            r = requests.get(f"http://localhost:5079/api/v1/block_exists?position={position}")
            data = r.json()
            if data["exists"]:
                return True, data["block"]
            else:
                return False, None
        except requests.exceptions.ConnectionError:
            return False, None

    def remove_block(self, position):
        position = encode_vector(position)
        try:
            r = requests.get(f"http://localhost:5079/api/v1/remove_block?position={position}")
            data = r.json()
            return data
        except requests.exceptions.ConnectionError:
            return None

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

        to_delete = []
        for chunk in self.chunks.values():
            if chunk.position in positions:
                chunk._drawcall()
            if math.dist(chunk.position, position) > self.render_distance * 2:
                chunk._dispose()
                to_delete.append(chunk.position)   

        for position in to_delete:
            del self.chunks[position]
            # delete request file
            filename = encode_vector(position)
            if os.path.exists(f"cache/chunk_build/{filename}.json"):
                os.remove(f"cache/chunk_build/{filename}.json")
            if os.path.exists(f"cache/chunk/{filename}.json"):
                os.remove(f"cache/chunk/{filename}.json")
