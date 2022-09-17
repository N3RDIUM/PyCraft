from terrain.block import *
from core.util import encode_position
from player.player import Player
from core.fileutils import WriterBase
import math
from constants import *

class Chunk:
    def __init__(self, renderer, position, parent=None):
        self.renderer = renderer
        self.texture_manager = renderer.texture_manager
        self.position = position
        self.parent = parent
        self.block_handler = parent.block_handler
        self.writer = WriterBase("cache/chunk/")
        self.vbo_id = encode_position(self.position)
        self.renderer.create_vbo(self.vbo_id)

        # Request chunk generation from helper
        self.writer.write(f"{encode_position(self.position)}", {
            "id"          : self.vbo_id,
            "position"    : list(self.position),
            "blocktypes"  : self.block_handler.pack_blocks_to_json(),
            "seed"        : self.parent.seed
        })

    def _drawcall(self):
        player_position = self.parent.player.pos
        player_chunk = (round(player_position[0] // CHUNK_SIZE), round(player_position[2] // CHUNK_SIZE))

        if math.dist((player_chunk[0], player_chunk[1]), (self.position[0], self.position[1])) > self.parent.render_distance // 2:
            self.renderer.vbos[self.vbo_id]["render"] = False
        else:
            self.renderer.vbos[self.vbo_id]["render"] = True
