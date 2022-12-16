import random
from core.logger import *
from terrain.chunk import *
from terrain.block import *
from player.player import *
from settings import *
from core.util import *
from packages.perlin import *
from noise import snoise3
import requests
import threading
import time

class World:
    def __init__(self, renderer):
        self.renderer = renderer
        self.player = Player(renderer, self)
        self.texture_manager = renderer.texture_manager
        self.block_handler = BlockHandler(self)

        self.chunks = {}
        self.writer = WriterBase("cache/chunk/")
        self.render_distance = 12
        self.seed = random.randint(0, 1000000)
        self.to_delete = []
        self.last_update = time.time()
        self.fps = 0
        self.fpss = []
        self.scheduled = []

        self.player.pos = [
            0,
            round(lerp(
                smoothstep(snoise3(0, 0, self.seed)) / 2,
                snoise3(0, 0, self.seed) * 100,
                snoise3(0, 0, self.seed) * 64)
            ),
            0
        ]

        self.thread = threading.Thread(target=self._thread)
        self.thread.start()
        self.generate()

    def _schedule(self, func):
        self.scheduled.append(func)

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
        for chunk in self.chunks.values():
            chunk._drawcall()
            
        self.fps = 1 / (time.time() - self.last_update)
        self.fpss.append(self.fps)
        if len(self.fpss) > FPS_SAMPLES:
            self.fpss.pop(0)
        self.player.update(dt = time.time() - self.last_update)
        self.last_update = time.time()

    def _thread(self):
        while True:
            if len(self.to_delete) == 0 and len(self.scheduled) == 0:
                continue

            for position in self.to_delete:
                del self.chunks[position]
                # delete request file
                filename = encode_vector(position)
                if os.path.exists(f"cache/chunk_build/{filename}.json"):
                    os.remove(f"cache/chunk_build/{filename}.json")
                if os.path.exists(f"cache/chunk/{filename}.json"):
                    os.remove(f"cache/chunk/{filename}.json")
            self.to_delete = []

            for func in self.scheduled:
                func()

            # INFGEN
            position = (round(self.player.pos[0] // CHUNK_SIZE), round(self.player.pos[2] // CHUNK_SIZE))
            positions = []
            for i in range(-self.render_distance + position[0], self.render_distance + position[0]):
                for j in range(-self.render_distance + position[1], self.render_distance + position[1]):
                    if (i, j) not in self.chunks:
                        self.generate_chunk((i, j))
                    positions.append((i, j))

            self.to_delete = []
            for chunk in self.chunks.values():
                if not chunk.position in positions:
                    chunk._dispose()
                    self.to_delete.append(chunk.position)             
