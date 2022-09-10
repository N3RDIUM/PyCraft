from terrain.block import *
from core.util import encode_position
from player.player import Player
from core.fileutils import WriterBase

class Chunk:
    def __init__(self, renderer, position, parent=None):
        self.renderer = renderer
        self.texture_manager = renderer.texture_manager
        self.position = position
        self.parent = parent
        self.block_handler = BlockHandler(self)
        self.player = Player(self.renderer)
        self.writer = WriterBase("cache/chunk/")
        self.vbo_id = encode_position(self.position)
        self.renderer.create_vbo(self.vbo_id)

        # Request chunk generation from helper
        self.writer.write(f"{encode_position(self.position)}", {
            "id"          : self.vbo_id,
            "position"    : list(self.position),
            "blocktypes"  : self.block_handler.pack_blocks_to_json(),
            "seed"        : 69
        })

    def _drawcall(self):
        self.player.update()
