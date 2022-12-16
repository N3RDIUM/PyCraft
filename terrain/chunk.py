from terrain.block import *
from core.util import encode_vector
from core.fileutils import WriterBase
import math
from settings import *

class Chunk:
    def __init__(self, renderer, position, parent=None):
        self.renderer = renderer
        self.texture_manager = renderer.texture_manager
        self.position = position
        self.parent = parent
        self.block_handler = parent.block_handler
        self.vbo_id = encode_vector(self.position)
        self.renderer.create_vbo(self.vbo_id)
        self.blocks = {}

        # Request chunk generation from helper
        self.parent._schedule(lambda: self.parent.writer.write(f"{self.parent.writer.written}-{encode_vector(self.position)}", {
            "id"          : self.vbo_id,
            "position"    : list(self.position),
            "blocktypes"  : self.block_handler.pack_blocks_to_json(),
            "seed"        : self.parent.seed
        }))
        self.in_cache = False

    def _drawcall(self):
        if not self.in_cache:
            player_position = self.parent.player.pos
            player_chunk = (player_position[0] // CHUNK_SIZE, player_position[2] // CHUNK_SIZE)

            distance = 2

            try:
                # Get if the chunk is in the player's FOV
                fov = 360 - FOV
                rot = self.parent.player.rot
                chunk_pos = (self.position[0] * CHUNK_SIZE, self.position[1] * CHUNK_SIZE)
                chunk_pos = (chunk_pos[0] - player_position[0], chunk_pos[1] - player_position[2])
                
                # Get the angle between the player and the chunk
                angle = math.atan2(chunk_pos[1], chunk_pos[0])
                angle = math.degrees(angle)
                angle = (angle + rot[1]) % 360

                # If the chunk is in the player's FOV, render it
                if angle < fov / 2 and angle > -fov / 2:
                    self.renderer.vbos[self.vbo_id]["render"] = False
                else:
                    self.renderer.vbos[self.vbo_id]["render"] = True

                # If the chunk is within the render distance, render it
                if abs(self.position[0] - player_chunk[0]) <= distance and abs(self.position[1] - player_chunk[1]) <= distance:
                    self.renderer.vbos[self.vbo_id]["render"] = True

            except KeyError:
                pass

    def _dispose(self):
        try:
            self.renderer.vbos[self.vbo_id]["render"] = False
            self.renderer.delete_vbo(self.vbo_id)
            self.in_cache = True
        except KeyError:
            pass