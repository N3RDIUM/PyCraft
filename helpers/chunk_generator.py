import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from constants import *
from terrain.biomes import *
from core.util import encode_position
from core.fileutils import ListenerBase, WriterBase
from core.logger import *
from json import JSONDecodeError

class ChunkGenerator(ListenerBase):
    def __init__(self):
        log("ChunkGenerator", "Initializing...")
        super().__init__("cache/chunk/")
        self.writer = WriterBase("cache/chunk_build/")

    def on(self, data):
        try:
            _simulated_blocks = {}
            _blocks           = {}

            blocktypes = data["blocktypes"]
            vbo_id     = data["id"]
            position   = data["position"]
            position   = [position[0] * CHUNK_SIZE, position[1] * CHUNK_SIZE]
            seed       = data["seed"]

            SEED = seed
            generator = PlainsGenerator()

            for x in range(-1, CHUNK_SIZE + 1):
                for z in range(-1, CHUNK_SIZE + 1):
                    if x == -1 or x == CHUNK_SIZE or z == -1 or z == CHUNK_SIZE:
                        pos = [
                            position[0] + x,
                            position[1] + z
                        ]
                        generator.generate_subchunk(pos, SEED, _simulated_blocks)
                    else:
                        pos = [
                            position[0] + x,
                            position[1] + z
                        ]
                        generator.generate_subchunk(pos, SEED, _blocks)


            self.writer.write(encode_position(position), {
                "id"          : vbo_id,
                "position"    : position,
                "blocktypes"  : blocktypes,
                "blocks"      : _blocks,
                "simulated"   : _simulated_blocks
            })
            log("ChunkGenerator", f"Generated chunk {position} with {len(_blocks)} blocks.")
        except Exception as e:
            log("ChunkGenerator", f"Error while generating chunk: {e}")

if __name__ == "__main__":
    try:
        generator = ChunkGenerator()
        while True:
            if len(generator.queue) > 0:
                try:
                    generator.on(generator.get_last_item())
                except JSONDecodeError:
                    warn("ChunkGenerator", "Invalid JSON data received, skipping...")
                except Exception as e:
                    log("ChunkGenerator", f"Error while generating chunk: {e}")
    except FileNotFoundError:
        pass
    sys.exit()
