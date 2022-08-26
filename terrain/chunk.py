import math


from terrain.block import *
from core.renderer import *
from core.fileutils import *
from core.util import *
from constants import *


class Chunk:
    def __init__(self, position, parent, vbo_id):
        self.position = (position[0] * CHUNK_SIZE, position[1] * CHUNK_SIZE)
        self.parent = parent
        self.block_data = dict(self.parent.block_data)
        self.blocks = self.block_data["blocks"]
        self._blocks = {}
        self._generated = False
        self.listener = ListenerBase('cache/generated/')
        self.writer   = WriterBase('cache/requested/')
        self.vbo_requester = WriterBase('cache/vbo_request/')
        self.vbo_id = vbo_id

    def block_exists(self, position):
        position = encode_position(position)
        return position in self._blocks

    def generate(self):
        blocktypes = get_block_types(self.blocks)
        self.writer.write(f"chunk{encode_position(self.position)}", {
            "position": encode_position(self.position),
            "seed": self.parent.seed,
            "blocktypes": blocktypes,
            "vbo_id": self.vbo_id
        })
        self._generated = True

    def _update(self, player_chunk):
        distance = math.dist(player_chunk, (self.position[0] / CHUNK_SIZE, self.position[1] / CHUNK_SIZE))
        if distance > self.parent.render_distance - 1:
            self.parent.renderer.vbos[self.vbo_id]["render"] = False
        else:
            self.parent.renderer.vbos[self.vbo_id]["render"] = True
